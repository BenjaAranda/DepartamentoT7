# T11: muros, esquinas, vanos y puertas

Fecha: 9 de septiembre de 2026, America/Santiago. Resultado: **T11 completada como registro 2D de trabajo**, con medidas inferidas y detalles pendientes identificados. No cierra la validación arquitectónica de E02 ni acredita un modelo 3D.

Se registraron las caras y ejes de 40 paños, con la transformación métrica común de T10. Los 20 grupos de muros de T08 quedan cubiertos sin extruir sus localizadores. Hay 13 vanos/pasos, seis puertas de recinto con soporte, ancho leído, bisagra y giro, y cinco hojas de mobiliario que explican los tres grupos de armarios de la fuente.

## Comprobación

| Revisión | Evidencia y resultado |
|---|---|
| Cobertura de fuente | 20/20 grupos de muros, 13/13 grupos de vanos y 9/9 grupos de hojas T08 vinculados al registro. |
| Caras | Lectura ampliada sobre planta nativa; 27 muestras de caras contrastadas con perfiles de intensidad. Máximo residuo seleccionado: 0,633 px, aproximadamente 5,36 mm con T10. Este control local no certifica todas las caras ni la precisión global. |
| Encuentros | Ocho grupos de retranqueos/cambios de espesor conectados mediante caras compartidas; 34 contactos entre paños. Sin encuentros reducidos a un único punto en el borde combinado. |
| Esquinas | 106 vértices de borde en ocho anillos cerrados, con IDs y coordenadas en píxeles/metros. Se suprimen las uniones internas colineales de los paños. Estos anillos no se interpretan como recintos. |
| Solapes | Cero superposiciones de área positiva entre paños del registro. |
| Vanos | Los 12 huecos con jambas tocan sus soportes y no intersectan huellas de muro. El paso abierto O13 se comprueba libre a lo largo de su eje de referencia. No se genera un muro en ese paso. |
| Puertas | Seis símbolos revisados visualmente sobre la ampliación: acceso y D3 giran hacia el muro superior; D1/D2 hacia sus recintos; baño hacia circulación; logia hacia su interior. Pivotes y extremos abiertos coinciden con las observaciones registradas dentro del detalle disponible. |
| Mobiliario | Las hojas de armarios quedan separadas de los accesos; arcos, equipos, achurados, ducha y panel Image190 no se admiten como muros. |
| Escala y fuente | Transformación T10 reutilizada sin deformación desigual ni ajuste por superficie. PDF, planta y calibración conservan las huellas esperadas; las demás referencias no se editaron. |

Se inspeccionaron las tres láminas completas: planta con caras y vanos, seis ampliaciones de puertas y cuatro detalles de remates/logia. Los trazos se apoyan en los contornos arquitectónicos, sin seguir líneas de camas, sanitarios, tramas o círculos de maniobra. La isométrica original se usó para contrastar el nicho, la continuidad de separaciones y la celosía del frente de logia. No se ha hecho una comparación isométrica de un modelo propio, que corresponde a las etapas de modelado.

## Resoluciones y límites

- **CL-M13:** respaldo y lateral del nicho D3 registrados con su remate superior de jamba. No es una caja maciza ni una pared sobre el arco pequeño.
- **CL-V11:** celosía probable por la isométrica, con frente parcialmente oculto por equipos en planta. Su apertura y detalle de carpintería continúan en T14/T22.
- **CL-H09:** una hoja pequeña visible en el nicho D3. Se conserva como evidencia; T37 debe producir el armario de dos hojas solicitado por el usuario.
- **CL-F11:** el panel añadido por Image190 no acredita un tabique. Queda excluido de arquitectura; su relación con el mueble final continúa en T34/T37.
- **CL-M20/CL-E12:** se registran los bordes del volumen técnico, sin convertir su X interior en diagonales físicas. Función y altura siguen en T12/T14.

El borde superior exterior está recortado: `v=1` es un trazo provisional, no una nueva cota acreditada. Los nominales de 15 cm se conservan separados de los espesores leídos. Los códigos F no se interpretan como centímetros. Las coordenadas con decimales permiten reproducir el registro, no suponen precisión de fabricación.

No se dispone de anchos nominales de puertas ni de detalle completo de marcos. La sensibilidad gráfica local de bisagras y hojas es de 2 px, además de la sensibilidad de escala T10. En P06 la hoja gráfica resulta 1 px (8,46 mm) mayor que el tramo levantado entre soportes. Se conserva la discrepancia para resolver en T22; **no se valida con ello una hoja física ni su barrido**. Los anchos libres terminados permanecen sin asignar.

El registro no calcula el área del departamento ni confirma 76,66 m²; no define alturas, antepechos o dinteles. Tampoco acredita accesibilidad final, ausencia de penetraciones de muebles, colliders, recorrido, POV, Blender, GLB o Unreal. Esas pruebas siguen pendientes en sus tareas específicas.

## Archivos y continuación

El [registro T11](../architecture/plan/README.md) contiene datos de autoría y resultado métrico, con tablas legibles. Las [evidencias visuales](../references/derived/t11-trazado/README.md) y [comprobacion.json](../references/derived/t11-trazado/comprobacion.json) documentan el resultado. El generador es `scripts/build-t11-plan.py`.

La siguiente tarea es **T12**, confirmar el baño longitudinal, la ducha al fondo, la función de sus símbolos y la separación de logia. Se reutilizarán los bordes T11; ninguna trama de área de uso deberá convertirse en un tabique transversal. T13 resolverá superficies y T14 las dimensiones verticales.

No cambió `web/`; no corresponde recompilar ni publicar una versión de arquitectura aún sin modelar. El sitio registrado sigue privado y sin despliegue. El seguimiento de E02 se sincroniza con la issue #3 del repositorio del proyecto.
