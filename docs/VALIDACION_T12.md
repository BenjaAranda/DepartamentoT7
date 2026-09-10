# T12: baño longitudinal y logia separada

Fecha: 9 de septiembre de 2026, America/Santiago. Resultado: **T12 completada como interpretación y comprobación de distribución 2D**. El baño es un recinto continuo, con ducha al fondo, y la logia permanece separada con entrada desde cocina.

Se compararon planta e isométrica de la página 20, ampliando cabecera, inodoro, apoyos, ducha y logia. Se revisaron los ejemplos constructivos de p22/p23 y el texto extraíble de las 42 páginas para buscar rótulos de función. La página 20 gobierna la distribución; los ejemplos no aportan nuevas dimensiones aplicables al T7.

## Resultado arquitectónico

El baño entra por O05, con P05 abriendo hacia la circulación. La cabecera contiene un lavamanos y un equipo independiente probable; el inodoro está en el tramo central; la ducha, junto a la ventana O10, ocupa el fondo. Los achurados central e inferior son reservas de uso sobre el piso. No hay evidencia de tabiques transversales que creen otro recinto.

La logia entra por O06 desde cocina. W20A y W20B, con la franja técnica entre ambos, cubren toda la longitud de planta que comparte con el baño. No se registra un acceso lateral baño-logia. La X del interior técnico se conserva como símbolo. O11 permanece como celosía probable con funcionamiento pendiente.

La identidad de EQ02 se precisa como lavamanos. EQ01 es probablemente una lavadora de carga superior, por su caja y panel posterior en la isométrica; el documento no la rotula de manera inequívoca. LG02 muestra dos cuerpos circulares de servicio que tampoco pueden identificarse definitivamente. Estas incertidumbres no justifican crear paredes ni colocar equipos extra: la lavadora final se encajará en logia en T42 según el programa.

## Verificación realizada

| Comprobación | Resultado |
|---|---|
| Contornos | Tres regiones registradas: baño, logia y franja técnica. Sus interiores no se solapan ni invaden huellas de muro. |
| Baño continuo | Tres bandas interiores conectadas por bordes de longitud positiva, correspondientes a cambios laterales de ancho. La descomposición coincide con el polígono por comparación de celdas de coordenadas. No se consideran tres recintos. |
| Perímetro de regiones | Muestras de cada lado apoyadas en las caras T11 y vanos declarados. Los cierres analíticos de puerta/ventana no se convierten en paredes. |
| Accesos | Baño solo O05 desde circulación; logia solo O06 desde cocina. Ventana y celosía excluidas del grafo de accesos. |
| Separación baño-logia | W20A/W20B cubren todo el intervalo longitudinal compartido. No existe un vano común entre regiones. |
| Ducha | Símbolo posterior al inodoro, adyacente al extremo inferior del baño. Su frente coincide con el final de la reserva anterior, sin una huella de muro que lo cierre. |
| Achurados | Dos reservas cruzadas por la guía longitudinal, sin intersección con muros. Se corroboran las lecturas locales 120/80 y 90, manteniendo unidades inferidas y función específica probable. |
| Maniobra | La elipse de giro observada en T10 no intersecta las huellas de muro. Esta comprobación no incluye sanitarios como volúmenes físicos, apoyos, puertas o circulación real. |
| Guías topológicas | Dos líneas sin anchura cruzan sus vanos previstos; cero intersecciones con interiores de paños T11. No se prueba el recorrido de un personaje o silla de ruedas. |
| Inventario | Doce elementos/áreas con fuentes, confianza, decisión y siguiente tarea. Ninguna caja de símbolo se convierte en collider. |
| Integridad | PDF y referencias T07/T10/T11 conservan sus huellas. Cero muros nuevos y ninguna coordenada de muro modificada. |

Se inspeccionaron las tres láminas finales. Se corrigió el recorte del ejemplo p23 para mostrar el diagrama completo, sin cortar sus rótulos. La vista de p20 mantiene orientación y contexto; no se refleja la planta ni se añade una partición en el baño.

## Alcance y pendientes

Las medidas de trabajo del baño, aproximadamente 5,284 m de longitud y 1,590/1,502/1,402 m de ancho por tramo, proceden de T10/T11. Su incertidumbre permanece. No se midió la altura mediante la isométrica ni se usaron datos de superficie para alterar esos valores.

Las áreas de uso no acreditan por sí mismas accesibilidad normativa ni maniobra real. Alturas, pendientes de ducha, detalle de apoyos, instalación técnica y funcionamiento de celosía siguen en T14/T38/T42 según corresponda. El piso continuo de la ducha es un requisito de implementación accesible, no una cota vertical extraída de la imagen. La identidad final de EQ01 y LG02 y el encaje de lavadora/lavadero continúan en la etapa de equipamiento.

No se calcula superficie en T12. No se genera ni valida todavía Blender, Unreal, GLB, colliders, POV o recorrido 3D. Tampoco cambia `web/`: el sitio sigue registrado, privado y sin publicar.

## Evidencia y continuación

Ver la [interpretación T12](../architecture/topology/README.md), el [registro métrico](../architecture/topology/t12-topologia.json), las [láminas e inventario](../references/derived/t12-bano-logia/README.md) y la [comprobación reproducible](../references/derived/t12-bano-logia/comprobacion.json). Entrada: `architecture/topology/t12-interpretacion.json`; generador: `scripts/build-t12-topology.py`.

Siguiente: **T13**, calcular por separado área de cómputo, área útil y terraza; resolver el contraste 76,66/76,80 m² y edificada/útil sin deformar el trazado. Se preservan las incertidumbres del borde superior, cotas y criterio de superficie. El seguimiento de E02 se actualiza en la issue #3 y mantiene las tareas posteriores pendientes.
