# T07: referencias extraídas y archivadas

Fecha: 9 de septiembre de 2026, America/Santiago. Resultado: T07 completada.

Se archivaron las referencias de la página 20, índice interno 19, en `references/derived/p20-t7/`. El PDF fuente tiene 42 páginas, 18.295.204 bytes y página de 960 × 540 puntos, sin rotación. Antes y después de extraer mantuvo la huella SHA-256 `ad8e0871ed6afb7117e2dafa80bc28ad90b3c845709dc268ba01fcd12259aeec`.

## Comprobaciones realizadas

| Referencia | Evidencia |
|---|---|
| Planta nativa | PNG de 1536 × 813 px, objeto 196. Sus píxeles RGB coinciden con los datos decodificados del PDF. |
| Isométrica nativa | JPEG de 915 × 826 px, objeto 195. Los bytes coinciden con el flujo JPEG original del PDF, sin nueva compresión. |
| Página completa | Render de Poppler a 216 DPI, 2880 × 1620 px, con encabezado, superficie, notas y ambas vistas. |
| Planta con anotaciones | Render de 1851 × 933 px. Coincide píxel a píxel con su región de la página completa. |
| Procedencia | Manifiesto con objetos PDF, posiciones, resolución, formato, tamaño, herramientas y huellas de los archivos. |
| Integridad del original | Misma huella antes y después; original conservado fuera del repositorio. |

Se revisaron visualmente las cuatro imágenes. La planta compuesta conserva los recintos completos visibles en la lámina, los rótulos y la flecha de acceso superior derecha. La isométrica conserva su orientación y contenido original. La repetición del proceso produjo las mismas huellas en las cuatro imágenes revisadas.

La imagen nativa del plano no contiene los nombres añadidos por el PDF ni sus dos superposiciones del recurso `Image190`. Se conserva también la composición completa para evitar perder esos datos al interpretar el plano. Su clasificación arquitectónica se realizará en T08.

## Archivos y alcance

El [índice de referencias](../references/derived/p20-t7/README.md) enlaza las imágenes y explica su uso. `manifest.json` conserva la evidencia técnica; `pagina-20-texto.txt` recoge los textos propios de la lámina sin pretender haber leído las cotas raster mediante OCR. La extracción es reproducible con `scripts/extract-t7-references.py`.

Las cuatro imágenes suman 1.721.887 bytes y se conservan como archivos completos en Git normal, de acuerdo con la política de referencias. No se modificaron la aplicación, Blender ni Unreal, ni se publicó el sitio. No se repitieron pruebas web porque esta tarea solo incorpora referencias y documentación.

Se fijaron saltos LF para los archivos `.txt`, para conservar la huella del texto extraído también al recuperar el repositorio en Windows. El seguimiento remoto quedó sincronizado y su comprobación independiente pasó el `2026-09-09T15:34:57.913Z`: 15 casillas completas y 63 pendientes; E02 continúa abierta con T07 verificada.

T07 no establece metros por píxel ni valida 76,66 m². Se conservan los rótulos contradictorios de 76,66 m² en el encabezado y 76,80 m² en la imagen. La interpretación y la calibración continúan en T08–T15; no se inventaron cotas ni se alteraron los dibujos para resolver esa diferencia.

Siguiente tarea: T08, clasificar muros, vanos, hojas, mobiliario, equipamiento, cotas, tramas y espacios libres antes de modelar.
