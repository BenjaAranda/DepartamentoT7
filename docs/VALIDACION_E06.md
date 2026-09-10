# E06 · Departamento amueblado

T34–T43 completadas. Revisión de activos: 3cea97167f9efbfb6594949266b6eeee6cc0ac5e1ff404f381f5e85cab85733f.

28 conjuntos definidos en architecture/furniture/layout.json, con posición métrica, recinto y procedencia. El módulo furnish.py los genera en Blender; geometría, hojas y colisiones se exportan juntos. Hay una cama por dormitorio (D1 matrimonial), cuatro veladores, tres armarios de dos hojas independientes, cocina, baño, estar, comedor y logia. Ningún escritorio en D2. Armarios con jambas, coronación, zócalo, tiradores, estante y barra; el nicho pequeño de D3 conserva su ancho y usa dos hojas estrechas. Sofá/TV y cama D1/TV están directamente enfrentados.

La detección sobre límites de mallas GLB comprobó cero penetraciones contra muros, marcos, dinteles y antepechos con tolerancia de 2 mm. Cuatro sillas también pasan en posición de uso, desplazadas 15 cm hacia atrás. Doce hojas completan apertura y cierre mediante el motor físico. Se detectó y corrigió una interferencia del lavadero con la puerta P06; lavadora y lavadero miran hacia el paso libre.

Diez recorridos de ida/vuelta pasan con armarios cerrados y otros diez con los seis frentes abiertos: dormitorios, baño, ducha, cocina, estar, comedor, logia y pasillo común. Se amplió la holgura junto a la cama D1 tras detectar atasco en el estado abierto. El muestreo de rutas considera también el margen horizontal del controlador. 5547/5548 pasos de seguimiento; ojo observado entre 1,59824 y 1,60438 m. La puerta sigue deteniéndose ante el jugador, sin empujarlo.

Evidencia: validation/e06/furniture-check.json, walk-check.json y wardrobes-open/walk-check.json. Se revisaron planta y dos isométricas generadas por Blender. GLB de 1,024 MB con 381 mallas; huellas de Blender, GLB y colisiones coinciden. La superficie GLB sigue siendo 77,100002 m² exteriores, dentro de la tolerancia acordada.

Alcance: pruebas automatizadas con el controlador real, más revisión visual de distribución. No equivalen todavía al recorrido manual final de E10 ni a certificación normativa de accesibilidad. Acabados, ambientación, iluminación final y optimización siguen en E07/E09.
