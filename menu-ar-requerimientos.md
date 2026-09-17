# Menú Interactivo 3D + AR — Requerimientos

Producto: el comensal apunta la cámara a la **carta física** y ve el plato en 3D sobre la mesa, puede elegir qué plato ver e interactuar con él, antes de pedir. Sin instalar apps.

> **Cambio de arquitectura (12/09/2026):** el requerimiento de usar la carta física como disparador invalida el enfoque inicial (QR → visor AR nativo). Ver §1.

## 1. Arquitectura requerida: seguimiento de imagen

Hay dos tecnologías AR distintas y necesitamos la segunda:

| | Colocación en superficie | **Seguimiento de imagen** |
|---|---|---|
| Cómo se activa | Detecta el piso/mesa y coloca el modelo donde toques | Reconoce **una imagen impresa** y ancla el modelo sobre ella |
| Quién lo ejecuta | Visor nativo del SO (Quick Look / Scene Viewer) | La página web, procesando la cámara ella misma |
| ¿Sirve para la carta física? | **No** | **Sí** |

**Hallazgos que condicionan todo el diseño:**

- **Quick Look y Scene Viewer no hacen seguimiento de imagen.** Solo colocan sobre superficie. El enfoque de handoff al visor nativo no cumple el requerimiento.
- **iOS Safari no soporta WebXR** (confirmado 2026, sin cambios). Como todo navegador en iOS está obligado a usar WebKit, esto aplica a Chrome y Firefox en iPhone también.
- Por lo tanto la única vía viable es una librería/plataforma que **procese el video de la cámara por su cuenta** (getUserMedia + visión computacional en WebAssembly/WebGL), esquivando WebXR.
- **8th Wall (la referencia del sector) cerró sus servicios hospedados el 28/02/2026** y pasó a open source MIT. Queda descartado como plataforma gestionada.

**UX resultante:** QR en mesa → web → permiso de cámara → "apunta a la carta" → el plato aparece anclado a su foto en la carta → interacción (rotar, escalar, ver info, agregar al pedido) → cambiar de plato apuntando a otra foto **o** desde una lista en pantalla.

## 2. Decisión de plataforma (pendiente de definir)

**Criterio decisivo: costo marginal por cliente.** Vendemos a PyMEs; una suscripción mensual por cada restaurante destruye el margen. La plataforma debe permitir **múltiples clientes en una sola cuenta** (licencia de reseller/agencia), o ser de costo cero.

| Opción | Costo | Multi-cliente | Notas |
|---|---|---|---|
| **MindAR** (open source, MIT) | **$0** | Sí (sin límite) | Funciona en iOS Safari. Mantenido por **un solo desarrollador**; issues abiertos de inestabilidad/jitter; archivos multi-target pesados (reporte de 6 targets → 32 MB) |
| **AR Code** | ~$29 USD/mes o $290/año (licencia comercial Standard) | **Sí — tiene licencia de reseller para agencias** | Mejor encaje con nuestro modelo de negocio. **Falta verificar** si hace seguimiento de imagen o solo QR |
| **Onirix** (España) | €45/mes Starter, €299/mes Professional | Limitado (Starter: 5 escenas/proyecto) | Soporte y documentación en español. Cloud recognition sin límite de imágenes |
| **Kivicube** (la del video) | Gratis y Personal **prohíben uso comercial**. Comercial: ¥5,300/año (~13,800 MXN) | Advanced: 10 escenas | **CDN chino** ("doméstico/nacional") → riesgo real de latencia en México. Marcas de agua y anuncios en planes bajos |
| **Zappar / Mattercraft** | $12.99/mes Developer, $315/mes Pro | Por verificar | Migración natural desde 8th Wall |
| 8th Wall self-hosted | $0 | Sí | Plataforma descontinuada; asumiríamos mantener un motor abandonado. **No recomendado** |

Conversiones aproximadas, verificar tipo de cambio al contratar.

**Recomendación:** correr la prueba técnica con **MindAR** (costo cero) porque el mayor riesgo del proyecto — *¿una carta impresa real, bajo la luz real de un restaurante, trackea de forma estable?* — es independiente de la plataforma. Si la calidad de tracking resulta ser el cuello de botella, ahí sí se justifica pagar por un motor de visión mejor. Si funciona, ahorramos un costo recurrente por cliente.

## 3. Costos de modelado (Meshy, recalculado)

Consumo real medido: **30 créditos por modelo**.

| Plan | Precio | Créditos | Modelos/mes | Costo/modelo | Licencia |
|---|---|---|---|---|---|
| Free | 0 MXN | 100 | 3 | — | **CC BY 4.0 — exige atribución pública. No usable en venta a cliente** |
| Starter | 175 MXN/mes | 250 | 8 | ~22 MXN | Activos privados y propiedad del cliente |
| **Pro** | **349 MXN/mes** (174.5 el 1er mes) | 1000 | **33** | ~10.6 MXN | Licencia privada |
| Premium | 698 MXN/mes (349 el 1er mes) | 3000 | 100 | ~7 MXN | Licencia privada |

**Ojo con los reintentos:** la comida es difícil de reconstruir; hay que presupuestar ~1.5 generaciones por modelo final utilizable. Starter incluye 2 reintentos gratis por tarea, Pro 4, Premium 12. Capacidad realista: Starter ~5 platos/mes, Pro ~22 platos/mes.

**Costo por cliente (5 platos):** 5 × 30 × 1.5 ≈ 225 créditos ≈ **~53 MXN en Pro**.

**Conclusión de negocio: Meshy no es el costo del producto.** El costo real es nuestro tiempo y la plataforma AR. No cotizar el servicio en función de los créditos.

**Plan recomendado:** Starter (175 MXN) para el piloto interno de validación. Subir a Pro cuando entre el primer cliente pagando — el primer mes de Pro cuesta 174.5 MXN, lo mismo que Starter.

## 4. Requerimientos de la carta física ⚠️ nuevo y crítico

Con este enfoque **la carta impresa deja de ser diseño gráfico y pasa a ser un componente técnico**. La mayoría de las cartas existentes NO van a trackear bien.

Cada foto de plato que funcione como disparador debe cumplir:

- **Alto contraste** y detalle definido. Las fotos suaves, borrosas o muy oscuras no generan puntos de referencia.
- **Puntos característicos distribuidos por toda la imagen**, incluidos los bordes. Evitar zonas amplias en blanco.
- **Sin patrones repetitivos** ni simetría fuerte — degradan la detección.
- **Cada plato visualmente distinto de los demás.** Dos fotos parecidas hacen que el sistema confunda un plato con otro.
- **Tamaño impreso suficiente** para escanearse cómodamente a distancia normal de lectura.
- **Acabado mate, no plastificado brillante.** El reflejo de la luz rompe el tracking.

**Implicación comercial:** o rediseñamos la carta física como parte del servicio (entregable adicional, cobrable), o auditamos la del cliente y avisamos que probablemente haya que reimprimirla. Esto debe decirse **en la venta**, no después.

## 5. Requerimientos técnicos

| Requisito | Detalle | Por qué |
|---|---|---|
| Hosting **HTTPS** propio | Obligatorio | La cámara no se activa en contexto inseguro. **No puede vivir en un Claude Artifact** (el sandbox bloquea la cámara) |
| Modelos `.glb` | Uno por plato | Formato que consume el motor web |
| Peso por modelo | **≤ 2-5 MB** | Más estricto que antes: el motor de visión corre en paralelo al render, en el navegador |
| Texturas | ≤ 1-2K, malla decimada, compresión Draco | Presupuesto de peso |
| Escala y pivot | Tamaño real, origen en la base | Que se asiente bien sobre la carta/mesa |
| Archivo de targets | Fotos de la carta compiladas al formato del motor | Vigilar el peso total al sumar platos |
| Selector en pantalla | Lista de platos para cambiar sin apuntar | Fallback cuando el tracking falla o el plato no está a la vista |
| Pantalla de instrucción | "Apunta a la carta" + manejo de permiso denegado | Sin esto el usuario no sabe qué hacer y abandona |
| Detección de navegador in-app | Aviso "abrir en Safari/Chrome" | Los navegadores embebidos de Instagram/Facebook/WhatsApp suelen bloquear la cámara — **riesgo alto, hay que probarlo** |
| `.usdz` (opcional) | Solo si añadimos "ver a tamaño real en tu mesa" vía visor nativo | Función secundaria, no reemplaza el tracking de la carta |

## 6. Herramientas y equipo

| Recurso | Costo | Estado |
|---|---|---|
| Meshy Starter → Pro | 175 → 349 MXN/mes | Por contratar |
| Plataforma AR | $0 (MindAR) o según §2 | **Por decidir tras la prueba** |
| Blender | Gratis | Por instalar |
| `gltf-transform` (Node CLI) | Gratis | Por instalar |
| Hosting HTTPS + dominio | Por definir | Definir si lo proveemos nosotros |
| **Android físico** | — | **Obligatorio para QA** |
| **iPhone físico** | — | **Obligatorio para QA** — es donde están las restricciones (sin WebXR, WebKit forzado) |
| Carta física impresa de prueba | Costo de impresión | **Obligatorio**: el tracking no se valida en pantalla, se valida sobre papel |

## 7. Lo que necesitamos del cliente

**Bloqueantes:**
- Lista de platos a digitalizar (recomendación: **3-5 platos hero**)
- Fotos de cada plato para generar el 3D (plato completo, luz difusa, fondo neutro, sin manos ni utensilios)
- **La carta física actual**, para auditar si sirve como target o hay que rediseñarla
- Nombre, precio, descripción, ingredientes/alérgenos
- Logo y colores de marca
- Destino del pedido: WhatsApp, llamada, o solo consulta
- **Acceso al local para probar con su iluminación real**

## 8. Criterios de aceptación

- [ ] El plato aparece anclado a la carta en < 2 s desde que se apunta
- [ ] El modelo se mantiene estable, sin jitter perceptible, con la mano temblando normal
- [ ] Funciona en iPhone (Safari) y Android (Chrome), ambos probados en dispositivo físico
- [ ] Funciona bajo la iluminación real del restaurante, de noche incluida
- [ ] Se puede cambiar de plato tanto apuntando a otra foto como desde la lista en pantalla
- [ ] El menú carga en < 3 s con datos móviles
- [ ] Si se niega el permiso de cámara, hay mensaje claro y el 3D sigue viéndose sin AR
- [ ] Funciona sin instalar ninguna app

## 9. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Tracking inestable sobre papel real | **Alto — mata el producto** | Prueba con carta impresa antes de vender nada |
| Poca luz en el restaurante | Alto | Probar en el local de noche; considerar carta con más contraste |
| Navegadores in-app bloquean cámara | Alto | Detectar y redirigir a navegador nativo |
| MindAR con un solo mantenedor | Medio | Criterio de salida definido: si falla, migrar a plataforma paga |
| Carta del cliente no sirve como target | Medio | Auditar antes de cotizar; cobrar el rediseño |
| Platos transparentes/brillantes/vapor modelan mal | Medio | Elegir platos hero evitando esos casos |
| Cada plato nuevo = costo recurrente | Bajo | Definir esquema de mantenimiento o precio por plato adicional |

## 10. Fases

1. **Prueba de viabilidad (interna, sin cliente)** — 1 plato, MindAR, carta impresa de prueba, validado en iPhone y Android físicos bajo luz baja. *Decisión: seguir con MindAR o pagar plataforma.*
2. **Piloto comercial** — 3-5 platos hero de un cliente real, carta auditada o rediseñada, probado en su local.
3. **Escala** — menú completo, pipeline de optimización automatizado, esquema de mantenimiento y precio por plato adicional.

## 11. Fuera de alcance (v1)

- App nativa iOS/Android
- Pedido y pago dentro del menú (v1 deriva a WhatsApp)
- Panel de autogestión para el restaurante
- Modelos animados o con partículas (vapor, humo)
- Menú multi-idioma
