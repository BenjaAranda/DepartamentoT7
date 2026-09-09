# T10: origen, ejes y escala

Fecha: 9 de septiembre de 2026, America/Santiago. Resultado: T10 completada como calibración de trabajo del raster, con su incertidumbre documentada y sin cerrar la validación dimensional global.

Se fijó una escala uniforme de **0,008459347583241785 m/px** (118,21242597727385 px/m). El origen está en la intersección de caras interiores inferior e izquierda de D1, en `(u, v) = (22,292490118577074; 630,9126213592233)` px nativos, sobre el piso terminado. X apunta a la derecha, Y hacia arriba del plano y Z hacia arriba físicamente. No se asigna norte geográfico.

## Verificación realizada

| Comprobación | Resultado |
|---|---|
| Ajuste | Tres cotas: baño 90 horizontal, logia 137.5 horizontal y logia 50 vertical. Máximo residuo 1,232 mm. |
| Coherencia de ejes | Diferencia relativa de 0,1246 % entre escalas diagnósticas horizontal y vertical. Se conserva una sola escala. |
| Cadenas y espesores de control | Diez tramos fuera del ajuste, con dependencia parcial señalada en el que comparte una marca. Incluyen seis paños rotulados de 15 cm. |
| Círculos de maniobra | Cuatro símbolos fuera del ajuste, comprobados con diámetros horizontal y vertical por separado. No se impone una igualdad de radios para ocultar deformaciones. |
| Residuos de control | Las 18 comparaciones seleccionadas quedan dentro de 10 mm. Máximo: 4,586 mm, CAL-CE08. Los dos diámetros de un círculo y las marcas compartidas no se tratan como fuentes independientes. |
| Ejes del raster | Cara inferior de D1 horizontal y cara izquierda vertical, comprobadas en posiciones separadas. Desviación máxima aproximada 0,000023°; sin giro correctivo. |
| Transformación | Origen convertido a cero, referencias algebraicas de un metro en X/Y y recorrido directo-inverso de cinco puntos comprobados. |
| Orientación | Marcas de acceso, D3 y logia conservan su orden y posición relativa; no hay reflejo de la planta. |
| Integridad | PDF y referencias T07 intactos; catálogo y lecturas T09 con sus huellas anteriores. |

La [tabla completa de residuos](../architecture/calibration/RESIDUOS_T10.md) identifica cada nominal, lectura, función y resultado. El generador es `scripts/calibrate-t10.py`, con parámetros de lectura en `architecture/calibration/t10-observaciones.json`. Las huellas y comprobaciones quedan en [comprobacion.json](../references/derived/t10-calibracion/comprobacion.json).

Se inspeccionaron la planta anotada, los acercamientos de baño/logia y las cuatro elipses sobre los círculos originales. Se verificó que las marcas se apoyaran en los trazos seleccionados y se corrigió la posición gráfica transversal de la cota vertical de logia. La corrección no cambió su longitud ni la escala. Los rótulos, unidades y límites de uso son legibles en las evidencias finales.

## Límites y continuidad

El máximo residuo local no equivale a la precisión absoluta del plano. Un píxel representa unos 8,46 mm. La sensibilidad registrada de ±1 px por extremo de ajuste da un intervalo de escala de [0,00836013120406623; 0,008568520902896778] m/px. Ese intervalo de consistencia no es una confianza estadística ni una tolerancia de obra. Su efecto crece al extrapolar distancias largas, como se explica en [la calibración](../architecture/calibration/README.md).

Las unidades locales siguen identificadas como inferidas, coherentes con los espesores explícitos. No se usaron las superficies 76,66/76,80 m² para ajustar, ni mobiliario supuesto, ni códigos de tabique como dimensiones. Las cifras sobre achurados y el borde superior recortado conservan sus exclusiones razonadas.

T10 no valida la superficie, el conjunto de cotas arquitectónicas, alturas, giros de puertas, colliders, recorrido ni POV de una cámara existente. Tampoco convierte las marcas de orientación en posiciones de inicio. V02 solo tiene aquí evidencia parcial de controles del raster; V01-V15 no se declaran cerradas por esta tarea.

No cambió `web/`, por lo que no corresponde recompilarla o publicar el sitio. Blender, GLB y Unreal recibirán posteriormente la misma transformación. La siguiente tarea es T11: registrar muros, esquinas, retranqueos y vanos, con soporte, ancho, bisagra y sentido de apertura de cada puerta, conservando incertidumbres donde falte detalle.
