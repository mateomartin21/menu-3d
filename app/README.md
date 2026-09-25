# Menú interactivo — Aleida Café

Sitio estático. Sin build, sin dependencias que instalar: se sube tal cual.

```
app/
  index.html      estructura
  styles.css      diseño y animaciones
  app.js          datos del menú + interacción
  models/*.glb    10 modelos 3D (tamaño real horneado, ~390 KB en total)
  img/*.webp      logo, florales, fotos reales y renders de los modelos
  vercel.json     cache de assets
```

## Verlo en local

```bash
cd menu-3d/app
python -m http.server 8080
# http://localhost:8080
```

Para probarlo en el celular en la misma red WiFi: `http://TU-IP-LOCAL:8080`.
**El AR no funciona sobre `http://` fuera de `localhost`** — la cámara exige HTTPS, así que
para probar "ver en tu mesa" hay que desplegarlo.

## Desplegar

**Vercel** (gratis):

```bash
npm i -g vercel
cd menu-3d/app
vercel        # preview
vercel --prod # producción
```

**Netlify** (gratis, sin CLI): arrastra la carpeta `app/` a <https://app.netlify.com/drop>.

**GitHub Pages**: sube el contenido de `app/` a una rama `gh-pages`.

Cualquiera de los tres da HTTPS, que es requisito para AR.

Después de desplegar, cambia `og:image` en `index.html` a la URL absoluta
(`https://tu-dominio/img/og.jpg`) para que la vista previa salga bien al compartir por WhatsApp.

## Qué funciona dónde

| | Ver en 3D | Colocar en la mesa a tamaño real |
|---|---|---|
| Android (Chrome) | Sí | Sí — Scene Viewer |
| iPhone (Safari) | Sí | Quick Look; `<model-viewer>` genera el USDZ al vuelo. **Verificar en iPhone real** |
| Escritorio | Sí | No — se avisa en pantalla que se abra desde el celular |

## Fotos

Hot cakes, chilaquiles, el capuchino y la terraza son **fotos reales de Aleida**
(de su ficha de Google Maps). Los otros ocho platillos usan **fotos de referencia de
Wikimedia Commons**, todas CC BY o CC BY-SA: la atribución está en el pie del menú
(`Créditos de fotos de referencia`) y **no se puede quitar** sin cambiar esas fotos.
Sustitúyelas por fotos propias de Aleida en cuanto las haya — es el plan de todos modos.

Para rehacerlas: `python tools/build-stock-photos.py` (fuentes y licencias en
`tools/stock-photos/`). Los assets de marca se rehacen con
`python tools/build-brand-assets.py` (fuentes en `tools/source-photos/`).

## Cambiar el menú

Los 10 platillos viven en el arreglo `DISHES` al inicio de `app.js`
(nombre, precio, descripción, modelo y miniatura). El texto y los precios salen de
su carta física real.

## Cambiar un modelo 3D

Los modelos viven en `app/models/`, ya escalados al tamaño real del platillo (en metros).
Eso es lo que hace que el AR lo coloque a escala correcta sobre la mesa.

**1. Deja el archivo crudo.** Exporta el `.glb` desde Meshy y déjalo en `tools/source-raw/`
(esa carpeta está fuera de git: los exports crudos pesan decenas de MB).

**2. Optimízalo.** Un export de Meshy trae ~850 mil triángulos y pesa 20–30 MB. El menú
tiene presupuesto de ~5 MB por platillo, así que hay que simplificar la malla y bajar la
textura. Requiere Node:

```bash
cd menu-3d/tools
npx @gltf-transform/cli@4 weld   source-raw/PLATILLO.glb /tmp/w.glb
npx @gltf-transform/cli@4 simplify /tmp/w.glb /tmp/s.glb --ratio 0.06 --error 0.002
npx @gltf-transform/cli@4 resize   /tmp/s.glb optimized/PLATILLO.glb --width 1024 --height 1024
```

Con esos valores la hamburguesa pasó de 28 MB a 2 MB **sin diferencia visible**. Si el
modelo sale facetado, sube el `--ratio` (0.10, 0.15). Para ver cuánto pesa cada parte:
`npx @gltf-transform/cli@4 inspect archivo.glb`.

**3. Dale su tamaño real.** Abre `tools/build-models.py` y agrégalo al diccionario
`SCALES` con la escala que lo lleva a metros. Para calcularla: mide el modelo con
`mv.getDimensions()` (el lado más largo) y divide el tamaño real entre ese número.
Los modelos de Meshy salen normalizados a ~2 unidades, así que un plato de 24 cm
es `0.24 / 2.01 = 0.1192`.

```bash
cd menu-3d && python tools/build-models.py
```

El script toma de `optimized/` si el archivo existe ahí, si no de `source/`.

**4. Conéctalo al platillo.** En `app.js`, cambia el `model:` del platillo
correspondiente. Y si quieres, su `thumb:` por una foto real.
