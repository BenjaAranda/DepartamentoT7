# E02 · Cierre del análisis dimensional

T13–T15 completadas como base de simulación aproximada. El criterio posterior del usuario se incorpora al final y sustituye la consulta inicial. No acredita medidas de obra.

## Superficies

| Concepto | m² |
|---|---:|
| Exterior trazado | 77.9800 |
| Interior entre caras, sin umbrales | 69.7806 |
| Interior con umbrales de puertas | 70.2200 |
| Muros | 6.5805 |
| Franja técnica | 0.3406 |
| Terraza de presentación provisional | 8.7223 |

El encabezado p20 dice 76,66 m² EDIFICADO y 0,00 m² TERRAZA; la planta nativa dice 76,80 m². Su diferencia es 0,14 m². No hay perímetro de cómputo ni cuadro útil por recinto. No se ha demostrado que ninguno sea superficie útil. La partición geométrica en celdas analíticas cierra con residuo menor de 1e-8 m²; una fórmula independiente del contorno en L coincide.

La sensibilidad de escala T10 aplicada al área exterior produce 76,1615–80,0058 m²; no es intervalo estadístico y no incluye todos los errores de borde. Contener 76,66 y 76,80 dentro de esa sensibilidad no valida ninguno. El extremo superior sigue recortado. Las superficies por uso común se separan mediante límites contables, nunca paredes. Armarios y equipos no se descuentan de esta superficie geométrica.

## Alturas y contexto

Las alturas se registran por parámetro con su procedencia: ojo 1,60 m es requisito; cielo 2,40 m, entrepisos 2,70 m, losa 0,20 m y antepechos son supuestos editables. No se atribuyen a cotas ilegibles. Torre A/primer piso es la propuesta apoyada por p15–p16; los tres pisos superiores son contexto T6 opaco, sin copiar T7. La ubicación exacta de la unidad, dimensiones del pasillo y límite de terraza permanecen provisionales.

## Continuación

E03 puede comprobar intercambio, unidades, orientación y sincronización sin resolver una equivalencia documental inexistente en el PDF. Conservar T10 mientras la consulta está pendiente y regenerar desde la fuente si el criterio cambia. No declarar exactitud 76,66 m² ni aprobar V03 por un rótulo. La lámina de superficies se revisó visualmente; sus fondos y colores no modifican la fuente.

Archivos: architecture/dimensions/t13-superficies.json, t14-alturas.json, t15-contexto.json; evidencia validation/e02/superficies.png.

## Criterio posterior del usuario

El 10-09-2026 el usuario admite aproximación a 76,66 con margen 0,5, interpretado y comunicado como ±0,5 m² de referencia edificada. Se adopta contorno de simulación de 77,10 m², diferencia +0,44 m², mediante factor uniforme XY 0,9943414226883663. La escala permanece dentro de la sensibilidad T10. La superficie útil se conserva separada; ni el contorno ni la tolerancia acreditan una medición oficial. El mayor residuo gráfico resultante es 12,073 mm, frente a meta inicial 10 mm: se conserva ese límite explícito, sin declarar V02 exacta. Alturas y marca ocular no se escalan. T13 concluye con este criterio de aproximación; E02 queda cerrada como base de simulación, con sus supuestos transferidos a validación.
