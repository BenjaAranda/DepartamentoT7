# Evidencia de calibración T10

- [Planta calibrada](planta-calibrada.png): origen, ejes de un metro, cadenas de ajuste y controles de espesores y maniobra sobre la imagen nativa.
- [Detalle de cadenas](detalle-cadenas.png): marcas elegidas en baño y logia; azul para ajuste y verde para control.
- [Controles de círculos](controles-circulos.png): sectores de píxeles utilizados y elipses medidas en ambos ejes, sin usarlas para ajustar la escala.
- [Residuos TSV](residuos.tsv): 21 comparaciones con referencia, función, longitud, nominal y residuo.
- [Comprobación automática](comprobacion.json): integridad de fuentes, pruebas métricas y huellas de derivados.

Los parámetros completos, método y limitaciones se explican en [la calibración](../../../architecture/calibration/README.md). También está disponible la [tabla de residuos en Markdown](../../../architecture/calibration/RESIDUOS_T10.md) y el [informe de validación](../../../docs/VALIDACION_T10.md).

Las imágenes son derivados de lectura, no una nueva referencia arquitectónica ni vistas de un modelo 3D ya construido. No alteran el PDF ni las imágenes T07. Los círculos superpuestos representan símbolos de maniobra, no volúmenes físicos.

Regenerar desde la raíz con `python scripts/calibrate-t10.py`. No cambiar solamente una imagen o coordenadas en el navegador: la fuente de parámetros es `architecture/calibration/t10-observaciones.json` y la transformación común se obtiene de `t10-calibracion.json`.
