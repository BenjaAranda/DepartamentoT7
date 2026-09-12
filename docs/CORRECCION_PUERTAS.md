# Corrección de puertas y clóset D1

Solicitud del usuario del 12 de septiembre de 2026: corregir logia y eje de dormitorio 1, abrir baño y dormitorio 2 hacia dentro, mantener cerrado el clóset D1.

## Causa y cambio

El GLB importaba correctamente los pivotes, pero una media vuelta alrededor de Y podía descomponerse como giros de 180° en X y Z. El animador web sobrescribía solo Y y conservaba esos otros dos giros. Por ello, la puerta visible y su collider se separaban hasta 0,823 m; ocurría en P03, P04, P06 y la segunda hoja del clóset D1. Las pruebas físicas anteriores no comprobaban esta discrepancia visual.

Ahora `applyDoorAngle` sustituye el cuaternión completo del pivote. No cambia el eje vertical ni su posición de bisagra. Las dos hojas del clóset D1 empiezan cerradas y su geometría coincide con la colisión. No se bloquea su interacción voluntaria.

En la fuente métrica, el baño cambia de +90° a −90°. Dormitorio 2 conserva el giro físico hacia el interior, que ahora se representa correctamente. D1 y logia también giran hacia sus recintos desde la jamba registrada. Los cuatro ejes se montan en la cara interior, con 6 mm de separación adicional al semiespesor de hoja, para que todo el barrido libre el marco. El cambio de sentido solicitado se registra en `architecture/model/door-adjustments.json`, sin alterar el plano histórico del PDF.

Un cuadro de D2 interfería con la hoja al abrirla correctamente; se desplazó 40 cm a lo largo del mismo muro. No se modificaron muros, vanos, dimensiones de muebles, superficie ni altura ocular.

## Validación

- `validation/door-fix/transforms.json`: doce hojas, 91 posiciones cada una. Compara los volúmenes de la malla visible transformada con el collider; incluye reproducción del fallo anterior y estado cerrado del clóset D1. Error máximo actual inferior a 0,022 mm.
- `validation/door-fix/clearance.json`: cuatro puertas, 91 posiciones por puerta contra muros, jambas propias, muebles y todas las mallas estáticas, incluida decoración. Además, 8.281 combinaciones independientes de ángulos entre baño y D2. Cero interferencias por encima de 2 mm de tolerancia numérica.
- Veinte recorridos físicos de ida y vuelta con armarios cerrados/abiertos, doce barridos de motor y 40 contactos repetidos sin atascos; evidencias actuales en `validation/e10/`.
- Revisión interactiva de D1, clóset cerrado, baño/D2 simultáneamente abiertos y logia con entrada/salida. La comprobación final de la revisión publicada y Unreal se registra en `validation/door-fix/release.json`.

Las evidencias históricas de rendimiento mantienen su revisión original. No se renombra una medición antigua para presentarla como nueva. El listado de tareas se reabrió durante la corrección y se cierra tras verificar y publicar.
