# Datos arquitectónicos

La [clasificación T08](classification/README.md) contiene 89 grupos de trazos de la página 20, con localizadores, procedencia, criterio y confianza. Su [atlas visual](../references/derived/t08-clasificacion/atlas.html) permite compararlos sobre la planta nativa y la lámina anotada. Los rectángulos están en píxeles: no son caras de muro, polígonos de superficie ni geometría apta para extrusión.

El [inventario T09](measurements/README.md) añade 58 lecturas y referencias con su ubicación, unidad y confianza. Distingue las ocho menciones de 15 cm de los códigos de tabiques que no acreditan espesor, y registra la búsqueda complementaria en las 42 páginas del PDF.

La [calibración T10](calibration/README.md) fija origen, ejes y escala uniforme de trabajo, con controles y sensibilidad de lectura documentados. La transformación común está en `calibration/t10-calibracion.json`; se reutilizará para evitar coordenadas distintas en Blender y web.

T11 es el siguiente paso: registrar muros, esquinas, retranqueos y vanos, además del soporte, ancho, bisagra y sentido de apertura de cada puerta. La calibración no cierra los espesores desconocidos, alturas ni superficie del departamento.

Cada medida deberá conservar su unidad en metros, identificador, procedencia y grado de certeza. Distinguir el objetivo oficial de 76,66 m², el área calculada y la superficie útil; excluir la terraza del cómputo interior. La diferencia con el rótulo de 76,80 m² se resolverá según el plan.

Los archivos de texto y JSON se versionan normalmente. Esta carpeta gobierna las medidas que se aplicarán a Blender, no una segunda geometría independiente para el navegador.
