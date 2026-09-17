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

Los modelos actuales son placeholders CC0 de [Kenney Food Kit](https://kenney.nl/assets/food-kit),
elegidos por forma parecida — no son los platillos reales. Para sustituir uno por un
render de Meshy:

1. Exporta el `.glb` desde Meshy.
2. Déjalo en `menu-3d/tools/source/`.
3. Agrega su escala real (en metros) al diccionario `SCALES` de `tools/build-models.py`
   y corre `python tools/build-models.py`. Ese paso incrusta la textura y hornea el
   tamaño real, que es lo que hace que el AR lo coloque a escala correcta.
4. Apunta el platillo a ese archivo en `app.js`.
5. Regenera su miniatura con `tools/poster-gen.html` (o usa una foto real del platillo).
