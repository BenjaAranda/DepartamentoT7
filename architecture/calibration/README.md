# Calibración de trabajo T10

Fecha: 9 de septiembre de 2026. Se fijaron origen, ejes y una escala uniforme para continuar el levantamiento de la planta nativa. Los controles seleccionados cumplen el objetivo de residuo de 0,01 m. Esto no cierra la validación dimensional del departamento: faltan el despiece, las medidas no documentadas y la resolución de superficie.

| Parámetro | Resultado |
|---|---|
| Imagen calibrada | Planta nativa de p20, 1536 × 813 px |
| Escala uniforme | **0,008459347583241785 m/px** |
| Equivalencia | **118,21242597727385 px/m** |
| Origen nativo | **u = 22,292490118577074; v = 630,9126213592233 px** |
| Origen físico | Intersección de caras interiores inferior e izquierda de D1, sobre piso terminado; (0, 0, 0) m |
| Ejes de autoría | X hacia la derecha del plano, Y hacia arriba, Z vertical |
| Giro aplicado | 0°; se conservan los ejes del raster |
| Norte geográfico | No documentado |
| Residuo máximo del ajuste | 1,232 mm |
| Residuo máximo de los controles | **4,586 mm**, en CAL-CE08 |
| Diferencia entre escalas estimadas por eje | 0,1246 %; se adopta una única escala |

Los decimales completos permiten reproducir el cálculo, no expresan precisión constructiva. Para uso humano basta indicar aproximadamente 118,21 px/m. Los datos completos están en [t10-calibracion.json](t10-calibracion.json), gobernados por [t10-observaciones.json](t10-observaciones.json). La [tabla de residuos](RESIDUOS_T10.md) conserva cada comparación.

## Medidas de ajuste y controles

Se fijaron tres cotas de ajuste, antes de incorporar los controles:

| ID | Referencia T09 | Dirección | Nominal aceptado para trabajo | Tramo leído |
|---|---|---|---:|---:|
| CAL-FH01 | D05: cadena superior del baño | Horizontal | 0,900 m | 106,537 px |
| CAL-FH02 | D12: cota superior de logia | Horizontal | 1,375 m | 162,471 px |
| CAL-FV01 | D14: cota de logia | Vertical | 0,500 m | 59,039 px |

Las cotas locales de T09 siguen teniendo cm como unidad **inferida**, ahora respaldada por su coherencia con las seis lecturas comprobadas de muros rotulados de 15 cm. No se reescribió T09 como si el PDF imprimiera esa unidad junto a cada cifra.

Se midieron aparte diez tramos de control: cuatro cotas locales y seis espesores explícitos. CAL-CH01 comparte una marca con el ajuste del baño, por lo que se identifica como control adicional parcialmente dependiente. Los demás extremos de control no participan en el ajuste. CAL-CH02/CH03 comparten una marca entre sí; CE03/CE04 pertenecen a la misma alineación de fachada. Estas relaciones quedan registradas y no se cuentan como fuentes estadísticas independientes.

Los cuatro círculos de giro también quedaron fuera del ajuste. Se comprobaron dos diámetros por símbolo mediante una elipse de ejes paralelos al raster, sin imponer que fueran iguales. Son ocho comparaciones numéricas de cuatro símbolos, no ocho fuentes independientes. Todos los diámetros convertidos quedan entre 1,4964 y 1,5039 m frente al nominal inferido de 1,50 m.

Los residuos se calcularon después de fijar la escala y no se usaron para volver a ajustarla. El resultado comprende 21 comparaciones: tres de ajuste y 18 de control, con las dependencias anteriores explícitas. Los 18 controles seleccionados quedan dentro de 10 mm. Este resultado solo se aplica a esas lecturas y no declara V02 superada para todas las dimensiones futuras del modelo.

## Método de lectura y ajuste

1. Las ventanas de lectura se seleccionan sobre las marcas de cota o trazos de caras, con sus coordenadas nativas y motivo. No son las cajas de texto de T09 ni las cajas generales de clasificación de T08.
2. Dentro de cada ventana se obtiene un perfil medio perpendicular al trazo. Se localiza su mínimo de luminosidad y se calcula un centro ponderado por oscuridad dentro de un píxel a cada lado. El umbral y la ventana quedan registrados. La otra coordenada localiza la línea de cota, sin intervenir en la longitud proyectada sobre el eje correspondiente.
3. Para los círculos se seleccionan sectores que evitan textos y superposiciones. Un ajuste de círculo permite descartar ruido alejado del trazo; luego se mide una elipse con radios independientes en X e Y. Semillas, sectores, umbrales y cantidad de píxeles usados quedan registrados. Estos cálculos ocurren íntegramente en píxeles antes de convertir a metros.
4. La escala uniforme minimiza los residuos de las tres cotas de ajuste: `s = sum(longitud_px * nominal_m) / sum(longitud_px²)`.
5. Se estiman por separado escalas horizontal y vertical solo como diagnóstico: 0,00845845633309471 y 0,008468999322156633 m/px. No se aplican dos escalas distintas al modelo.
6. Se convierten los controles con la misma escala y se comprueban origen, reglas de un metro, puntos de orientación y transformación de ida y vuelta.

Se comprobó la horizontalidad de la cara inferior de D1 en dos zonas separadas y la verticalidad de la cara izquierda en otras dos. Las desviaciones calculadas son 0° y aproximadamente -0,000023°, respectivamente, por debajo del criterio de 0,1°. Son mediciones de alineación del raster; no justifican declarar una precisión angular equivalente en obra.

## Incertidumbre y exclusiones

Con esta escala, un píxel representa aproximadamente 8,46 mm. Una posición subpíxel mejora la reproducibilidad de lectura del trazo, pero no añade detalle al documento ni demuestra su exactitud respecto de la obra.

Se registró una sensibilidad conservadora desplazando cada extremo de ajuste hasta ±1 px. El intervalo común de consistencia resultante es **[0,00836013120406623; 0,008568520902896778] m/px**, aproximadamente -1,17 % a +1,29 % respecto de la escala adoptada. Por ejemplo, extrapolar a una longitud nominal de trabajo de 10 m puede implicar aproximadamente -0,117 a +0,129 m en este análisis. Esto muestra por qué un residuo local de 4,6 mm no acredita centímetros de precisión en toda la vivienda. El intervalo no es una confianza estadística ni una tolerancia constructiva; tampoco incluye errores desconocidos de la documentación original.

Se mantienen fuera de la aprobación métrica:

- T09-D07, D08 y D11: cifras asociadas a achurados, con límites funcionales o lecturas pendientes. La confianza alta de la cifra 120 no confirma automáticamente sus extremos geométricos. Resolver en T12 sin convertir tramas en paredes.
- T09-E01 y E02: el borde exterior superior toca el límite del raster. No se mide como si ambas caras estuvieran completas.
- Los 28 códigos de tabiques: sus números no definen espesor en centímetros.
- Las cuatro menciones de superficie y las cuatro referencias complementarias de T09: no se utilizan para ajustar la escala.

No se usaron los 76,66 m², las medidas supuestas de muebles o baldosas ni un estiramiento desigual de la planta. Los datos genéricos de p23-p24 tampoco se usaron como altura o espesor del T7. Las cuestiones de T08 y T09 que siguen sin resolver permanecen abiertas.

## Transformación que debe reutilizar T11

Para un punto nativo `(u, v)` y una altura `h` en metros:

```text
s  = 0.008459347583241785
u0 = 22.292490118577074
v0 = 630.9126213592233

Blender: X = (u - u0) * s
         Y = (v0 - v) * s
         Z = h

glTF/web desde Blender: (X, Y, Z) -> (X, Z, -Y)
```

Las matrices directa e inversa están en el JSON. Esta transformación conserva la orientación: acceso arriba a la derecha, D3 arriba a la izquierda y logia abajo a la derecha. Las tres marcas de zona incluidas sirven para detectar un reflejo accidental; no son bisagras, puntos de inicio de cámara ni posiciones certificadas de muebles.

Una unidad de autoría y de glTF/web representará un metro. La referencia ocular de 1,60 m permanece como requisito, sin declarar una cámara 3D validada en T10. La importación de escala y orientación en Unreal corresponde a T49.

## Reproducción y siguiente tarea

Ejecutar `python scripts/calibrate-t10.py` desde la raíz. Runtime verificado: Python 3.12.14, NumPy 2.3.5, Pillow 12.3.0 y Arial de Windows. El proceso comprueba las huellas del PDF, referencias T07 y catálogo/lecturas T09; regenera JSON, tabla, residuos y tres imágenes de evidencia. Guarda la huella de la fuente tipográfica utilizada. Si un control sale del objetivo, el proceso termina con error y requiere revisar el resultado antes de marcar la tarea.

Ver [evidencias](../../references/derived/t10-calibracion/README.md) y [validación T10](../../docs/VALIDACION_T10.md). T11 registrará los muros, caras, esquinas, retranqueos y vanos con esta transformación, documentando incertidumbre y datos inferidos. Si una nueva fuente exige cambiar la escala, deberá revisarse esta calibración y regenerarse la geometría dependiente.
