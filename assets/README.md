# Activos compartidos

- `interchange/`: GLB sin extensiones de compresión no comprobadas en Unreal, exportado desde Blender.
- `colliders/`: datos de colisión y proxies geométricos con los mismos identificadores, coordenadas y revisión que el modelo.

GLB y otros binarios de intercambio usan LFS; JSON y metadatos usan Git normal. Las exportaciones definitivas se generarán en E03 y etapas posteriores. Esta tarea solo reserva su ubicación.

Los archivos que servirá el navegador estarán bajo `../web/public/models/` y `../web/public/textures/`, con el manifiesto de revisión previsto en T20. No mantener correcciones geométricas distintas entre esas copias y la fuente Blender.
