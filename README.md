# Menú Interactivo 3D + AR

Producto de [Code Consulting](https://github.com/). El comensal abre el menú desde su
celular, ve cada platillo en 3D y lo coloca a tamaño real sobre su mesa, sin instalar nada.

El prototipo actual está armado con el menú real de **Aleida · Café y Comida Confortable**
(Mérida, Yucatán).

## Qué hay aquí

| | |
|---|---|
| [`app/`](app/) | El sitio. HTML, CSS y JS planos, sin build. Es lo que se despliega. |
| [`tools/`](tools/) | Scripts de Python que generan los modelos y las imágenes del sitio. |
| [`menu-ar-prd.md`](menu-ar-prd.md) | PRD del producto completo. |
| [`menu-ar-requerimientos.md`](menu-ar-requerimientos.md) | Requerimientos técnicos y análisis de plataformas AR. |
| [`menu-ar-historias-usuario.md`](menu-ar-historias-usuario.md) | Historias de usuario priorizadas. |
| [`menu-ar-demo-plan.md`](menu-ar-demo-plan.md) | Alcance, decisiones y estado de este prototipo. |

## Desplegar

El sitio vive en `app/`, no en la raíz. En Vercel hay que configurar
**Root Directory = `app`**. Instrucciones completas en [`app/README.md`](app/README.md).

```bash
cd app
python -m http.server 8080   # verlo en local
vercel --prod                # o conectar este repo a Vercel
```

## Estado

Colocación en superficie funcionando (ver el platillo en 3D y ponerlo a tamaño real en
la mesa). El seguimiento de imagen sobre la carta impresa —el producto completo descrito
en el PRD— sigue pendiente.

**Falta validar en dispositivo físico:** el AR sólo se puede probar sobre HTTPS, así que
hay que desplegar y abrirlo en un Android y un iPhone reales.

## Avisos

- Los 10 modelos 3D son placeholders CC0 de [Kenney Food Kit](https://kenney.nl/assets/food-kit),
  elegidos por forma parecida. No son los platillos de Aleida.
- 8 de las fotos son de referencia (Wikimedia Commons, CC BY / CC BY-SA) y están
  acreditadas en el pie del menú, como exige su licencia. Hot cakes, chilaquiles,
  capuchino y terraza sí son fotos de Aleida.
- Ambas cosas se sustituyen por material propio del cliente antes de cualquier uso real.
