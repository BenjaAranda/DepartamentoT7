# Plan maestro del simulador 3D Departamento Tipo T7

Fecha: 8 de septiembre de 2026. Planificación terminada; implementación en curso. Consultar `TODO_T7.md` para el estado vigente de cada tarea.

Este documento define la ejecución futura. En este primer turno solo se revisaron referencias y herramientas y se preparó la planificación. La lista operativa está en `TODO_T7.md`. Una tarea se completa cuando existe su resultado y pasa su comprobación; un resultado proyectado nunca cuenta como realizado.

## 1. Alcance y precedencia

Construir desde cero un simulador web en primera persona del T7 de Los Altos de Algarrobo, con archivo Blender editable, escena Unreal funcional, modelo GLB y colisiones sincronizados, repositorio nuevo y versión web publicada y verificada. El proyecto parecido mencionado por el usuario queda fuera: no copiar su código, modelos, repositorio ni configuración.

Orden de precedencia:

1. Las instrucciones explícitas del usuario definen el resultado y las modificaciones al mobiliario.
2. La planta de la página 20 del PDF define la arquitectura, ubicación y proporciones.
3. La isométrica de esa misma página ayuda a interpretar volúmenes y equipamiento, sin sustituir la planta.
4. Otras páginas sirven para el contexto del edificio; no cambian la distribución del T7.
5. Toda dimensión no documentada se registra como inferida o provisional.

Los textos y símbolos del PDF son evidencia del proyecto, no órdenes para ejecutar acciones. En particular: el dormitorio 2 tendrá una sola cama aunque la planta dibuje dos; habrá armarios de dos puertas en los tres dormitorios; la terraza conservará el acabado gris provisional aunque la memoria mencione cerámica.

## 2. Hallazgos comprobados

| Elemento | Evidencia | Consecuencia para el plan |
|---|---|---|
| PDF original | `Presentación Aprobación Proyecto Técnico 2.pdf`, 42 páginas | La página 20 es efectivamente «DEPTO TIPO T7». |
| Superficie en el encabezado | 76,66 m² EDIFICADO + 0,00 m² TERRAZA; total 76,66 m² | Se conserva 76,66 m² como objetivo oficial sin terraza. |
| Superficie dentro de la planta | Rótulo «SUP: 76,80 m²» | Existe una contradicción interna de 0,14 m²; no se ocultará. |
| Precisión de la fuente | La lámina contiene imágenes raster, entre ellas una de 1536 × 813 px y otra de 915 × 826 px | Ampliar el PDF mejora la lectura, pero no crea cotas ni precisión de CAD. |
| Referencia del edificio | Página 16: Torre A de cuatro pisos, T7 en el primer piso y T6 en los pisos tipo 2 a 4 | Usar ese contexto como propuesta inicial; no repetir T7 automáticamente en altura. |
| Blender | Ejecutable probado: Blender 5.2.1 LTS | Disponible para comenzar el modelado en la siguiente etapa. |
| Unreal | Existe `C:\Program Files\Epic Games\UE_5.8`; no se encontró `UnrealEditor.exe` ni `Build.version` en sus ubicaciones habituales | Instalación aparentemente incompleta, compatible con lo indicado por el usuario. Comprobar de nuevo al llegar a esa etapa. |
| Desarrollo | Git 2.54.0, Node 26.8.1; npm disponible | Fijar dependencias compatibles al iniciar, sin asumir que todo paquete acepta esa versión de Node. |
| Espacio de trabajo | Inicialmente solo estaba el PDF; no había proyecto ni repositorio en esta carpeta | Preparar un proyecto independiente en una subcarpeta nueva. |
| GitHub | Cuenta indicada: BenjaAranda; no se comprobó autenticación ni se crearon recursos | Verificar acceso y disponibilidad del nombre al ejecutar la etapa de configuración. |

Huella SHA-256 del PDF revisado: `ad8e0871ed6afb7117e2dafa80bc28ad90b3c845709dc268ba01fcd12259aeec`.

### Resolución de superficie y precisión

El usuario describe 76,66 m² como superficie interior; el PDF la llama edificada. No se puede afirmar todavía que la superficie libre entre caras terminadas también mida 76,66 m².

Se elaborarán tres mediciones distintas: superficie según el perímetro de cómputo documentado, superficie útil por recinto y superficie provisional exterior/terraza. La terraza tendrá su polígono independiente y quedará excluida de las dos primeras. Un rótulo de 76,66 m² en la pantalla no será una validación geométrica.

Primero se contrastarán cotas explícitas y espesores legibles. Los círculos de giro rotulados y otras medidas sirven como controles secundarios, nunca las dimensiones supuestas de una cama o de una baldosa. Se registrarán referencias horizontales y verticales y puntos de comprobación que no participen en el ajuste.

Si quedan cotas incompatibles o no se puede determinar qué perímetro corresponde a 76,66 m², se podrá avanzar con un modelo provisional marcado, pero no cerrar la validación dimensional. Será necesario resolver esa diferencia con la documentación disponible o una aclaración puntual. No se ensancharán recintos, modificarán vanos ni escalará todo indiscriminadamente para producir el número esperado.

La fidelidad exacta solo podrá declararse donde haya evidencia suficiente. Las alturas, dimensiones ilegibles y límites de terraza no se presentarán como datos oficiales.

## 3. Solución técnica propuesta

Se usarán Blender y Unreal, con una versión web directa derivada del mismo modelo. Esta elección permite desarrollar un recorrido accesible por URL sin depender de que Unreal esté ejecutándose para cada visita.

| Capa | Función y resultado |
|---|---|
| Datos de arquitectura | Medidas, ejes, muros, recintos, vanos y restricciones en metros, con identificadores y procedencia. |
| Blender + Python | Fuente editable de geometría, mobiliario, materiales, pivotes y proxies de colisión. Construcción y exportación reproducibles. |
| GLB de intercambio | Exportación sin compresión específica de navegador para comprobar e importar a Unreal. |
| GLB de distribución | Derivado optimizado para el navegador; conserva dimensiones, IDs necesarios y animaciones de puertas. |
| Unreal Engine | Proyecto propio con importación del modelo, iluminación, colisiones y recorrido real a 1,60 m. Prueba funcional obligatoria antes de declarar completo el trabajo. |
| Web | React, TypeScript, Three.js/React Three Fiber, Drei y Rapier; interfaces en español y física separada de la interfaz. Versiones fijadas con archivo de dependencias. |
| Optimización | glTF Transform; probar Meshopt y KTX2 solo donde exista soporte y ganancia medida. No comprimir el GLB de Unreal con extensiones sin validar compatibilidad. |
| Entrega | Proyecto y sitio nuevos mediante Sites; repositorio independiente en GitHub; controles automáticos y evidencia de la versión publicada. |

Unreal documenta importación de escenas glTF mediante Interchange, que se probará primero con una pieza de escala, un muro y una puerta antes de importar el departamento completo. [Documentación de Interchange](https://dev.epicgames.com/documentation/en-us/unreal-engine/importing-assets-using-interchange-in-unreal-engine).

**Alternativa si el navegador debe ejecutar específicamente la experiencia de Unreal:** Pixel Streaming, que transmite una aplicación Unreal ejecutada en un equipo o servidor con GPU. Requiere estudiar alojamiento, sesiones, latencia y disponibilidad; un sitio estático por sí solo no aloja ese proceso. La ruta base de este plan es Unreal local más web GLB, y no se anunciará la web GLB como si utilizara el motor Unreal. No se contratarán servicios para streaming durante la planificación. [Pixel Streaming de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/pixel-streaming-in-unreal-engine).

## 4. Convenciones y sincronización

### Unidades y orientación

- Sistema de autoría: Blender en metros, escala de unidad 1; X hacia la derecha del plano, Y hacia arriba del plano, Z vertical. No atribuir norte geográfico al borde superior sin evidencia.
- Origen propuesto: esquina interior inferior izquierda del dormitorio 1, sobre el piso terminado. Guardar ese punto en la referencia calibrada.
- Web/glTF: una unidad equivale a un metro; Y vertical. Conversión prevista desde Blender: `(x, y, z) → (x, z, -y)`.
- Unreal usa centímetros por defecto. La equivalencia física será 1 m = 100 unidades Unreal, y POV = 160 cm; no se fingirá que sus unidades nativas son metros. El adaptador definirá la orientación y la conversión una sola vez y comprobará que el importador no aplique una segunda conversión. [Unidades de Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/units-of-measurement-in-unreal-engine).
- Se probarán una regla de 1 m, una marca de altura de 1,60 m y puntos asimétricos en acceso, dormitorio 3 y logia, para detectar escala incorrecta, rotación o espejo.
- Altura ocular medida desde el piso terminado hasta el centro óptico, independiente del centro y tamaño de la cápsula física. Sin oscilación vertical durante la medición.

### Fuente y exportación

La tabla arquitectónica gobierna las medidas; Blender gobierna la geometría y los activos visuales. Una corrección de medidas se registra primero en la tabla y se aplica a Blender. Los elementos generados se separan de los detalles manuales para que regenerar arquitectura no borre mobiliario o acabados.

Cadena de actualización: datos → Blender guardado → GLB de intercambio + colisiones → importación Unreal y GLB web optimizado → verificaciones → publicación. No recolocar muros solamente en el navegador ni corregir Unreal de forma que se pierda el cambio en la siguiente importación.

Cada lote tendrá un manifiesto con revisión del modelo, huellas del archivo Blender, GLB, colisiones y parámetros, versión de herramientas y resultado de validación. El sitio cargará un conjunto atómico con nombres versionados para impedir que una caché combine geometría nueva con colisiones antiguas. El registro de publicación asociará ese manifiesto al commit de GitHub y a la versión de Sites.

Identificadores estables para recintos, muros, vanos, hojas y colliders. Las hojas móviles conservan pivote en la bisagra; el modelo visual y el collider utilizan el mismo ángulo y transformación. Muros estáticos segmentados alrededor de los vanos: una caja envolvente del conjunto no puede cerrar todas las puertas accidentalmente.

## 5. Especificación espacial y mobiliario

| Zona | Modelado exigido | Comprobación particular |
|---|---|---|
| Acceso y circulación | Acceso en el extremo superior derecho; registrar muro de soporte, bisagra y arco según planta; conexión al pasillo común | Entrada y salida a todas las habitaciones con la puerta operable desde ambos lados. |
| Dormitorio 1 | Cama matrimonial adosada al muro indicado, sin penetración; armario empotrado de dos hojas; veladores y TV frente a la cama | Ajustar medidas de muebles al espacio real; cama contra muro con contacto controlado, no escondida dentro de él. |
| Dormitorio 2 | Exactamente una cama, un velador y armario de dos hojas; sin escritorio ni cama adicional | La reducción respecto al mobiliario dibujado no modifica la arquitectura. |
| Dormitorio 3 | Una cama individual, un velador y armario de dos hojas | Mantener vano, apertura y circulación hacia la cama. |
| Todos los armarios | Carcasa, hojas separadas, tiradores, zócalo, coronación, jambas y remates del color del muro | Inspección frontal, lateral y puertas abiertas; no crear huecos arquitectónicos inexistentes para simular un empotrado. |
| Baño | Recinto longitudinal único, ducha accesible al fondo, sanitarios y apoyos; mantener espacios de transferencia y giro dibujados | Tramas, círculos y bordes de equipamiento no son tabiques; no imponer mamparas o peldaños que bloqueen la ducha. |
| Cocina | Encimera, muebles, lavaplatos, cocina/horno, campana y refrigerador adaptados a la huella disponible | Equipos y aperturas fuera de la circulación principal; separación real del baño. |
| Estar | Sofá y TV enfrentados directamente, mesa solo si cabe | Línea de visión libre y paso continuo al comedor y acceso. |
| Comedor | Mesa y sillas, respetando aproximación y espacio señalado en planta | Comprobar con sillas recogidas y en posición de uso. |
| Logia | Recinto separado del baño, con lavadero y lavadora, acceso y espacio de operación | No unirla al baño ni colocar equipos contra el barrido de su puerta. |
| Terraza | Superficie gris provisional, contorno y cota identificados como provisionales donde falte evidencia | Excluida de 76,66 m²; no crear una puerta exterior donde el plano solo tenga ventana. |
| Edificio | Pasillo común, losa y cielo, tres niveles superiores de contexto y vecinos opacos, según la Torre A como hipótesis inicial | No dejar el departamento flotando ni permitir ver al vecino por muros ausentes. No duplicar la distribución T7 en pisos T6. |
| Decoración | Alfombras, plantas, lámparas, cuadros, cojines y accesorios | Añadir al final; revisar geometría completa y circulación después de cada conjunto. |

Se inventariarán todos los vanos, espesores, retranqueos y esquinas antes de extruir muros. Cada trazo se clasificará como muro, vano, hoja, equipamiento, mobiliario, cota, trama o área libre. El volumen del baño se comprobará especialmente con planta e isométrica antes de amueblar.

La propuesta de acabados es sobria: muros claros, cerámica como referencia del T7, carpinterías discretas y materiales PBR. Las luces se colocarán después de validar aberturas; la iluminación no ocultará falta de techos, huecos o caras ausentes.

## 6. Recorrido e interacción

El simulador abrirá con la escena como actividad principal, instrucciones breves y carga con progreso. Controles de caminar y mirar con teclado/ratón; pausa que libera el puntero, ayuda, reinicio al acceso y pantalla completa. Controles táctiles sencillos para recorrer desde móvil, con calidad adaptable. Planta ortográfica e isométrica disponibles como modos de inspección.

El personaje tendrá cápsula cinemática, gravedad, detección barrida y paso de física fijo. Radio inicial de referencia 0,25 m, sujeto a prueba frente a los anchos libres; no reducirlo hasta convertir al usuario en un punto para ocultar errores arquitectónicos. Velocidad inicial 1,2 m/s y ausencia de salto durante el recorrido, ajustables como parámetros de experiencia. La altura ocular permanece en 1,60 m.

El controlador debe deslizarse por muros, cruzar umbrales válidos y detenerse en paredes, vidrios cerrados, muebles y límites. Se comprobarán esquinas, juntas de suelo y marcos a velocidad normal y con cuadros lentos. Las hojas deben detenerse o revertirse si encuentran al jugador; nunca empujarlo a través de una pared. [Controlador de personajes de Rapier](https://rapier.rs/docs/user_guides/javascript/character_controller/).

Si la terraza provisional no tiene delimitación respaldada por la referencia, se delimitará explícitamente el área recorrible del prototipo y se documentará el límite provisional. Una recuperación desde una posición inválida será una defensa adicional; no sustituye al suelo continuo ni permite aprobar una caída.

Las vistas de inspección pueden ocultar techo y contexto por capas. Al volver a primera persona se restauran techo, vecinos y límites opacos, conservando una posición válida. Puertas y armarios tendrán interacción suficiente para verificar barridos; no se requiere simular ciclos reales de electrodomésticos.

## 7. Etapas, dependencias y entregables

| Etapa | Trabajo | Depende de | Resultado para cerrar |
|---|---|---|---|
| E00 | Referencias, herramientas y planificación | Solicitud | Este plan y to-dos revisados. Completada. |
| E01 | Proyecto, repositorio y sitio nuevos; seguimiento | E00 | Estructura independiente, acceso a GitHub comprobado, primer estado versionado y sitio registrado sin anunciarlo como terminado. |
| E02 | Interpretación de planta y calibración | E00 | Inventario de trazos y cotas, plano anotado, perímetro de cómputo, discrepancias resueltas o explícitas. |
| E03 | Datos y exportación mínima | E01 + mediciones base de E02 | Prueba de 1 m, orientación, puerta y collider reproducible. |
| E04 | Arquitectura sin muebles y contexto | E02 + E03 | Blender estructural, superposición ortográfica e isométrica; control dimensional aprobado. |
| E05 | Primer recorrido con colisiones | E04 | Todas las estancias accesibles y vuelta al acceso, sin atravesar, caer ni atascarse. |
| E06 | Mobiliario por recinto | E05 | Inventario exacto, barridos e interferencias comprobados recinto por recinto. |
| E07 | Acabados, iluminación y decoración | E06 | Escena legible y completa, nueva revisión de penetraciones y paso. |
| E08 | Integración completa en Unreal | E03 + E07 + instalación operativa | Proyecto Unreal guardado, importación íntegra, recorrido y comparación con Blender/GLB. |
| E09 | Web final y optimización | E07 + recorrido de E05 | Interfaz completa, activos optimizados, pruebas de carga y rendimiento. |
| E10 | Validación integral | E08 + E09 | Todos los requisitos con evidencia y sin defectos de entrega abiertos. |
| E11 | Compilación, GitHub y publicación | E10 | Misma revisión validada en repositorio y sitio, URL comprobada y entrega. |

Se avanza una tarea verificable a la vez. Si Unreal continúa instalándose, E02–E07 y la parte web de E09 pueden seguir; E08 permanece pendiente y no se declara completo el proyecto. Una comprobación que falla se corrige en su fuente y reabre las tareas dependientes afectadas, sin repetir pruebas ajenas al cambio.

No se fijan fechas de terminación ficticias antes de resolver las medidas y comprobar Unreal. Se informará el avance por hitos terminados y evidencia disponible.

## 8. Plan de validación y umbrales

Los umbrales siguientes son criterios de ingeniería propuestos, no una afirmación de precisión de la lámina. En E02 se registrará la incertidumbre de lectura. Si excede el umbral, se requiere una fuente mejor o se informa la limitación: no se relaja el criterio silenciosamente.

| ID | Prueba | Criterio de cierre | Evidencia prevista |
|---|---|---|---|
| V01 | Planta contra modelo | Cámara ortográfica registrada al plano, sin perspectiva, rotaciones arbitrarias ni deformación no uniforme. Comparar ejes, caras, esquinas y todos los vanos. | Superposición al 50 %, diferencias de contorno y tabla de puntos de control. |
| V02 | Medidas | Error objetivo ≤ 0,01 m en cotas verificables; dimensiones ilegibles marcadas pendientes. Informar error máximo, no solo promedio. | Informe de cotas y confianza por medida. |
| V03 | Superficie | Polígono de cómputo documentado con objetivo 76,66 m², diferencia objetivo ≤ 0,01 m²; suma útil por recinto por separado; terraza excluida. | Coordenadas y método reproducible; informe que distingue cálculo y dato oficial. |
| V04 | Escala y POV | Regla de 1 m con error de intercambio ≤ 0,001 m; cámara 1,600 m ± 0,005 m sobre piso en reposo en cada recinto; Unreal equivalente en cm. | Mediciones en Blender, web y Unreal. |
| V05 | Isométrica | Revisar desde al menos dos esquinas opuestas y una vista alineada a la referencia; todos los recintos y espesores reconocibles. | Capturas de arquitectura y de versión amueblada. |
| V06 | Interferencias | Cero penetraciones muebles-muros no justificadas; contactos previstos explícitos. Detección amplia por volúmenes y confirmación con geometría, tolerancia numérica ≤ 0,002 m. | Informe por ID y capturas de cualquier contacto aceptado. |
| V07 | Puertas y armarios | Verificar cerrado, mitad de apertura y abierto, además del barrido continuo; cero bloqueo de rutas obligatorias y cero empuje del jugador a través de muros. | Pruebas de ambas caras, estados y obstáculos. |
| V08 | Recorrido | Acceso → cada dormitorio, baño/ducha, estar, comedor, cocina y logia → acceso; pasillo común y terraza solo donde exista acceso real. Cero caídas, cruces de muro o atascos. | Rutas automatizadas mediante el controlador y recorrido manual completo. |
| V09 | Casos adversos | Chocar diagonalmente con esquinas y marcos, caminar contra vidrios y límites, simular FPS bajos, cambiar de pestaña, pausar y reanudar, abrir hojas junto al jugador. | Registro de resultados; ningún caso puede depender del botón de reinicio para aprobar. |
| V10 | Sincronización | Todos los activos pertenecen a la misma revisión; probar una modificación controlada y su propagación a GLB, colliders y Unreal. | Manifiesto, huellas, dimensiones y comparación de posiciones. |
| V11 | Inventario y arquitectura | Tres dormitorios; D2 una cama sin escritorio; armarios completos; baño longitudinal sin muros ficticios; logia independiente; vecinos y pisos presentes. | Lista por recinto y capturas. |
| V12 | Rendimiento | Objetivos iniciales: 60 FPS en escritorio de referencia y 30 FPS en móvil medio, después de carga; registrar hardware, resolución, calidad y tiempos de cuadro. | Medición sobre una ruta de 60 s, no estimación visual. |
| V13 | Carga | Presupuesto inicial web: activos esenciales ≤ 25 MB transferidos, escena completa ≤ 50 MB; escena utilizable objetivo ≤ 10 s en conexión controlada de 50 Mbps. Medir y ajustar calidad antes de comprometer esos valores. | Tamaños, tiempos de red/decodificación, prueba sin caché y memoria observada. |
| V14 | Navegadores e interfaz | Recorrido verificado en Chrome y Edge de escritorio; móvil real o emulado identificado como tal, con prueba táctil. Registrar lo que no se haya podido probar. | Capturas, controles operativos, carga, pausa, reinicio y recuperación de errores. |
| V15 | Entrega | Compilación limpia, activos sin errores de carga, mismo manifiesto en GitHub y URL final; acceso al enlace desde el contexto de uso previsto. | Informe de compilación, estado de despliegue exitoso y comprobación posterior. |

La accesibilidad se comprobará contra los espacios y equipamiento del plano y la usabilidad del recorrido. No se afirmará certificación normativa del departamento a partir del simulador.

## 9. Organización prevista

Carpeta del proyecto: `simulador-t7/` dentro del espacio actual, creada en T01. La base Sites se ubica en `simulador-t7/web/` desde T02: el inicializador exige una carpeta vacía y la raíz ya contiene la documentación. Blender, Unreal y los datos arquitectónicos permanecerán junto a `web/`. Repositorio propuesto: `BenjaAranda/los-altos-algarrobo-t7`, sujeto a disponibilidad. La propuesta de nombre no significa que exista.

| Carpeta | Contenido previsto |
|---|---|
| `docs/` | Este plan, to-dos, medidas, decisiones, requisitos y reportes. |
| `references/` | Referencias originales de trabajo y calibración; distinguir los documentos de autoría externa antes de incluirlos en una distribución pública. |
| `architecture/` | Tabla de muros, vanos, recintos, áreas, medidas, procedencia y parámetros. |
| `blender/` | Archivo maestro, materiales y exportadores reproducibles. |
| `unreal/T7/` | Proyecto Unreal, configuración, contenido e importador. |
| `assets/interchange/` | GLB de intercambio y proxies. |
| `web/public/models/` | Activos optimizados y manifiesto para el navegador. |
| `web/app/` y `web/components/` | Aplicación Sites, escena, controlador, interacción y controles. |
| `web/.openai/hosting.json` | Configuración del sitio; reutilizar el identificador registrado en T05. |
| `validation/` | Comparaciones, mediciones, informes de colisiones, rutas y rendimiento. |

El repositorio incluirá código, documentación, configuración y activos necesarios. T03 dejó Git local y LFS configurados: fuentes editables e intercambio binario en LFS; recursos de `web/public/` en Git normal; videos y paquetes grandes como entregables de versión. Las exclusiones, límites de trabajo y comprobaciones se detallan en `ALMACENAMIENTO.md` y `VALIDACION_T03.md`. T04 creó y vinculó el repositorio privado [BenjaAranda/los-altos-algarrobo-t7](https://github.com/BenjaAranda/los-altos-algarrobo-t7); sus identificadores y evidencia están en `GITHUB_REPOSITORY.json` y `VALIDACION_T04.md`. La cuota efectiva de LFS sigue por comprobar antes de la primera subida de binarios. No incluir el instalador de Unreal ni archivos del proyecto anterior.

Crear un tablero GitHub Projects vinculado al repositorio si la cuenta ofrece esa capacidad; trasladar allí los mismos IDs de tareas. El archivo TODO seguirá siendo la referencia local verificable. Crear un proyecto nuevo de código y sitio no requiere abrir otra tarea de conversación.

## 10. Publicación y continuidad

Al cerrar cada hito, actualizar to-dos, evidencias y cambios de alcance, y subir al repositorio nuevo. Publicar la versión de entrega únicamente después de E10 y de compilar la misma revisión. Las verificaciones intermedias pueden tener vistas previas identificadas como tales.

Registrar visibilidad del repositorio, acceso del sitio y dirección exacta al configurar los destinos. Un despliegue privado se identificará como privado. Usar la autorización de creación, actualización y publicación ya expresada por el usuario al ejecutar esas etapas; resolver solo permisos o decisiones que realmente falten.

T05 dejó registrado el sitio para `web/`, con acceso privado solo para el propietario, sin versiones guardadas ni despliegues. Su ID exacto está en `web/.openai/hosting.json`; `SITE_REGISTRATION.json` conserva la dirección prevista y `VALIDACION_T05.md` documenta la comprobación de acceso. Reutilizar este destino; la dirección prevista no acredita una publicación.

Después de publicar, comprobar la URL desplegada y su manifiesto, carga del GLB, colisiones, acceso a recintos y ausencia de errores críticos. Conservar una revisión recuperable. Una corrección posterior modifica la fuente, reexporta lo afectado, repite los controles pertinentes y actualiza tanto GitHub como el sitio; no editar únicamente la copia publicada.

Entregables finales: enlace web validado; repositorio nuevo; Blender editable; proyecto Unreal probado; GLB y colliders de la misma revisión; comparación ortográfica e isométrica; informe de superficie, escala y POV; prueba de recorrido e inventario; instrucciones breves de uso y de actualización. Solo entonces se marca el proyecto completo.
