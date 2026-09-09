# T08: clasificación gráfica del plano

Fecha: 9 de septiembre de 2026, America/Santiago. Resultado: T08 completada, con incertidumbres de detalle explícitas para las tareas siguientes.

Se registraron 89 grupos de trazos de la página 20 en [el catálogo de clasificación](../architecture/classification/README.md). Se conservaron por separado los muros, vanos, hojas, mobiliario, equipamiento, cotas, tramas, espacios libres y anotaciones. El [atlas](../references/derived/t08-clasificacion/atlas.html) permite localizarlos sobre la imagen nativa y la lámina compuesta.

## Comprobaciones realizadas

| Comprobación | Resultado observado |
|---|---|
| Integridad de referencias | El generador comprobó la huella del PDF original y las huellas de los archivos de referencia del manifiesto T07; permanecen intactos. |
| Catálogo | 89 registros con 89 IDs únicos, en nueve familias; 77 con confianza alta y 12 con confianza media. |
| Coordenadas | Todos los rectángulos están dentro del marco de su imagen; la transformación entre vistas procede de la colocación registrada en el PDF. |
| Uso geométrico | Escala métrica nula, rectángulos declarados como localizadores y exportación de geometría deshabilitada en los 89 registros. |
| Navegación del atlas | Se probaron las nueve familias en navegador de escritorio; lista y detalle mostraron respectivamente 20, 13, 9, 11, 12, 7, 5, 8 y 4 registros. |
| Tramas del baño | Se seleccionó CL-T02 y se revisó visualmente su localización previa a la ducha, junto con los otros achurados. El criterio descarta un tabique o escalón deducido solo de la trama. |
| Superposición de D1 | Se seleccionó CL-F11 y se alternaron ambos fondos. El panel gris de la composición aparece dentro del localizador y desaparece en la imagen nativa, manteniéndose el registro. |
| Presentación | Se inspeccionaron capturas del atlas en escritorio con el plano, lista y criterio visibles. No se realizó una prueba específica de dispositivos móviles. |

La [comprobación automática](../references/derived/t08-clasificacion/comprobacion.json) registra cantidades, referencias intactas, IDs provisionales y huellas de los derivados. El generador es `scripts/build-t08-atlas.py`; su fuente editable es `architecture/classification/t08-trazos.tsv`. La revisión visual y sus conclusiones se documentan aquí; el generador no las realiza ni las certifica por sí mismo.

## Decisiones y límites

Los achurados del baño, círculos de maniobra, arcos de puertas, líneas de ducha y divisiones de mobiliario no se usarán para crear paredes. Se distingue el acceso a la logia desde cocina y su separación longitudinal respecto del baño. La topología detallada sigue abierta en T12. El acceso principal permanece arriba a la derecha.

Los 12 registros de confianza media tienen su incertidumbre y tarea de resolución en la [tabla de pendientes](../architecture/classification/README.md#doce-registros-provisionales). Ninguna caja localizadora se considera un contorno exacto, un ancho de vano ni un volumen. Algunos registros representan grupos o ejemplos repetidos: no se afirma un despiece de todos los segmentos constructivos.

T08 no valida 76,66 m², escala real, POV, alturas, colisiones ni recorridos; esas verificaciones requieren las fases posteriores. Se conserva la discrepancia documental 76,66/76,80 m². El dibujo fuente de dos camas en D2 no modifica la instrucción de incorporar solo una.

El trabajo afecta documentación y clasificación. No cambió el código de `web/`; no corresponde repetir su compilación ni publicar el sitio en esta tarea. Blender, GLB, colliders y Unreal todavía no se han generado para este departamento. La siguiente tarea es T09: inventariar cotas y espesores legibles y buscar medidas complementarias en el PDF.
