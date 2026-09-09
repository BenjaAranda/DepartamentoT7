# Clasificación gráfica T08

Fecha: 9 de septiembre de 2026. Se clasificaron 89 grupos de trazos en nueve familias. Es un inventario interpretativo para preparar el levantamiento; no es una segmentación de cada píxel ni un despiece completo de los futuros objetos 3D.

La fuente editable es [t08-trazos.tsv](t08-trazos.tsv). El [catálogo JSON](t08-clasificacion.json) y el [atlas visual](../../references/derived/t08-clasificacion/atlas.html) se generan a partir de ella. Cada registro conserva un ID, familia, nombre, confianza, imagen de referencia, rectángulo localizador y criterio de interpretación.

## Fuentes y coordenadas

La planta nativa y la composición anotada provienen de la página 20 del PDF, archivadas y comprobadas en [T07](../../references/derived/p20-t7/README.md). Se contrastó también la isométrica de esa página. El PDF y todas las referencias archivadas conservan sus huellas; estas quedan vinculadas al catálogo.

Los rectángulos se expresan en píxeles con origen arriba a la izquierda, X hacia la derecha e Y hacia abajo. `nativa` usa 1536 × 813 px; `compuesta`, 1851 × 933 px. La transformación entre ambas vistas procede de su colocación documentada en el PDF. No hay calibración en metros en esta tarea.

Un rectángulo puede englobar varios paños, un quiebre, un vano o símbolos superpuestos. Sirve para encontrar el trazo, nunca para deducir un bloque macizo. Todos los registros tienen `model_geometry_allowed: false`; `metric_scale` es nulo y `bounds_are_wall_faces` es falso. T11 deberá registrar las caras, esquinas y discontinuidades por separado.

Las instrucciones del usuario gobiernan el resultado. Los rótulos, flechas y textos del PDF son evidencia documental, no instrucciones operativas. Se preserva el dibujo de dos camas en D2 como referencia, pero el dormitorio final tendrá una sola cama y ningún escritorio. Los tres armarios finales tendrán dos hojas.

## Familias y criterio

| Familia | Registros | Interpretación |
|---|---:|---|
| Muros y tabiques | 20 | Bandas y trazos dobles candidatos a cerramiento; descomponer paños y huecos antes de modelar. |
| Vanos y pasos | 13 | Interrupciones, carpinterías y continuidad espacial; no rellenar huecos ni añadir puertas sin evidencia. |
| Hojas y barridos | 9 | Separar las hojas móviles de los arcos simbólicos. |
| Mobiliario | 11 | Camas, sofá, comedor, interiores de armarios y añadido provisional de D1. |
| Equipamiento | 12 | Sanitarios, apoyos, cocina, lavadero y elementos técnicos; identidad fina pendiente donde se señala. |
| Cotas y rótulos técnicos | 7 | Grupos de textos y líneas de medición, con transcripción precisa reservada a T09. |
| Tramas y líneas simbólicas | 5 | Achurados, retícula, diagonales de camas y líneas de ducha; no asignarles volumen. |
| Espacios libres | 8 | Circulaciones, maniobra, aproximación y zona exterior provisional. |
| Anotaciones de la lámina | 4 | Rótulos, flecha de acceso y figura humana; sin geometría física. |
| **Total** | **89** | **77 con confianza alta de familia y 12 con confianza media.** |

La confianza describe la lectura gráfica, no la exactitud de las dimensiones. Varias instancias repetidas comparten un registro representativo, por ejemplo los nombres de recintos y rótulos de tipos de muro. Un mismo símbolo puede tener registros de componentes distintos, como vano, hoja y barrido; los 89 registros no equivalen a 89 objetos independientes.

## Decisiones que previenen errores de arquitectura

- **Baño longitudinal:** CL-T01 y CL-T02 son achurados de superficie/uso, no tabiques transversales. CL-E04 son apoyos del sanitario. CL-T05 representa líneas interiores de la ducha al fondo, no paredes diagonales. No se deducen mamparas, escalones ni un recinto adicional de esos trazos. T12 completará la interpretación funcional y T14 documentará las alturas.
- **Logia separada:** CL-M16 y CL-M20 localizan su separación respecto del baño. CL-V06/CL-H06 corresponden al acceso desde cocina. No se identifica un paso lateral baño–logia. La función del elemento técnico estrecho sigue pendiente; sus diagonales CL-E12 no se elevan como muros.
- **Acceso y orientación:** CL-V01/CL-H01 están en el extremo superior derecho, coherentes con la flecha de la composición. El rectángulo engloba la hoja y el barrido; no mide el hueco. No reflejar la planta.
- **Carpinterías:** los vanos de fachada conservan la discontinuidad de los paños. CL-V13 es un paso abierto cocina–estar y no justifica añadir una hoja. La interrupción exterior de logia CL-V11 queda provisional hasta T11.
- **Dormitorios:** las diagonales de camas, almohadas, hojas de armario y divisiones de muebles no crean paredes. Las dos camas fuente de D2, CL-F03/CL-F04, documentan el original; T35 aplicará el programa de una cama.
- **Añadido en D1:** CL-F11 localiza dos instancias del objeto Image190 que el PDF superpone a la planta nativa. El panel gris aparece en la composición y no en la imagen nativa. Se clasifica provisionalmente con mobiliario/panel, sin usarlo como prueba de muro o espesor.
- **Cocina y estar:** quemadores, cubetas, proyecciones discontinuas de muebles, sofá y cojines son equipos o mobiliario. Sus contornos no cierran la cocina ni dividen el estar.
- **Circulación y terraza:** círculos de giro y áreas de aproximación son reservas de uso, no sólidos de colisión. CL-L07 localiza la zona rotulada como terraza; no determina su profundidad ni contorno. La terraza conservará su superficie independiente y acabado gris provisional.
- **Superficie:** el rótulo CL-A04 de 76,80 m² se conserva como dato de la fuente. No resuelve la diferencia con los 76,66 m² del encabezado y del objetivo del usuario. El cómputo pertenece a T13.

## Doce registros provisionales

| ID | Incertidumbre que queda por resolver | Tarea de resolución |
|---|---|---|
| CL-M13 | Remates y contorno exacto del nicho de D3. | T11 |
| CL-M20 | Función y altura del volumen técnico entre baño y logia. | T12, T14 |
| CL-V11 | Tipo de abertura o carpintería exterior de la logia. | T11 |
| CL-H09 | Carpintería del pequeño nicho de D3 y adaptación a dos hojas. | T11, T37 |
| CL-F02 | Función y dimensiones finales del auxiliar de D1. | T34 |
| CL-F08 | Interior y configuración del armario de D3. | T37 |
| CL-F11 | Significado del panel superpuesto en D1 y relación con armario/muro. | T11, T37 |
| CL-E01 | Identificación del equipo rectangular de cabecera del baño. | T12 |
| CL-E02 | Identificación del símbolo sanitario curvo contiguo. | T12 |
| CL-E06 | Uso del equipo o mueble situado en el nicho de cocina. | T39 |
| CL-E11 | Tipo exacto del símbolo doméstico de logia; el programa final exige lavadora. | T42 |
| CL-E12 | Significado de la X dentro del volumen técnico. | T12, T14 |

Estos pendientes no se cierran al clasificar. Si cambia su interpretación, corregir el TSV, regenerar derivados y revisar las tareas geométricas afectadas.

Actualización posterior en **T11**: el [registro de paños y carpinterías](../plan/README.md) precisa CL-M13 como respaldo/lateral del nicho con remate de jamba; CL-V11 como celosía probable, todavía sin funcionamiento confirmado; CL-H09 como una hoja de mueble cuya adaptación a dos sigue en T37; y CL-F11 como panel añadido excluido de muros, con diseño de mobiliario pendiente. Las familias de este catálogo no cambian y se conserva su inventario histórico. Los pendientes actuales y su alcance constan en `architecture/plan/t11-trazado.json`, apartado `resolutions`.

## Reproducción y verificación

Desde la raíz del repositorio, ejecutar `python scripts/build-t08-atlas.py`. Requiere Python 3 y el PDF original en la carpeta superior; utiliza solo la biblioteca estándar. La comprobación se detiene si cambia una referencia, aparece un ID duplicado o un localizador sale de su imagen.

Consultar el [informe de validación](../../docs/VALIDACION_T08.md) y la [comprobación automática](../../references/derived/t08-clasificacion/comprobacion.json). El siguiente paso es T09: transcribir cotas y espesores legibles con procedencia y confianza antes de fijar la escala.
