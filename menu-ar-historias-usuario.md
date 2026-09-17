# Historias de usuario — Menú Interactivo 3D + AR

Complemento de [PRD](menu-ar-prd.md) y [requerimientos técnicos](menu-ar-requerimientos.md).

**Prioridad:** `P0` piloto · `P1` post-piloto · `P2` escala
**Roles:** Comensal · Dueño (cliente) · Operador (Code Consulting)

---

## E1 · Acceso y arranque

### HU-01 · Entrar sin instalar nada `P0`
**Como** comensal, **quiero** abrir el menú escaneando un QR de la mesa **para** usarlo sin descargar ninguna app.
- Dado el QR de la mesa, cuando lo escaneo con la cámara nativa, entonces se abre la web en < 3 s con datos móviles.
- No se pide registro, cuenta ni datos personales en ningún momento.

### HU-02 · Entender qué hacer `P0`
**Como** comensal, **quiero** entender en 3 segundos qué se espera de mí **para** no abandonar la página.
- Al abrir, veo una instrucción de una sola línea: apuntar la cámara a la carta.
- La instrucción sigue visible mientras no haya un plato reconocido.

### HU-03 · Saber por qué piden mi cámara `P0`
**Como** comensal, **quiero** saber para qué se usa la cámara **antes** de que el navegador me pregunte, **para** decidir con confianza.
- Existe una pantalla propia previa al prompt del navegador que explica el uso.
- Indica explícitamente que **el video no se graba ni se sube**.
- El prompt nativo solo se dispara tras una acción deliberada mía, nunca al cargar.

### HU-04 · No quedarme atorado en un navegador embebido `P0`
**Como** comensal que abrió el link desde Instagram o WhatsApp, **quiero** que me avisen si ahí la cámara no funciona **para** poder abrirlo donde sí.
- Si se detecta navegador in-app, se muestra un aviso con la acción "abrir en Safari/Chrome".
- Se ofrece copiar el enlace como alternativa.

---

## E2 · Ver el plato en AR

### HU-05 · Ver el plato sobre la carta `P0`
**Como** comensal, **quiero** apuntar a la foto de un plato y verlo en 3D anclado sobre la carta **para** saber cómo es realmente antes de pedirlo.
- Dada una foto registrada y permiso concedido, cuando la apunto, el modelo aparece anclado sobre ella en < 2 s.
- El modelo respeta proporción y tamaño real del plato.
- Al retirar la carta del encuadre, el modelo desaparece o se congela de forma limpia, sin parpadeo.

### HU-06 · Que no tiemble `P0`
**Como** comensal, **quiero** que el plato se mantenga estable mientras sostengo el teléfono **para** que se vea creíble y no mareador.
- Con pulso normal a ~30-40 cm, no hay jitter perceptible.
- Se mantiene estable con movimientos suaves de mano y cambios leves de ángulo.

### HU-07 · Girarlo y acercarlo `P0`
**Como** comensal, **quiero** rotar y acercar el modelo **para** verlo por todos lados.
- Arrastrar rota el modelo; pellizcar acerca y aleja.
- Hay forma de volver a la vista inicial.

### HU-08 · Ponerlo en mi mesa a tamaño real `P1`
**Como** comensal, **quiero** colocar el plato sobre mi mesa a tamaño real **para** juzgar si la porción alcanza.
- Existe una acción secundaria para pasar a colocación sobre superficie.
- El tamaño corresponde al real del plato servido.

---

## E3 · Elegir plato e informarse

### HU-09 · Cambiar de plato apuntando `P0`
**Como** comensal, **quiero** apuntar a otra foto de la carta **para** cambiar de plato sin tocar la pantalla.
- Al apuntar a otra foto registrada, el modelo cambia al plato correspondiente.
- Nunca se muestran dos platos a la vez.
- No confunde un plato con otro (criterio de aceptación de diseño de la carta, ver requerimientos §4).

### HU-10 · Elegir desde una lista `P0`
**Como** comensal, **quiero** elegir el plato desde una lista en pantalla **para** no depender de tener la carta enfrente.
- Hay una lista con todos los platos digitalizados, accesible en todo momento.
- Al elegir uno, se muestra aunque la carta no esté en el encuadre.

### HU-11 · Ver la ficha del plato `P0`
**Como** comensal, **quiero** ver precio, descripción e ingredientes **para** decidir, y **para** detectar alérgenos.
- La ficha muestra nombre, precio, descripción e ingredientes/alérgenos.
- Es legible sin tapar el modelo.
- El precio coincide con el de la carta física — discrepancia se trata como defecto.

---

## E4 · Pedir

> Bloqueada por la pregunta abierta #1 del PRD: canal de pedido por definir con el primer cliente.

### HU-12 · Armar mi selección `P0`
**Como** comensal, **quiero** juntar los platos que me interesaron **para** no olvidarlos al pedir.
- Puedo agregar y quitar platos de una selección.
- La selección sobrevive a cambiar de plato y a cerrar el AR.

### HU-13 · Enviar o mostrar el pedido `P1`
**Como** comensal, **quiero** enviar mi selección al restaurante o mostrársela al mesero **para** cerrar el pedido.
- La selección se envía al canal configurado por el restaurante, o se muestra en pantalla en formato legible.
- El destino es configurable por cliente sin tocar código.

---

## E5 · Que nunca se rompa

### HU-14 · Negar la cámara y aun así ver algo `P0`
**Como** comensal que no quiere dar la cámara, **quiero** ver el plato igual **para** que la app me sirva de todos modos.
- Si niego el permiso, se muestra el visor 3D rotable sin AR.
- Se explica qué me estoy perdiendo y cómo activarlo si cambio de opinión.

### HU-15 · Saber que está cargando `P0`
**Como** comensal con mala señal, **quiero** ver que algo está pasando **para** no pensar que se trabó.
- Hay indicador de progreso mientras carga el modelo.
- Si falla la carga, hay mensaje claro y opción de reintentar.

### HU-16 · Ayuda cuando el tracking falla `P0`
**Como** comensal cuya carta no está siendo reconocida, **quiero** que me digan qué hacer **para** lograrlo.
- Si no se reconoce nada en ~10 s, aparece una pista accionable (acercarse, evitar reflejo, más luz).
- La pista no bloquea la pantalla ni impide usar la lista de platos.

---

## E6 · Producción de contenido (interno)

### HU-17 · Auditar la carta antes de cotizar `P0`
**Como** operador, **quiero** evaluar si la carta del cliente sirve como target **para** no comprometerme a algo inviable.
- Existe un checklist de evaluación (contraste, distinción entre platos, patrones, acabado).
- El resultado es un veredicto claro: sirve / sirve con ajustes / hay que rediseñar.
- Se ejecuta **antes** de emitir la cotización.

### HU-18 · Producir un plato `P0`
**Como** operador, **quiero** convertir fotos de un plato en un modelo listo para publicar **para** entregar en tiempo.
- El modelo final pesa ≤ 5 MB, con escala real y origen en la base.
- Queda verificado en iPhone y Android físicos antes de publicarse.
- El proceso está documentado para que cualquiera de los tres lo ejecute.

### HU-19 · Actualizar un plato sin tocar el resto `P1`
**Como** operador, **quiero** agregar o cambiar un plato sin republicar todo **para** que el mantenimiento sea rentable.
- Agregar un plato no obliga a regenerar los demás modelos.
- El cambio queda publicado sin downtime del menú.

---

## E7 · Medición

### HU-20 · Medir uso y fallos `P0`
**Como** Code Consulting, **quiero** medir activación, platos vistos y fallos de tracking **para** probar valor y detectar problemas en campo.
- Se registran: sesión iniciada, permiso concedido/negado, plato renderizado, fallo de tracking, tiempo al primer render.
- Los eventos son anónimos, sin datos personales del comensal.

### HU-21 · Reporte para el dueño `P1`
**Como** dueño del restaurante, **quiero** saber qué platos se ven más **para** entender si esto me sirve.
- Recibe un reporte periódico con platos más vistos y uso general.
- En lenguaje de negocio, sin jerga técnica.

---

## Resumen de prioridades

| Épica | P0 | P1 |
|---|---|---|
| E1 Acceso | HU-01, 02, 03, 04 | — |
| E2 AR | HU-05, 06, 07 | HU-08 |
| E3 Selección | HU-09, 10, 11 | — |
| E4 Pedido | HU-12 | HU-13 |
| E5 Resiliencia | HU-14, 15, 16 | — |
| E6 Producción | HU-17, 18 | HU-19 |
| E7 Medición | HU-20 | HU-21 |

**Total P0: 17 historias.** HU-05 y HU-06 son las que deciden si el producto existe — se validan en la Fase 0 antes que cualquier otra.
