# Prototipo — Menú interactivo para Aleida Café

**Código:** [app/](app/) — sitio estático listo para desplegar · instrucciones en [app/README.md](app/README.md)
**Pipeline de modelos:** [tools/build-models.py](tools/build-models.py)

## Qué es

Prototipo para pitchear a **Aleida · Café y Comida Confortable** (Mérida). El comensal
abre el menú, ve cada platillo en 3D y —desde el celular— lo coloca a tamaño real
sobre su mesa. Es colocación en superficie, **no** el seguimiento de imagen sobre la
carta impresa que describe el [PRD](menu-ar-prd.md); eso sigue pendiente y es el
producto completo. Corresponde a HU-08 del backlog, adelantada.

## Decisiones que importan

**Sitio estático, no Claude Artifact.** Las dos primeras versiones se publicaron como
Artifact y los modelos no cargaban en el navegador real, aunque sí en pruebas locales.
El sandbox de Artifacts bloquea tanto `blob:` como `fetch` de `data:` para alimentar a
`<model-viewer>`, y encima **no sirve archivos `.glb`** (solo tipos web estándar). Fuera
de ese sandbox nada de eso aplica: un host normal sirve el `.glb` y `<model-viewer>`
funciona. Además el AR nativo (Scene Viewer / Quick Look) **necesita una URL pública del
modelo**, cosa que un Artifact no puede dar. Por eso el entregable es una carpeta
estática para Vercel/Netlify — que es justo lo que los [requerimientos §5](menu-ar-requerimientos.md)
ya decían: hosting HTTPS propio, no Artifact.

**Tamaño real horneado en el `.glb`.** El AR coloca el modelo usando las unidades del
archivo (`ar-scale="fixed"`). Los modelos de Kenney vienen en unidades arbitrarias, así
que `tools/build-models.py` les aplica un nodo raíz con la escala que los deja en metros
reales (ej. hot cakes = 16 cm). Antes iba como atributo `scale` en el visor, que
descuadraba el encuadre de la cámara y no era la fuente de verdad para AR.

**Identidad tomada de su material real.** Logo, wordmark "Menú" y los florales están
recortados de la foto de su carta física (ficha de Google Maps), con el fondo de papel
convertido en transparencia. La hoja que invadía el logo se quitó por saturación: la
tinta es negra, el follaje no. Las fotos de hot cakes, chilaquiles, capuchino y la
terraza también son suyas, de la misma ficha. **No tenemos su logo en vector** — si esto
avanza, hay que pedírselos.

**Animación con criterio** (principios de Emil Kowalski): curvas propias
(`cubic-bezier(.23,1,.32,1)` para entradas, `(.32,.72,0,1)` para el drawer), nada por
encima de 340 ms, salidas más rápidas que entradas, `scale(0.97)` al presionar, stagger
de 45 ms en la lista, hover sólo detrás de `@media (hover: hover)`, y
`prefers-reduced-motion` respetado.

## Contenido

Los 10 platillos, precios y descripciones son el texto literal de su carta
(Hot cakes $70 → Pollo a la cordon bleu $150). La división "Desayunos / Platillos
fuertes" es nuestra; la carta impresa no la trae.

Hot cakes y chilaquiles usan **foto real** suya. Los otros 8 usan **fotos de referencia
de Wikimedia Commons** (CC BY / CC BY-SA), acreditadas en el pie del menú porque la
licencia lo exige — hay que reemplazarlas por fotos de Aleida antes de cualquier uso
serio. Los 10 modelos 3D siguen siendo placeholders CC0 de
[Kenney Food Kit](https://kenney.nl/assets/food-kit) elegidos por forma parecida; se
avisa en el pie y se sustituyen por Meshy cuando haya fotos de cada platillo.

## Bugs que costaron encontrar

- **Las imágenes decorativas se estiraban.** Con `width` en CSS y los atributos
  `width`/`height` en el HTML, falta `height: auto` o el atributo gana: un floral de
  660×844 se renderizaba 240×844 y aparecía como una franja rosa cortada a lo largo de
  la página. Era lo que se veía como "cortes" en laptop.
- **`[hidden]` no ocultaba nada.** `.panel { display: flex }` le gana al estilo de
  usuario-agente; sin `[hidden] { display: none !important }` los paneles salían
  abiertos al cargar.
- **Miniaturas invisibles.** El fade-in partía de `opacity: 0` y dependía de JS; ahora
  sólo se marca como pendiente lo que aún está cargando, así que un fallo de script no
  puede dejar el menú sin fotos.

## Estado

Probado en Chromium (390 px y 1280 px): los 10 modelos cargan, cero errores de consola,
el pedido persiste en `localStorage`, el panel es drawer en móvil y modal en escritorio,
y en escritorio avisa que hay que abrirlo desde el celular para el AR.

**Falta la prueba que decide:** desplegarlo y abrirlo en un Android y un iPhone reales
para confirmar "ver en tu mesa". Es exactamente lo que no se pudo validar en las dos
versiones anteriores.

## Siguiente

1. Desplegar (`vercel --prod` desde `app/`, o arrastrar `app/` a Netlify Drop).
2. Abrirlo en Android y iPhone físicos y confirmar el AR a tamaño real.
3. Con eso funcionando: fotos de sus platillos → Meshy → sustituir los 10 placeholders.
4. Pedirles logo en vector y fotos en alta si el pitch avanza.
