# PRD — Menú Interactivo 3D + AR

**Estado:** definición · **Fecha:** 12/09/2026 · **Owner:** Code Consulting
**Documentos relacionados:** [requerimientos técnicos](menu-ar-requerimientos.md) · [historias de usuario](menu-ar-historias-usuario.md)

## 1. Problema

Al leer una carta, el comensal no sabe cómo se ve realmente un plato ni de qué tamaño es la porción. Ante esa incertidumbre pide lo de siempre: el plato conocido y normalmente más barato. El restaurante pierde venta de los platos que mejor margen le dejan y de los que son difíciles de explicar por texto.

Las fotos en la carta ayudan, pero están retocadas, no dan escala real y el comensal ya aprendió a desconfiar de ellas.

## 2. Hipótesis de valor

> Si el comensal puede ver el plato en 3D a tamaño real sobre su propia mesa, pide con más confianza platos que no conocía, y el restaurante sube el ticket promedio.

**Esta hipótesis no está validada y el PRD no asume ningún porcentaje de mejora.** El piloto existe para medirla con datos del propio restaurante. No usar cifras de uplift en material de venta hasta tener medición propia.

Valor secundario, sí observable desde el día uno: **diferenciación**. Ningún restaurante local de la zona lo tiene, y es material que el comensal fotografía y comparte.

## 3. Usuarios

| Usuario | Quién es | Qué necesita | Restricciones reales |
|---|---|---|---|
| **Comensal** | Cliente sentado en la mesa, no técnico | Decidir qué pedir sin arrepentirse | Prisa, poca batería, señal mala, luz baja, está acompañado |
| **Dueño del restaurante** | Nuestro cliente de pago, PyME, no técnico | Vender más y verse moderno | Presupuesto chico, sin equipo de sistemas, escéptico de tecnología |
| **Operador (nosotros)** | Code Consulting | Producir y mantener los modelos con poco tiempo | 3 personas, sin dedicación exclusiva |

## 4. Objetivos y métricas

**Objetivo del piloto:** probar que la experiencia funciona en un local real y que el dueño le ve valor suficiente para pagarla y renovarla.

| Métrica | Cómo se mide | Meta |
|---|---|---|
| Activación | Sesiones iniciadas / mesas atendidas | Línea base a establecer en el piloto |
| Éxito de cámara | Sesiones que ven ≥1 plato / sesiones que llegaron al permiso | **≥ 80%** (técnico, sí es exigible) |
| Fallo de tracking | Sesiones con permiso dado que nunca reconocen la carta | **≤ 10%** |
| Platos vistos por sesión | Evento por plato renderizado | Línea base |
| Tiempo al primer render | Telemetría cliente | **< 2 s** |
| Venta de platos digitalizados | Comparación contra el mismo periodo previo, dato del restaurante | Línea base — **requiere que el cliente comparta ventas antes/después** |

Sin medición no hay caso de venta para el siguiente cliente: **la analítica es alcance de v1, no un extra.**

## 5. Alcance v1

**Incluido**
- Seguimiento de imagen sobre la carta física impresa
- 3-5 platos hero modelados en 3D
- Selector de plato en pantalla, además de apuntar a la carta
- Ficha del plato: nombre, precio, descripción, ingredientes/alérgenos
- Derivación del pedido (canal por definir, ver §9)
- Modo degradado: visor 3D rotable sin cámara
- Analítica de eventos
- Auditoría (y rediseño si hace falta) de la carta física

**Fuera de alcance**
- App nativa
- Pago dentro del menú
- Panel de autogestión para el restaurante
- Modelos animados o con vapor/partículas
- Menú multi-idioma
- Menú completo del restaurante (v1 son solo los platos hero)

## 6. Flujo principal

1. El comensal escanea el QR de la mesa → abre la web
2. Pantalla de bienvenida: qué es, y **por qué pedimos la cámara** (antes del prompt del navegador)
3. Da permiso → se abre la cámara con la instrucción "apunta a la carta"
4. Apunta a la foto de un plato → el modelo aparece anclado sobre la carta
5. Gira, acerca, lee la ficha
6. Cambia de plato: apuntando a otra foto, o desde la lista en pantalla
7. Arma su selección → la envía o se la muestra al mesero

## 7. Requisitos no funcionales

- **Rendimiento:** carga inicial < 3 s en datos móviles; primer render < 2 s; modelos ≤ 2-5 MB
- **Compatibilidad:** iPhone (Safari/WebKit) y Android (Chrome), ambos verificados en dispositivo físico
- **Condiciones reales:** debe funcionar con la iluminación del local de noche
- **Privacidad:** el video de la cámara **se procesa en el dispositivo y no se sube ni se graba**. Debe decirse explícitamente en la pantalla de permiso — sube la tasa de aceptación y nos cubre frente a la LFPDPPP
- **Resiliencia:** negar la cámara, perder señal o fallar el tracking nunca deja pantalla en blanco
- **Sin instalación:** ninguna app, ninguna cuenta, ningún registro

## 8. Dependencias y supuestos

- **Supuesto crítico a validar antes de vender:** una carta impresa real trackea de forma estable bajo luz de restaurante. Si no, el producto no existe en esta forma.
- Requiere hosting HTTPS propio — no puede vivir en un Claude Artifact
- Requiere acceso al local del cliente para probar en condiciones reales
- Requiere que el cliente comparta datos de venta para medir el impacto
- Plataforma AR aún sin decidir (ver requerimientos técnicos §2)

## 9. Preguntas abiertas

| # | Pregunta | Bloquea | Responsable |
|---|---|---|---|
| 1 | ¿El pedido va por WhatsApp al restaurante, o el comensal solo arma su selección y se la muestra al mesero? | Épica de pedido | Definir con el primer cliente |
| 2 | ¿Quién paga el rediseño y reimpresión de la carta si la actual no trackea? | Cotización | Fernando / Ariff |
| 3 | ¿Hosting nuestro (recurrente) o del cliente? | Modelo de precio | Equipo |
| 4 | ¿MindAR o plataforma de pago? | Arquitectura | Tras prueba técnica |
| 5 | ¿Precio del servicio y de cada plato adicional? | Venta | Equipo |

## 10. Fases

| Fase | Objetivo | Criterio de salida |
|---|---|---|
| **0 · Viabilidad** | 1 plato, carta impresa de prueba, MindAR | Trackea estable en iPhone y Android con luz baja |
| **1 · Piloto comercial** | 3-5 platos de un cliente real, en su local | El dueño renueva o recomienda |
| **2 · Escala** | Menú completo, pipeline automatizado | Producir un cliente nuevo en < 1 semana |
