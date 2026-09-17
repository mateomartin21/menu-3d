"""Builds the .glb files the menu ships.

Source models are Kenney's Food Kit (CC0). Two things happen here:

1. The shared colormap texture is embedded into each file, so a model is a
   single self-contained request.
2. Each model is scaled to the real-world size of the dish it stands in for,
   in metres. model-viewer's `ar-scale="fixed"` then places it on the table at
   true size, and the 3D viewer frames it correctly on its own.

Sizes were derived from each model's measured bounding box (model-viewer's
getDimensions()) against a realistic plate/cup dimension.

    pip install pygltflib
    python tools/build-models.py
"""
import os
import pygltflib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "app", "models")

# file -> uniform scale that brings the model to its real-world size in metres
SCALES = {
    "pancakes.glb": 0.3175,        # ~16 cm stack of hot cakes
    "egg-cooked.glb": 0.3864,      # ~16 cm omelette
    "egg-half.glb": 0.8949,        # ~12 cm
    "egg.glb": 0.4843,             # ~8 cm
    "whole-ham.glb": 0.3126,       # ~20 cm
    "cheese-cut.glb": 0.3646,      # ~14 cm plate
    "cupcake.glb": 0.2124,         # ~9 cm pan dulce
    "burger-cheese.glb": 0.4762,   # ~18 cm plate
    "waffle.glb": 0.4994,          # ~16 cm
    "cheese.glb": 0.2353,          # ~16 cm
}


def bake(filename: str, scale: float) -> None:
    gltf = pygltflib.GLTF2().load(os.path.join(SRC, filename))
    gltf.convert_images(pygltflib.ImageFormat.DATAURI)

    scene = gltf.scenes[gltf.scene or 0]
    # a fresh root keeps every existing node transform untouched
    root = pygltflib.Node(children=list(scene.nodes), scale=[scale, scale, scale])
    gltf.nodes.append(root)
    scene.nodes = [len(gltf.nodes) - 1]

    out_path = os.path.join(OUT, filename)
    gltf.save(out_path)
    print(f"{filename:22} {os.path.getsize(out_path) / 1024:6.1f} KB  scale {scale}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, scale in SCALES.items():
        bake(name, scale)
