# Referencias T7 de la página 20

Extraídas el 9 de septiembre de 2026 desde `Presentación Aprobación Proyecto Técnico 2.pdf`, de 42 páginas. El original permanece en la carpeta superior del proyecto; no se modificó ni se incorporó a Git. Su huella y la de cada derivado están en [manifest.json](manifest.json).

| Archivo | Resolución | Uso |
|---|---|---|
| [planta-nativa.png](planta-nativa.png) | 1536 × 813 px | Imagen base del plano, sin las anotaciones añadidas por la lámina. Conserva exactamente los píxeles RGB del objeto PDF 196. |
| [planta-compuesta.png](planta-compuesta.png) | 1851 × 933 px | Referencia visual con los nombres de recintos, flecha y rótulo de acceso y demás elementos superpuestos del PDF. |
| [isometrica-nativa.jpg](isometrica-nativa.jpg) | 915 × 826 px | Isométrica del objeto PDF 195; conserva sus bytes JPEG originales sin recomprimir. |
| [pagina-20-contexto.png](pagina-20-contexto.png) | 2880 × 1620 px | Página completa con encabezado de superficie, planta, isométrica y notas originales. |
| [pagina-20-texto.txt](pagina-20-texto.txt) | Texto UTF-8 | Textos de la página extraídos del PDF. No incluye OCR de las cotas o rótulos internos de las imágenes. |

Las imágenes nativas no están giradas, reflejadas ni redimensionadas. Los dos renders proceden directamente de Poppler a 216 DPI. Esa resolución hace legibles los textos de la lámina, pero no agrega detalle arquitectónico al raster original.

## Diferencias que deben conservarse

La lámina añade contenido sobre la imagen base: nombres de recintos, flecha de acceso y dos apariciones del recurso `Image190` en el sector del dormitorio 1. Por eso la imagen nativa por sí sola no representa todos los elementos visibles de la página. El manifiesto registra la posición de cada recurso; la clasificación de esos elementos corresponde a T08.

El recorte compuesto abarca `[8, 174, 625, 485]` en puntos PDF, con origen en la esquina superior izquierda. Incluye el rótulo completo de acceso, que queda a la derecha del límite de la imagen nativa. Se comprobó que el recorte coincide píxel a píxel con esa región de la página completa.

El encabezado indica 76,66 m² edificados y la imagen del plano indica 76,80 m². Ambos se conservan tal como aparecen. Los dibujos de mobiliario y las notas de la lámina son referencias documentales; las instrucciones del usuario siguen prevaleciendo, incluido un solo lecho en dormitorio 2.

## Estado de calibración

**Sin calibrar en metros.** Las posiciones en puntos PDF, el tamaño en píxeles y los DPI describen los archivos, no la escala del departamento. No se ha verificado aún la superficie geométrica. La lectura de cotas y la calibración corresponden a T09–T13.

Para reproducir desde la raíz `simulador-t7/`, ejecutar `python scripts/extract-t7-references.py` con las bibliotecas y versión de Poppler registradas en el manifiesto. El programa admite `--source`, `--output` y `--pdftoppm`; comprueba la huella esperada del original antes de generar los derivados. Para repetir una comprobación sin reemplazar estos archivos, indicar otra carpeta de salida temporal.
