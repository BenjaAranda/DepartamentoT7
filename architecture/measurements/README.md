# Inventario de cotas y espesores T09

Fecha: 9 de septiembre de 2026. Se registraron 58 lecturas y referencias: 14 cotas locales del T7, ocho menciones de espesor, 28 rótulos de tabiques, cuatro menciones de superficie y cuatro referencias complementarias. Se revisó el texto extraíble y una vista general de las 42 páginas, ampliando las imágenes técnicas relevantes.

La fuente editable es [t09-inventario.tsv](t09-inventario.tsv). El [JSON generado](t09-inventario.json) añade procedencia, conversión condicional de unidades y comprobaciones. Cada entrada conserva ubicación textual, página/imagen, rectángulo exacto del recorte de lectura, confianza, vínculo con T08 y límite de uso. Consultar también las [láminas de lecturas](../../references/derived/t09-medidas/README.md) y la [revisión por páginas](t09-revision-pdf.json).

## Cotas locales

Las cifras locales no llevan una unidad impresa junto a ellas. Se propone **cm como unidad inferida**, por el contexto conjunto de maniobra, equipos y rótulos de 15 cm. Esto deberá contrastarse con controles horizontales y verticales en T10. La confianza de lectura de una cifra no confirma su unidad ni los extremos que mide.

| ID | Lectura | Ubicación | Confianza de lectura | Uso previsto |
|---|---|---|---|---|
| T09-D01 | ø 150 | Giro junto a D3 | Alta | Control secundario de diámetro |
| T09-D02 | ø 150 | Giro de D1 | Alta | Control secundario de diámetro |
| T09-D03 | ø 150 | Giro del baño | Alta | Control secundario de diámetro |
| T09-D04 | ø 150 | Giro del estar | Alta | Control secundario de diámetro |
| T09-D05 | 90 | Cadena superior del baño, izquierda | Alta | Candidato horizontal |
| T09-D06 | 40 | Cadena superior del baño, derecha | Alta | Candidato horizontal |
| T09-D07 | 120 | Achurado central del baño | Alta | Candidato horizontal de zona de uso |
| T09-D08 | 80, lectura probable | Mismo achurado, sentido perpendicular | Media | Confirmar antes de usar |
| T09-D09 | 80 | Tramo junto al inodoro | Alta | Candidato horizontal |
| T09-D10 | 70 | Tramo sobre la proyección del inodoro | Alta | Candidato horizontal |
| T09-D11 | 90, lectura probable | Achurado previo a ducha | Media | Confirmar antes de usar |
| T09-D12 | 137.5 | Cota horizontal superior de logia | Alta | Candidato horizontal |
| T09-D13 | 90 | Cota horizontal inferior de logia | Alta | Extremos y soporte por confirmar |
| T09-D14 | 50 | Cota vertical de logia | Alta | Candidato vertical |

Las cifras sobre achurados describen zonas de uso; no convierten esas zonas en paredes. Las cotas de 70, 90 o 137.5 no se asignan automáticamente al ancho de una puerta. El punto decimal de 137.5 se conserva en la transcripción.

## Espesores que sí aparecen escritos

Hay **ocho instancias de “M.H.A. 15cm”**. El espesor explícito es 15 cm, equivalente a 0,15 m, solo para los paños identificados:

| ID | Localización | Referencia T08 |
|---|---|---|
| T09-E01 | Borde superior izquierdo | CL-M01 |
| T09-E02 | Borde superior derecho | CL-M01 |
| T09-E03 | Borde izquierdo, tramo superior D3 | CL-M02 |
| T09-E04 | Borde izquierdo, tramo D1 | CL-M03 |
| T09-E05 | Borde derecho exterior | CL-M04 |
| T09-E06 | Paño inferior entre D1 y D2 | CL-M10 |
| T09-E07 | Retorno exterior izquierdo del baño | CL-M07 |
| T09-E08 | Paño corto cocina-estar | CL-M18 |

Esta lectura no demuestra el espesor terminado de los otros tabiques ni permite sumar acabados supuestos. Tampoco establece todavía las caras y ejes de esos ocho paños.

## Códigos sin espesor acreditado

| Lectura del código | Instancias | Tratamiento |
|---|---:|---|
| TAB-8A F-90 | 1 | Conservar como código |
| TAB-1C F-15 | 10 | Conservar como código |
| TAB-1D F-15 | 7 | Conservar como código |
| TAB-?A F-120 | 1 | T09-R13: lectura candidata TAB-10A, aún ambigua |
| TAB-2A F-60 | 1 | Conservar como código |
| TAB-5 F-30 | 1 | Conservar como código |
| TAB-3A F-60 | 2 | Conservar como código |
| TAB-11A F-120 | 4 | Conservar como código |
| TAB-11B | 1 | No añadir un sufijo que no se lee |

Los 28 registros R01-R28 contienen sus posiciones individuales. La transcripción normaliza espacios y separadores para comparar códigos; `?` marca caracteres no confirmados. Los números de F-15, F-30, F-60, F-90 o F-120 **no se convierten en centímetros ni en espesor del tabique**. No se encontró en esta presentación un cuadro de composición y espesores aplicable a esos códigos de la planta T7.

## Superficies y búsqueda complementaria

T09-A01/A02/A03 conservan las tres menciones del encabezado de p20: 76,66 m² EDIFICADO, 0,00 m² TERRAZA y TOTAL 76,66 m². T09-A04 conserva 76,80 m² dentro de la planta. Son datos documentales, no un cálculo de superficie. La discrepancia de 0,14 m² y la diferencia entre edificada y útil siguen pendientes en T13.

Las plantas de Torre A y B, p15-p18, ayudan a ubicar el T7 en el edificio. No se encontró en ellas una cadena general de cotas legibles que cierre la geometría exacta de p20. P19 corresponde al T6 y p29-p30 a casas diferentes; no se trasladan sus medidas al T7.

P22-p24 describen sistemas y canalizaciones. En p23 se leen **PERFILES 150 MM** y **DESCARGA SANITARIA 110 MM**, registrados en T09-B01/B02. Son dimensiones de componentes de un detalle Galaxy DS49; no documentan por sí mismas el espesor terminado de los tabiques del T7.

El esquema de p24 contiene una cota horizontal de lectura probable **267,5**, T09-B03, y otras cotas parciales, T09-B04. Su unidad general, altura y vinculación al T7 no se confirmaron. La imagen embebida tiene texto reflejado: los recortes de lectura se reflejan horizontalmente y esa transformación queda registrada. Ningún dato de este esquema se adopta como ancho o altura de la vivienda.

La búsqueda no resolvió largos y anchos generales de recintos, ancho de todos los vanos, alturas interiores, espesores de losa, antepechos ni profundidad real de terraza. Eso no impide continuar con T10 y medir la consistencia de los controles disponibles; cualquier dimensión inferida deberá quedar distinguida de una medida documentada.

## Confianza, coordenadas y siguiente paso

Hay 53 registros de lectura alta, cuatro de lectura media (D08, D11, R13 y B03) y uno de lectura baja (B04). La unidad de las 14 cotas locales sigue siendo inferida incluso cuando su cifra se lee bien. Los 12 pendientes funcionales de T08 permanecen abiertos; T09 no los cierra.

Las cajas de p20_planta, p23_obj210 y p24_obj222 se expresan en píxeles de sus imágenes nativas. Las cajas de p20_pagina se expresan en puntos PDF desde arriba a la izquierda; el recorte se obtiene de la página renderizada a factor 3. Todas se refieren a textos o detalles para lectura, no a extremos de medición ni caras de muro. Los giros y reflejos afectan únicamente a los recortes de evidencia.

`length_m_if_unit_accepted` muestra una conversión aritmética condicional, por ejemplo 150 cm → 1,50 m. No es una calibración del raster. `metric_transform` permanece nulo y los 58 registros tienen `model_geometry_allowed: false`.

T10 deberá seleccionar extremos geométricos independientes, contrastar referencias horizontales y verticales, separar controles de ajuste y comprobación, fijar origen y ejes y registrar desviaciones. Los círculos de giro son controles secundarios; las lecturas de confianza media y los componentes genéricos no deben ser la única base del ajuste.

Para regenerar, usar `python scripts/build-t09-inventory.py` desde la raíz. Requiere pypdf, Pillow, las referencias T07 y el PDF original en la carpeta superior. Usa Arial de Windows para las láminas; en otro entorno indicar `--font /ruta/a/fuente.ttf` con soporte de español y diámetro. La huella de la fuente utilizada queda registrada para reproducir el aspecto de las láminas. Consultar [VALIDACION_T09.md](../../docs/VALIDACION_T09.md).
