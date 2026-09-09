# Registro T11: muros y aperturas

Generado desde `t11-trazado.json` mediante `scripts/build-t11-plan.py`. Todas las longitudes de las tablas son lecturas métricas de trabajo, no cotas nominales ni precisión de fabricación. El JSON conserva píxeles, metros, caras, ejes, fuentes, contactos y límites.

## Paños

| ID | Paño | Longitud de eje (m) | Espesor leído (m) | Nominal documentado (m) |
|---|---|---:|---:|---:|
| W01A | Superior izquierdo | 4.547 | 0.147 | 0.150 |
| W01B | Superior central | 3.962 | 0.147 | — |
| W01C | Superior derecho | 4.399 | 0.147 | 0.150 |
| W02 | Oeste sobre ventana D3 | 0.923 | 0.149 | 0.150 |
| W03 | Oeste bajo ventana D3 y lateral D1 | 3.371 | 0.149 | 0.150 |
| W04 | Este bajo acceso | 5.528 | 0.147 | 0.150 |
| W05A | Fachada D1 izquierda de ventana | 2.506 | 0.119 | — |
| W05B | Fachada D1 derecha de ventana | 0.368 | 0.119 | — |
| W06A | Fachada D2 izquierda de ventana | 0.827 | 0.119 | — |
| W06B | Fachada D2 derecha de ventana | 0.877 | 0.119 | — |
| W07 | Retorno exterior al costado del baño | 3.363 | 0.148 | 0.150 |
| W08A | Fachada baño izquierda de ventana | 0.358 | 0.125 | — |
| W08B | Fachada baño derecha de ventana y pie de shaft | 0.817 | 0.125 | — |
| W09A | Machón entre logia y ventana comedor | 0.660 | 0.125 | — |
| W09B | Fachada comedor derecha de ventana | 0.306 | 0.125 | — |
| W10A | D1–D2 tabique superior | 1.634 | 0.061 | — |
| W10B | D1–D2 paño de 15 cm | 2.094 | 0.149 | 0.150 |
| W11 | D2–baño tabique superior | 2.107 | 0.060 | — |
| W12A | D3–D1 paño inferior | 1.734 | 0.059 | — |
| W12B | D3–D1 retorno del nicho | 0.659 | 0.059 | — |
| W12C | D3–D1 cabecera hasta jamba D1 | 1.194 | 0.060 | — |
| W13A | Respaldo del nicho D3 | 0.599 | 0.060 | — |
| W13B | Lateral del nicho D3 y remate de jamba | 0.623 | 0.061 | — |
| W14A | Cabecera D2 tramo bajo | 0.601 | 0.060 | — |
| W14B | Cabecera D2 retorno | 0.473 | 0.059 | — |
| W14C | Cabecera D2 hasta jamba | 1.311 | 0.061 | — |
| W15 | Cabecera baño a la derecha de su puerta | 0.695 | 0.061 | — |
| W16A | Baño–cocina tramo largo | 3.264 | 0.058 | — |
| W16B | Baño–cocina después del retranqueo | 0.500 | 0.059 | — |
| W17A | Nicho cocina paño superior | 0.654 | 0.099 | — |
| W17B | Nicho cocina paño inferior | 0.654 | 0.058 | — |
| W18A | Cocina–estar paño corto de 15 cm | 0.998 | 0.145 | 0.150 |
| W18B | Cocina–comedor continuación delgada | 0.717 | 0.057 | — |
| W18C | Retorno de jamba derecha de logia | 0.178 | 0.084 | — |
| W18D | Logia–comedor | 1.438 | 0.061 | — |
| W19A | Retorno bajo lavaplatos | 0.670 | 0.059 | — |
| W19B | Cabecera del volumen técnico | 0.369 | 0.084 | — |
| W19C | Cabecera logia sobre lavadero | 0.409 | 0.084 | — |
| W20A | Baño–volumen técnico | 1.438 | 0.059 | — |
| W20B | Volumen técnico–logia | 1.438 | 0.073 | — |

Las longitudes de eje terminan en la sección del paño, sin prolongarse hasta ejes de otro muro. Los encuentros se describen con sus caras compartidas, no sumando estas longitudes como cotas de recinto.

## Vanos y paso abierto

| ID | Ubicación | Tramo entre soportes (m) | Tipo |
|---|---|---:|---|
| O01 | Acceso principal | 1.041 | puerta |
| O02 | Dormitorio 3 | 0.889 | puerta |
| O03 | Dormitorio 1 | 0.884 | puerta |
| O04 | Dormitorio 2 | 0.881 | puerta |
| O05 | Baño | 0.896 | puerta |
| O06 | Logia desde cocina | 0.850 | puerta |
| O07 | Ventana oeste D3 | 1.007 | ventana |
| O08 | Ventana D1 | 0.998 | ventana |
| O09 | Ventana D2 | 0.998 | ventana |
| O10 | Ventana baño al fondo | 0.596 | ventana |
| O11 | Frente de logia | 1.107 | celosia_probable |
| O12 | Ventana comedor | 1.895 | ventana |
| O13 | Paso abierto cocina–estar | 3.207 | paso_abierto |

O13 es una línea de paso libre de referencia, sin muro ni marco. O11 tiene jambas parcialmente ocultas por equipos y celosía probable por la isométrica. Antepechos, dinteles y funcionamiento de ventanas siguen pendientes.

## Puertas de recinto

| Puerta / vano | Hoja gráfica (m) | Bisagra en el plano | Soporte | Giro Blender +Z | Abre hacia |
|---|---:|---|---|---:|---|
| P01 / O01 | 1.002 | superior | W01C | -90° | interior, hacia el muro superior |
| P02 / O02 | 0.863 | superior | W01A | -90° | D3, hacia el muro superior |
| P03 / O03 | 0.867 | derecha | W14A / W10A | +90° | D1, junto a separación D1–D2 |
| P04 / O04 | 0.859 | derecha | W11 | +90° | D2, junto a separación con baño |
| P05 / O05 | 0.863 | izquierda | W11 | +90° | circulación superior, hacia fuera del baño |
| P06 / O06 | 0.859 | derecha | W18C / W18D | +90° | logia, junto a separación con comedor |

La posición cerrada se deriva del pivote, el radio gráfico y el sentido observado. No define todavía holguras de herrajes. En P06 la hoja gráfica supera el tramo entre soportes en 1 px (8,46 mm); ambos se conservan como observaciones del símbolo, dentro de la sensibilidad de lectura de 2 px, y requieren ajuste de carpintería en T22 antes de generar una hoja física. No se autoriza una hoja que penetre su marco.

## Hojas de mobiliario

| ID | Propietario | Hoja gráfica (m) | Situación |
|---|---|---:|---|
| F-D1-L | armario D1 | 0.482 | hoja izquierda de las dos dibujadas |
| F-D1-R | armario D1 | 0.482 | hoja derecha de las dos dibujadas |
| F-D2-T | armario D2 | 0.491 | hoja superior de las dos dibujadas |
| F-D2-B | armario D2 | 0.491 | hoja inferior de las dos dibujadas |
| F-D3-S | nicho D3 | 0.457 | una hoja visible en fuente; sustituir por armario de dos hojas en T37 según usuario, sin adoptar este símbolo como diseño final |

Las cinco hojas visibles se registran para explicar los nueve grupos de símbolos T08 junto con las seis puertas de recinto. No son once accesos de habitaciones. Los tres armarios finales tendrán dos hojas según el usuario; D3 requiere adaptar el diseño en T37.

## Esquinas y retranqueos

La unión de los paños produce 106 vértices de borde en 8 anillos cerrados. Incluye esquinas entrantes, convexas y remates de jambas; no equivale al número de esquinas de recintos. Las uniones internas entre paños se eliminan del borde. Los IDs, las coordenadas y los paños relacionados están en [esquinas.tsv](../../references/derived/t11-trazado/esquinas.tsv) y el registro JSON.

| Grupo | Encuentro | Paños conectados |
|---|---|---|
| J01 | Escalón D3–D1 | W12A, W12B, W12C |
| J02 | Nicho D3 y remate superior | W13A, W13B, W12C |
| J03 | Cabecera escalonada D2 | W14A, W14B, W14C |
| J04 | Cambio de espesor D1–D2 | W10A, W10B |
| J05 | Cambio de espesor D2–baño | W11, W07 |
| J06 | Retranqueo baño–cocina | W16A, W19A, W16B, W19B, W20A |
| J07 | Cocina–estar hasta logia–comedor | W18A, W18B, W18C, W18D |
| J08 | Escalón de fachada junto a terraza | W06B, W07, W08A |

## Resoluciones y continuidad

- **CL-M13**: Respaldo horizontal W13A y lateral W13B con saliente superior para jamba D3 identificados en ampliación; la hoja oeste es mobiliario. Estado: resuelto para trazado 2D. Sigue en Altura y carpintería T14/T37.
- **CL-V11**: Cerramiento de lamas probable por isométrica; ancho levantado hasta shaft a izquierda, aunque parte esté oculta por equipo en planta. Estado: tipo probable, funcionamiento no resuelto. Sigue en T14/T22.
- **CL-H09**: Una hoja pequeña gira hacia D3 desde frente oeste del nicho. La fuente y el requisito de dos hojas se registran por separado. Estado: simbología localizada, adaptación pendiente. Sigue en T37.
- **CL-F11**: Panel Image190 añadido por composición de la lámina, sin doble cara de tabique en planta nativa. Se excluye del catálogo de muros; no acredita otro espesor ni modifica el perímetro. Estado: exclusión arquitectónica resuelta, diseño de mueble pendiente. Sigue en T34/T37.
- **CL-M20 / CL-E12**: Solo bordes W19B/W20A/W20B y fachada; X interior no es geometría. Función y altura por confirmar. Estado: contorno registrado, uso pendiente. Sigue en T12/T14.
