# Datos arquitectónicos

La [clasificación T08](classification/README.md) contiene 89 grupos de trazos de la página 20, con localizadores, procedencia, criterio y confianza. Su [atlas visual](../references/derived/t08-clasificacion/atlas.html) permite compararlos sobre la planta nativa y la lámina anotada. Los rectángulos están en píxeles: no son caras de muro, polígonos de superficie ni geometría apta para extrusión.

El [inventario T09](measurements/README.md) añade 58 lecturas y referencias con su ubicación, unidad y confianza. Distingue las ocho menciones de 15 cm de los códigos de tabiques que no acreditan espesor, y registra la búsqueda complementaria en las 42 páginas del PDF.

La [calibración T10](calibration/README.md) fija origen, ejes y escala uniforme de trabajo, con controles y sensibilidad de lectura documentados. La transformación común está en `calibration/t10-calibracion.json`; se reutilizará para evitar coordenadas distintas en Blender y web.

El [levantamiento T11](plan/README.md) registra 40 paños entre caras, 13 vanos/pasos, seis puertas de recinto y sus bisagras, cinco hojas de mobiliario de la fuente y 106 vértices de borde. Conserva medidas leídas, nominales documentados e incertidumbres por separado.

La [interpretación T12](topology/README.md) confirma baño longitudinal, ducha al fondo y logia separada con acceso desde cocina. Registra doce elementos/áreas de uso, sin convertir símbolos o achurados en muros. T13 es el siguiente paso: resolver áreas de cómputo, útiles y terraza. La calibración y el trazado no cierran los espesores desconocidos, alturas ni superficie del departamento.

Cada medida deberá conservar su unidad en metros, identificador, procedencia y grado de certeza. Distinguir el objetivo oficial de 76,66 m², el área calculada y la superficie útil; excluir la terraza del cómputo interior. La diferencia con el rótulo de 76,80 m² se resolverá según el plan.

Los archivos de texto y JSON se versionan normalmente. Esta carpeta gobierna las medidas que se aplicarán a Blender, no una segunda geometría independiente para el navegador.
