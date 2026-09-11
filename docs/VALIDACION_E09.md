# E09 — Web y comprobaciones de recorrido

Estado: en ejecución. Revisión geométrica `3b8848a03f921bd64711cc458be818a92fc938ee4860b824629ffd188bd66806`.

## Resultados comprobados

- GLB web: 1.497.004 bytes frente a 2.338.412 del intercambio original. Se conservan 511 nodos y 12 pivotes. Desviación máxima de límites por compresión: 0,084 mm. El GLB para Unreal permanece intacto.
- Carga atómica de modelo y colisiones, verificación de huellas, escala, altura ocular y revisión. Once comprobaciones cubren descargas fallidas, corrupción, versiones mezcladas, cancelación, reintento y liberación de recursos.
- Veinte recorridos mediante el controlador real: diez con armarios cerrados y diez abiertos. La cámara se mantiene a 1,60 m sobre el suelo de apoyo, sin ocultar caídas fuera del piso.
- Las doce hojas completan sus barridos cuando están libres. Una puerta junto al visitante activo se detiene; desplazamiento numérico observado de 0,103 mm, inferior al criterio de 1 mm.
- Se reprodujo y corrigió un atasco numérico junto a la puerta cerrada de D3. La prueba de regresión comprueba la retirada sin reiniciar.
- Sin penetraciones entre los 28 conjuntos de mobiliario/decoración y la arquitectura. Repetidos los controles de paredes, ventanas, pausa, velocidad diagonal y cuadros lentos sobre la escena amueblada.

## Navegador e interfaz

Revisión real en el navegador integrado de Codex, sobre NVIDIA RTX 4070 Laptop GPU mediante ANGLE/D3D11. Se probaron planta, isométrica, recorrido, pausa, regreso al acceso, cambio desde la referencia al modelo, ayuda y controles en pantalla a 390 × 844. Una pulsación breve en Avanzar produjo desplazamiento real con colisiones.

Se implementaron siete acciones WebMCP y se comprobó el rechazo de argumentos inválidos en todas ellas. Movimiento en pausa rechazado. La interacción de acceso se repitió en el navegador tras corregir el empuje y mantuvo la posición del visitante.

Se detectó y corrigió un uso del controlador ya liberado durante la recarga de desarrollo. La revisión posterior del navegador nuevo no mostró errores de aplicación.

Las sombras permanecen almacenadas mientras la geometría está quieta y se actualizan al girar hojas o cambiar de modo. Medición preliminar: aproximadamente 125 FPS, p95 de 8,1 ms y entre 176–684 llamadas de dibujo en inspecciones del pasillo. **No es todavía la medición final V12**: se debe repetir una ruta de 60 segundos en la revisión final y registrar carga/memoria. La comparación previa rondaba 70 FPS y 5.607 llamadas con sombras recalculadas continuamente.

Chrome y Edge separados no están disponibles en las herramientas de navegador de esta sesión; ambos intentos devolvieron `Browser is not available`. El tamaño móvil es una emulación de viewport sobre el mismo equipo, no una medición de teléfono real. Pantalla completa nativa depende del navegador; la interfaz informa si este no la admite.

## Pendiente

Cerrar comprobación final de controles, medición V12–V14, prueba controlada de propagación Blender/GLB/colliders/Unreal y compilación de entrega. Los informes actuales se encuentran en `validation/e09/`; no cierran por sí solos E10 ni publicación.
