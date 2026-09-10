# T12: baño y logia

Se confirma la distribución del núcleo húmedo de la página 20: **un baño longitudinal, ducha al fondo y logia separada con acceso desde cocina**. El levantamiento reutiliza las caras T11 sin mover muros, crear particiones o recalibrar la planta.

El baño tiene un acceso, O05, cuya puerta P05 abre hacia la circulación superior. Su ventana O10 está al fondo, junto a la ducha; no se convierte en una salida. La logia se accede por O06 desde cocina. Sus bordes W20A/W20B y la franja técnica intermedia separan ambos recintos en toda la longitud compartida. O11 conserva la celosía probable sin atribuirle una puerta exterior.

## Contornos y continuidad

El contorno del baño se descompone en tres bandas interiores conectadas, que describen cambios laterales de ancho. No son tres habitaciones. Su longitud trazada es aproximadamente **5,284 m**, con anchos de **1,590 m**, **1,502 m** y **1,402 m**. Estas medidas derivan de T10/T11 y conservan su incertidumbre; no son nuevas cotas certificadas.

Los contornos se cierran analíticamente en la cara interior de los vanos para describir cada región. Esos cierres no se añaden como muros o colliders. El recinto técnico no tiene un acceso dibujado: sus diagonales simbolizan el interior, no estructuras que deban modelarse.

Dos guías sin anchura cruzan O05 hacia la ducha y O06 hacia logia. No intersectan las huellas de muro. La primera atraviesa ambos achurados, comprobando que esas superficies no se han convertido en barreras. Las guías **no prueban el paso de una cápsula, persona o silla de ruedas**, ni sustituyen las pruebas de muebles, puertas y apoyos de E05/E06.

## Lectura funcional

| ID | Elemento o área | Interpretación y decisión |
|---|---|---|
| EQ01 | Caja de cabecera del baño | Lavadora de carga superior probable por la caja y el panel posterior en isométrica; sin rótulo confirmatorio. No convertirla en muro ni fijar una segunda lavadora en baño. El programa final sitúa la lavadora en logia, T42. |
| EQ02 | Lavamanos | Cubeta curva con grifería, reconocible en las dos vistas. Conservar su ubicación; alturas, apoyo y espacio inferior se definirán en T14/T38. |
| EQ03 | Inodoro | Taza y estanque en el tramo central; una sola unidad. La transferencia queda a su izquierda en planta. |
| EQ04 | Barras del inodoro | Apoyos visibles, sin convertir sus líneas o proyecciones en tabiques. Estados plegados, alturas y barridos pendientes de equipamiento. |
| SH01 | Ducha | Al fondo, bajo el achurado inferior y frente a O10. Las líneas convergentes y el desagüe son equipamiento/piso. La línea frontal no acredita mampara, pared o escalón. |
| UA01 | Achurado central | Superficie de uso/maniobra, probablemente vinculada a la aproximación al lavamanos. Cifras 120 y 80 coherentes con el dibujo; no es una segunda ducha. |
| UA02 | Achurado previo a ducha | Superficie de aproximación/uso. La lectura 90 es coherente con su longitud. No divide el baño. |
| UA03 | Giro del baño | Reserva rotulada 150, con centro y diámetros de T10. La elipse observada no intersecta huellas de muro; falta comprobar equipos y uso real. |
| UA04 | Transferencia al inodoro | Reserva junto a la taza, apoyada por la cota 80 y las barras. La cota 70 no es ancho de puerta. Los límites longitudinales de esta reserva siguen siendo interpretativos. |
| LG01 | Lavadero | Cubeta de servicio en logia, independiente del lavamanos del baño. Modelo y dimensiones finales en T42. |
| LG02 | Dos cuerpos circulares | Equipo de servicio de identidad no confirmada; compatible con cuerpos cilíndricos, sin leyenda suficiente. No se acepta como prueba de una lavadora dibujada. Resolver al amueblar logia. |
| SV01 | Volumen técnico | Contorno confirmado, función de instalaciones probable. Conservar paredes laterales opacas y excluir la X de la geometría. No inventar tuberías, registros o accesos. |

Las unidades locales de 120/80/90/150 siguen siendo **centímetros inferidos**, coherentes con T09/T10. La coincidencia gráfica de esas lecturas no convierte los achurados en dimensiones reglamentarias o superficies útiles independientes. Su función de reserva está respaldada por las vistas; su denominación normativa exacta no se acredita en esta tarea.

El símbolo de ducha ocupa aproximadamente `(u, v) = (855,5; 671,5)` a `(1000,5; 780,2)` en la planta nativa. Ese localizador no representa una pared ni prueba que toda la anchura del baño sea un plato de ducha. Se conserva la continuidad de piso requerida para una ducha accesible; pendientes, impermeabilización, equipos y cotas verticales se definirán en T14/T38.

## Fuentes y límites

Se compararon la planta y la isométrica originales de p20. Las páginas 22/23 aportan ejemplos Galaxy DS49 con celosía y canalizaciones rotuladas; sirven de contexto de función. No se transfieren al T7 sus medidas, tuberías, estructura o distribución.

La búsqueda de texto extraíble en las 42 páginas no encontró un rótulo «lavadora» que identifique inequívocamente EQ01 o LG02. La búsqueda no equivale a OCR exhaustivo de las imágenes. Las identidades probables permanecen explícitas y no bloquean la confirmación de que son equipos, no tabiques.

Quedan pendientes alturas y detalles de ducha/apoyos, identidad exacta de EQ01/LG02, instalaciones internas del volumen técnico y apertura de celosía. No se declara cumplimiento normativo, accesibilidad física terminada, recorrido 3D o ausencia de penetraciones con muebles futuros. Las superficies 76,66/76,80 m² siguen sin calcular ni resolver; **T13 es la siguiente tarea**.

## Archivos

- [t12-interpretacion.json](t12-interpretacion.json): entrada de autoría; los contornos usan nombres de coordenadas T11, sin duplicar medidas de muros.
- [t12-topologia.json](t12-topologia.json): contornos derivados en píxeles/metros, zonas funcionales, puertos, guías, comprobaciones y pendientes.
- [Evidencias visuales](../../references/derived/t12-bano-logia/README.md): comparación planta/isométrica, símbolos del baño y lectura de logia/servicio.
- [Validación T12](../../docs/VALIDACION_T12.md): alcance y resultados.

Regenerar con `scripts/build-t12-topology.py`, usando Python con NumPy, Pillow y pypdf. El generador verifica las huellas del PDF, las referencias T07, T10 y T11 antes de derivar resultados. Las cajas de símbolos son localizadores y no se exportan como sólidos de equipamiento. Si cambia un muro, corregir T11, revisar esta interpretación y actualizar la dependencia de revisión de manera explícita.
