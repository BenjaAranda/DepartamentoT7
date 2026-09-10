# E04 · Arquitectura y edificio

T21–T27 implementadas y revisadas como modelo de simulación aproximado. El archivo Blender, GLB y colisiones se generan juntos desde el contrato métrico; los límites de precisión de E02 siguen vigentes.

Se construyeron los 40 paños, seis puertas con pivotes y tiradores, cinco ventanas con antepechos y dinteles, celosía de logia y paso abierto cocina–estar. Los tres dormitorios, baño longitudinal y logia separada conservan sus contornos. Los achurados, sanitarios y muebles de la referencia no generan paredes. Se añadió el piso en L, terraza gris separada, cielo, losa, pasillo común y masas opacas de vecinos y tres plantas superiores T6 de contexto. Alturas, detalle de carpintería, límites de terraza y extensión del edificio son supuestos identificados.

La superficie se midió sobre los triángulos superiores del pavimento GLB: 77,1000016 m², diferencia +0,4400016 m² respecto a 76,66; dentro de la tolerancia ±0,5 m² comunicada. Superficie útil separada en el contrato. Esta comprobación no acredita un perímetro oficial ni convierte área exterior en útil.

La comparación de los 40 muros de Blender y GLB con sus caras fuente dio errores de generación inferiores a 0,001 mm. Se produjo superposición sobre planta nativa, ortográfica renderizada y dos isométricas opuestas; ambas se revisaron visualmente sin recortar el volumen. Esa precisión de intercambio no es precisión de la referencia: el control gráfico máximo permanece en 12,073 mm, superior a la meta inicial de 10 mm. V02 exacta no se declara aprobada.

Las bisagras conservan el lado y sentido de T11. Se mantiene su desplazamiento normal al muro; solo el extremo longitudinal se ajusta al marco y holgura supuestos. Desplazamiento máximo: 28 mm, incluido el caso de logia cuya hoja gráfica excedía el vano. Los barridos y recorridos físicos completos se comprueban en E05 y se repetirán con muebles.

GLB: 165 mallas, 277720 bytes en esta revisión. Las huellas de Blender, GLB y colisiones coinciden; se verifican seis pivotes y presencia de techo, corredor, vecinos y tres masas superiores. Hay 121 proxies estáticos; las hojas móviles tienen sus registros separados. La marca ocular de Blender está a 1,600000024 m; el POV del controlador corresponde a E05. Tipos TypeScript correctos.

Evidencias: validation/e04/{geometry-check,orthographic-check,glb-check}.json y sus PNG. Fuentes: blender/DepartamentoT7.blend y blender/scripts/build-apartment.py. Continuar E05 antes de amueblar.
