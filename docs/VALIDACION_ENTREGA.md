# DepartamentoT7 · Validación de entrega

Fecha: 12 de septiembre de 2026. Revisión compartida: `3eed66c9dd62ba833406046c8f68ca7710ce3516de9e1333030586aa22b68c71`. Blender 5.2.1 LTS, Unreal 5.8.2 y aplicación web compilada. Publicación y comprobación en producción completadas; evidencia en `validation/e11/publication-check.json`.

## Arquitectura y alcance dimensional

La planta de la página 20 conserva orientación, acceso superior derecho, tres dormitorios, baño longitudinal con ducha al fondo, logia independiente, cocina y estar/comedor. La terraza conserva un acabado gris provisional. Se incluye pasillo común, vecinos opacos, cielo y tres niveles superiores de contexto. Las vistas de inspección ocultan 25 objetos de contexto y los restauran al recorrer.

El polígono exterior construido mide **77,10 m²**, diferencia **+0,44 m²** respecto de 76,66 m²; cumple la tolerancia de ±0,50 m² indicada por el usuario. La superficie útil calculada por separado es **69,4276 m²**. La terraza se excluye de ambas. No se presenta la superficie exterior como superficie útil.

La reconstrucción sigue un plano rasterizado, sin cotas completas. El residuo máximo de referencias gráficas es **12,073 mm**: supera el objetivo inicial de 10 mm de V02. Este objetivo queda **con salvedad documentada**, no aprobado falsamente. Las caras generadas reproducen la fuente geométrica con error máximo de 0,000711 mm; esa precisión informática no elimina la incertidumbre del plano. Alturas no acotadas y edificio circundante son supuestos identificados. No es un levantamiento para construcción ni una certificación normativa de accesibilidad.

## Matriz de comprobaciones

| Control | Resultado y evidencia |
|---|---|
| V01 · Plano | Superposición y 40 muros comparados en `validation/e04/`; planta sin reflejar, vanos y caras cotejados. |
| V02 · Medidas | Salvedad: máximo gráfico 12,073 mm frente al objetivo de 10 mm. `orthographic-check.json` conserva `nominal_10mm_source_goal_met: false`. |
| V03 · Superficie | 77,10 m² exteriores, diferencia +0,44 m²; útil separada y terraza excluida. |
| V04 · Escala y ojos | Metros en Blender/GLB/web; centímetros en Unreal. Web 1,600 m; Unreal 160–160,000122 cm. |
| V05 · Vistas | Dos isométricas opuestas de Blender, ortográfica, doce capturas reales de Unreal; D2 corregido y ventana despejada. |
| V06 · Interferencias | Cero penetraciones no justificadas de los 28 conjuntos comprobados; cuatro cuadros apoyados en muros, sin cubrir vanos. `validation/e10/furniture-check.json`. |
| V07 · Hojas | Doce barridos de puertas/armarios, parada ante visitante. Desplazamiento observado 0,103 mm en web y 0 cm en Unreal. |
| V08 · Recorrido | Diez destinos y regreso, armarios cerrados y abiertos: veinte rutas web y veinte Unreal. Recorrido interactivo de navegador por los diez destinos en la revisión previa; la revisión final cambia un cuadro, conserva arquitectura y repite todas las rutas físicas. |
| V09 · Adversos | Esquinas, vidrios, FPS bajos, puerta junto al jugador y 40 viajes contra contacto cerrado. Cinco viajes adicionales en navegador, sin reinicio ni atasco. |
| V10 · Sincronización | Revisiones y hashes en `validation/e10/delivery-manifest.json`; prueba aislada de desplazamiento de 10 mm en `validation/e09/revision-probe.json`. |
| V11 · Mobiliario | Inventario contrastado abajo, volúmenes y circulaciones comprobados. |
| V12 · Rendimiento | Aproximadamente 69,91 FPS, percentil 95 de 14,5 ms en equipo de referencia; sin medición física móvil. |
| V13 · Carga | Escena utilizable 1,43 s a 50 Mbps locales sin caché; activos esenciales 1,61 MB, recursos transferidos 5,59 MB. |
| V14 · Interfaz | Navegador Chromium integrado y pantalla móvil emulada de 390 × 844. Ayuda, controles, pausa, retorno, pantalla completa, calidad y restauración de contexto comprobados. Chrome/Edge independientes no disponibles; no se declaran probados. |
| V15 · Publicación | [Sitio privado publicado](https://departamentot7.benjaaranda.chatgpt.site); carga, revisión, colisión, retroceso, puerta y vista isométrica comprobados en producción. |

## Inventario solicitado

- Dormitorio 1: cama matrimonial adosada, veladores, TV enfrentada y armario empotrado de dos hojas.
- Dormitorio 2: una cama, un velador y armario de dos hojas; sin escritorio ni segunda cama.
- Dormitorio 3: cama individual, velador y armario de dos hojas.
- Los tres armarios incluyen hojas independientes, tiradores, zócalo, coronación, jambas y remates del muro.
- Estar: sofá y TV enfrentados. Comedor con mesa y sillas; cocina equipada; baño continuo, apoyos y ducha al fondo; logia con lavadora y lavadero.
- Alfombras, plantas, luminarias, cuadros, cojines y accesorios revisados con el mobiliario. No se interpretaron líneas de mobiliario o ducha como tabiques.

La puerta del baño abre según el plano y puede ocupar la circulación occidental cuando permanece abierta. La ruta cierra la hoja después de usarla; no se altera la arquitectura para ocultar ese comportamiento.

## Rendimiento observado y límites

Windows 11, Ryzen 7 8845HS, 15,31 GB RAM y RTX 4070 Laptop. Chromium integrado, ANGLE Direct3D11, ventana 1280 × 800, lienzo 1280 × 592,67 y DPR 1, calidad estándar. Se ejecutaron 20 órdenes de tres segundos: 60 s de movimiento dentro de 89,43 s de observación, incluidos intervalos entre tres tandas. La muestra acumulada de 99,27 s incluye la preparación inicial. No se presenta como un minuto de marcha ininterrumpida.

Memoria JavaScript observada: 40,27 MB antes y 24,20 MB después; la recolección de memoria explica que disminuya. No incluye GPU ni memoria nativa. La red fue un proxy local con presupuesto compartido de 50 Mbps, caché deshabilitada y transferencia sin compresión. No reproduce latencia de Internet ni rendimiento de un teléfono. `validation/e10/browser-final.json` conserva medidas y posiciones.

## Correcciones y reproducción

El cuadro de D2 se movió desde la ventana al muro lateral en Blender y se regeneraron Blender, GLB, datos y Unreal. El atasco esporádico al retroceder de una puerta cerrada se reprodujo con una prueba de 40 viajes; la corrección solo acepta un paso si el barrido continuo de la cápsula, el destino libre y el soporte de piso lo permiten. La prueba y las rutas completas pasaron después del cambio.

Unreal se importa y guarda primero; en un proceso nuevo configura colisiones y movilidad, evitando actualizaciones pendientes de Chaos. La segunda reapertura no necesitó reparaciones. La compilación web y tipos terminaron con código 0. En Windows se utilizó la compilación npm del proyecto porque el ayudante de Sites no resolvió su lanzador npm; se empaqueta ese mismo resultado válido.

Abrir las fuentes y reproducir según `README.md`, `web/README.md` y `VALIDACION_E08.md`. Los informes antiguos conservan sus revisiones históricas; el manifiesto de entrega enumera las comprobaciones de la revisión actual.
