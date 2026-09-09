# Atlas de clasificación T08

Abrir [atlas.html](atlas.html) en un navegador. Es un archivo autónomo: incluye las dos imágenes y el catálogo, no necesita conexión ni servidor. El visor es documentación local de la interpretación; no es una versión publicada del simulador.

1. Elegir una de las nueve familias.
2. Seleccionar un registro en la lista o sobre su rectángulo para leer el criterio y su confianza.
3. Alternar la imagen nativa y la lámina anotada para comprobar superposiciones, especialmente CL-F11 en dormitorio 1.

Los rectángulos son localizadores aproximados en píxeles. No usarlos como caras de muros, límites de recintos o dimensiones de mobiliario. La escala métrica y el detalle constructivo se resolverán en T09–T15.

Archivos relacionados:

- [Criterios y pendientes](../../../architecture/classification/README.md).
- [Fuente editable TSV](../../../architecture/classification/t08-trazos.tsv).
- [Catálogo generado JSON](../../../architecture/classification/t08-clasificacion.json).
- [Comprobación automática](comprobacion.json).
- [Validación T08](../../../docs/VALIDACION_T08.md).

Para regenerar, ejecutar `python scripts/build-t08-atlas.py` desde la raíz del repositorio. El proceso comprueba las huellas del PDF y de las referencias T07, valida el catálogo y reconstruye el JSON, este atlas y la comprobación. No modifica las imágenes originales. `.gitattributes` conserva saltos LF en TSV, JSON, HTML y Python para mantener la reproducción entre sistemas.
