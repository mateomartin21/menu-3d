"""Builds the .glb files the menu ships.

Each model is scaled to the real-world size of the dish it stands in for, in
metres. model-viewer's `ar-scale="fixed"` then places it on the table at true
size, and the 3D viewer frames it correctly on its own. Sizes come from each
model's measured bounding box (model-viewer's getDimensions()) against a
realistic plate dimension.

Inputs are read from `optimized/` when a file exists there, otherwise from
`source/`. See README-modelos.md for the optimization step.

    pip install pygltflib
    python tools/build-models.py
"""
import os
import pygltflib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "source")
OPTIMIZED = os.path.join(HERE, "optimized")
OUT = os.path.join(os.path.dirname(HERE), "app", "models")

# file -> (uniform scale to real-world metres, what that size represents)
SCALES = {
    # photoreal Meshy models — stand-ins, but the quality the real dishes will have
    "burger.glb": (0.1100, "plato de 22 cm"),
    "taco.glb": (0.1192, "plato de 24 cm"),
    "hotdog.glb": (0.0905, "18 cm de largo"),
    # Kenney Food Kit (CC0) placeholders
    "pancakes.glb": (0.3175, "16 cm"),
    "egg-cooked.glb": (0.3864, "16 cm"),
    "egg-half.glb": (0.8949, "12 cm"),
    "egg.glb": (0.4843, "8 cm"),
    "whole-ham.glb": (0.3126, "20 cm"),
    "cheese-cut.glb": (0.3646, "14 cm"),
    "cupcake.glb": (0.2124, "9 cm"),
    "burger-cheese.glb": (0.4762, "18 cm"),
    "waffle.glb": (0.4994, "16 cm"),
    "cheese.glb": (0.2353, "16 cm"),
}


def source_path(filename: str) -> str:
    optimized = os.path.join(OPTIMIZED, filename)
    return optimized if os.path.exists(optimized) else os.path.join(SOURCE, filename)


def has_external_images(gltf) -> bool:
    """Kenney's files point at a shared texture on disk; Meshy's embed it already."""
    return any(
        img.uri and not img.uri.startswith("data:") for img in (gltf.images or [])
    )


def bake(filename: str, scale: float, note: str) -> None:
    src = source_path(filename)
    gltf = pygltflib.GLTF2().load(src)

    # only inline textures that live in a separate file — re-encoding an already
    # embedded texture as base64 would just grow the file by a third
    if has_external_images(gltf):
        gltf.convert_images(pygltflib.ImageFormat.DATAURI)

    scene = gltf.scenes[gltf.scene or 0]
    # a fresh root keeps every existing node transform untouched
    root = pygltflib.Node(children=list(scene.nodes), scale=[scale, scale, scale])
    gltf.nodes.append(root)
    scene.nodes = [len(gltf.nodes) - 1]

    out_path = os.path.join(OUT, filename)
    gltf.save(out_path)
    where = "optimized" if src.startswith(OPTIMIZED) else "source"
    print(f"{filename:20} {os.path.getsize(out_path) / 1024:8.1f} KB  {note:15} ({where})")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, (scale, note) in SCALES.items():
        bake(name, scale, note)
