# E03 · Intercambio mínimo comprobado

T16–T20 completadas. La fuente métrica architecture/model/departamento-t7.json reúne recintos, 40 paños, 13 vanos, seis puertas, alturas, procedencias y revisión derivada. El navegador no redibuja los muros a partir de coordenadas propias.

Blender 5.2.1 LTS guardó DepartamentoT7-prueba.blend en sistema métrico, escala de unidad 1 y transformaciones de malla aplicadas. Colecciones: Architecture, Equipment, Decoration, References y Collisions. Incluye regla de 1 m, datum ocular de 1,60 m, cámara a esa altura, puerta con pivote y muro dividido en jambas/dintel.

La exportación GLB se cargó con Three.js y se comparó contra el archivo de colisiones. La regla mide 1,000000 m; la marca ocular 1,600000024 m. Las cuatro cajas de colisión coinciden con los volúmenes exportados a menos de 1 mm. Huellas del Blender, GLB y colisiones coinciden con el manifiesto; la revisión es común. No se aplicó una segunda conversión de unidades.

Se ejecutó Rapier con una cápsula durante 180 pasos por caso: cruce del vano desde ambas caras, bloqueo contra muro, bloqueo de hoja cerrada y apoyo en suelo. Los casos pasaron; posiciones reales en validation/e03/exchange-check.json. Esta prueba aislada no reemplaza recorridos del departamento en E05/E10.

En el navegador se comprobó la carga 3D y apertura de la hoja; se corrigieron materiales blancos exportados y sombras con bandas. La interfaz identifica la prueba como prototipo y permite consultar la planta nativa. El ejemplo web aún no incluye controlador de recorrido; las colisiones de la hoja dinámica se implementarán en E05.

La compilación de producción y tipos TypeScript pasaron. El auxiliar de Sites falló al resolver npm en Windows; la misma compilación declarada se completó mediante npm run build. Se mantiene ese problema del auxiliar registrado, sin atribuirle una compilación exitosa. Avisos: módulos 3D grandes pendientes de optimización en E09 y advertencia de API de inicialización de Rapier, sin fallo de casos físicos.

Unreal 5.8.2 tiene sus archivos principales disponibles; medición e importación real pendientes en E08. El sitio sigue privado y sin publicar, conforme al hito de entrega E11.

Reproducción: scripts/build-model-data.py; Blender en segundo plano ejecutando blender/scripts/build-exchange-proof.py; desde web, node scripts/check-exchange.mjs, npm run typecheck y npm run build. El manifiesto distribuye la pareja GLB/colisiones y comprueba sus huellas antes de mostrar la escena.
