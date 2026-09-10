# Evidencias T12

Las láminas contienen referencias originales y anotaciones de interpretación. No son renders de un modelo propio.

- [Baño y logia: continuidad](bano-logia-continuidad.png): contornos T11 sobre planta, guías sin anchura e isométrica original de p20. Baño longitudinal, ducha al fondo y acceso separado de logia.
- [Símbolos del baño](simbolos-del-bano.png): equipo probable de cabecera, lavamanos, inodoro/apoyos, dos reservas achuradas y ducha. Se distingue la lectura de la fuente del equipamiento final.
- [Logia y servicio](logia-y-servicio.png): lavadero, símbolo doble no identificado y franja técnica. Se contrastan ejemplos genéricos de p22/p23 sin adoptar sus dimensiones para el T7.
- [Inventario funcional](lectura-funcional.tsv): doce registros con confianza, interpretación, decisión y tarea de continuidad.
- [Comprobación y huellas](comprobacion.json): integridad de fuentes, contornos, vanos, separación y límites de la verificación.

La entrada está en [t12-interpretacion.json](../../../architecture/topology/t12-interpretacion.json) y el resultado métrico en [t12-topologia.json](../../../architecture/topology/t12-topologia.json). Se generan con `scripts/build-t12-topology.py` sin modificar la planta o isométrica archivadas en T07.

Las regiones coloreadas y sus cierres analíticos no son muros nuevos. Las guías solo prueban continuidad geométrica 2D; no tienen anchura de personaje ni incluyen barridos o equipamiento final. El cómputo de superficie queda en T13 y las dimensiones verticales en T14.
