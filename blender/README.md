# Fuente Blender

El archivo maestro editable se guardará aquí. `scripts/` contendrá las herramientas de construcción, exportación y comprobación; `textures/`, las texturas originales de autoría. El modelo aún no se ha creado.

Autoría métrica: una unidad Blender equivale a un metro, X hacia la derecha del plano, Y hacia arriba del plano y Z vertical. Las geometrías y los proxies compartirán identificadores y revisión según E03.

Los `.blend` y las texturas de autoría especificadas en `.gitattributes` se almacenan con LFS. Las copias de recuperación `.blend1`, `.blend2`, etc. permanecen locales. Conservar rutas de texturas relativas o empaquetarlas en el archivo al preparar una entrega reproducible.

Las exportaciones de intercambio irán a `../assets/interchange/`; las colisiones a `../assets/colliders/`. Los recursos optimizados para el navegador se derivarán de esa misma revisión.
