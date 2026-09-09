# Tareas del simulador T7

Actualizado: 9 de septiembre de 2026. T01–T10 completadas; T11 es la siguiente tarea.

Esta es la lista de seguimiento principal del nuevo proyecto `simulador-t7`.

Plan y criterios: `PLAN_MAESTRO_T7.md`. Los códigos V01–V15 se refieren a sus pruebas de validación.

Regla de trabajo: tomar el primer pendiente cuyas dependencias estén satisfechas, realizarlo, verificarlo y registrar evidencia antes de marcarlo. No completar una casilla solo porque esté planificada. Si cambia su fuente, reabrir las comprobaciones afectadas. Mantener los mismos IDs en GitHub.

Seguimiento remoto: [12 etapas en GitHub Issues](https://github.com/BenjaAranda/los-altos-algarrobo-t7/issues). Cada etapa contiene las mismas tareas y casillas de esta lista. Después de actualizarla, sincronizar y comprobar con `scripts/sync-github-tasks.mjs`, según `SEGUIMIENTO_GITHUB.md`.

## E00. Planificación completada

- [x] P01. Localizar el PDF original y confirmar su extensión de 42 páginas. Evidencia: revisión local del PDF.
- [x] P02. Leer y revisar visualmente la página 20, incluida planta, isométrica y encabezado de superficie.
- [x] P03. Registrar diferencias entre solicitud y lámina: 76,66/76,80; edificada/útil; mobiliario D2; armarios; terraza.
- [x] P04. Examinar la página 16 para definir contexto de edificio sin reutilizar otro proyecto.
- [x] P05. Verificar Blender por ejecución de versión y comprobar el estado visible de la instalación Unreal.
- [x] P06. Definir ruta Blender → GLB/colisiones → Unreal y web, más la alternativa Pixel Streaming.
- [x] P07. Definir etapas, dependencias, inventario y pruebas de cierre en el plan maestro.
- [x] P08. Guardar plan y lista de tareas; dejar explícitamente pendientes todas las tareas de implementación.

## E01. Proyecto independiente

Dependencia: E00. Hito: estructura y destinos nuevos preparados.

- [x] T01. Crear la carpeta nueva `simulador-t7` y llevar una copia de estos documentos a su carpeta de documentación; preservar las referencias originales. Evidencia: carpeta `simulador-t7/docs`, copias inicialmente verificadas por SHA-256 y PDF original con la misma huella registrada en el plan.
- [x] T02. Inicializar el sitio con las herramientas de Sites y fijar dependencias compatibles; comprobar una compilación mínima. Evidencia: `web/`, versiones y archivo de bloqueo coherentes, compilación y tipos correctos, lint del código propio correcto, respuesta local HTTP 200 y auditoría final sin vulnerabilidades reportadas. Ver `VALIDACION_T02.md` para alcance y avisos del catálogo generado.
- [x] T03. Preparar estructura de arquitectura, Blender, Unreal, activos y validación; configurar exclusiones y almacenamiento de binarios grandes. Evidencia: carpetas y documentación creadas, `.gitignore`, `.gitattributes`, Git local con LFS y 55 comprobaciones de reglas correctas. Ver `VALIDACION_T03.md`, `VALIDACION_T03.json` y `ALMACENAMIENTO.md`.
- [x] T04. Verificar autenticación GitHub, disponibilidad de nombre y visibilidad; crear el repositorio nuevo en BenjaAranda y registrar su URL real. Evidencia: [repositorio privado nuevo](https://github.com/BenjaAranda/los-altos-algarrobo-t7), propietario e ID comprobados por API, remoto `origin` vinculado y conexión Git correcta. Ver `VALIDACION_T04.md` y `GITHUB_REPOSITORY.json`. La subida inicial corresponde a T06.
- [x] T05. Registrar un sitio nuevo, conservando su identificador para todas las actualizaciones; documentar acceso previsto. Evidencia: ID persistido en `web/.openai/hosting.json`, sitio consultado y acceso privado solo para el propietario, sin versiones ni despliegues. Ver `VALIDACION_T05.md` y `SITE_REGISTRATION.json`.
- [x] T06. Crear seguimiento de tareas en GitHub Projects si está disponible, conservar IDs y subir el estado inicial al repositorio. Evidencia: primera revisión subida y comprobada; 12 issues por etapa con P01–P08 y T01–T70. GitHub Projects rechazó la creación por `INSUFFICIENT_SCOPES`; se usa Issues con la autenticación disponible. Ver `VALIDACION_T06.md`, `GITHUB_TRACKING.json` y `SEGUIMIENTO_GITHUB.md`.

## E02. Interpretación y medidas

Dependencia: E00. Hito: plano calibrado y cuestiones geométricas resueltas antes de cerrar arquitectura.

- [x] T07. Extraer y archivar referencias de planta e isométrica sin alterar el original; comprobar su resolución y procedencia. Evidencia: `references/derived/p20-t7/`, planta nativa de 1536 × 813 px, isométrica de 915 × 826 px, composición anotada y página completa; píxeles/bytes nativos comprobados y huella del PDF intacta. Ver `VALIDACION_T07.md` y el manifiesto de referencias. La calibración métrica sigue pendiente.
- [x] T08. Clasificar trazos: muros, vanos, hojas, mobiliario, equipamiento, cotas, tramas y espacios libres. Evidencia: 89 grupos en nueve familias, catálogo con procedencia y confianza en `architecture/classification/`, atlas visual en `references/derived/t08-clasificacion/` y referencias intactas. Se probaron las nueve familias y la comparación de fondos; 12 registros quedan provisionales para su resolución posterior. Ver `VALIDACION_T08.md`. Los localizadores están en píxeles y no son geometría de construcción.
- [x] T09. Inventariar las cotas y espesores legibles, su posición en el plano y confianza; buscar en el PDF medidas complementarias. Evidencia: `architecture/measurements/`, 58 registros con fuente, recorte, unidad y confianza; 14 cotas locales, ocho menciones de 15 cm, 28 códigos, cuatro menciones de superficie y cuatro referencias complementarias. Revisión general de las 42 páginas y ampliaciones técnicas, tres láminas de lectura y referencias intactas. Ver `VALIDACION_T09.md`. Las unidades locales inferidas y cinco lecturas medias/bajas quedan señaladas; T10 y el cierre dimensional siguen pendientes.
- [x] T10. Fijar origen, ejes y escala mediante referencias horizontales y verticales, con puntos independientes de control. Evidencia: `architecture/calibration/`, escala uniforme de 0,008459347583241785 m/px, origen interior inferior izquierdo de D1 y matrices directa/inversa. Tres cotas de ajuste, diez tramos de control y cuatro círculos comprobados en ambos ejes; máximo residuo seleccionado de 4,586 mm y dependencias entre controles explícitas. Tres láminas y tabla en `references/derived/t10-calibracion/`; fuentes intactas. Ver `VALIDACION_T10.md`. Calibración de trabajo con sensibilidad documentada; no cierra superficie, alturas ni validación dimensional global.
- [ ] T11. Registrar todos los muros, esquinas, retranqueos y vanos; para cada puerta, soporte, ancho, bisagra y sentido de apertura.
- [ ] T12. Confirmar baño longitudinal y ducha al fondo; distinguir áreas de maniobra y sanitarios de paredes; confirmar separación de logia.
- [ ] T13. Calcular por separado área de cómputo, áreas útiles y terraza; resolver 76,66 frente a 76,80 y edificada frente a útil sin distorsionar la planta.
- [ ] T14. Registrar alturas, antepechos, dinteles, espesores de losa y borde de terraza faltantes como datos documentados o supuestos explícitos.
- [ ] T15. Fijar contexto de Torre A/primer piso como propuesta o corregirlo con evidencia; cerrar informe de calibración y pendientes dimensionales.

## E03. Datos y prueba de intercambio

Dependencia: E01 y medidas base de E02. Hito: intercambio mínimo consistente.

- [ ] T16. Definir datos en metros con IDs y fuente por recinto, muro y vano, sin coordenadas duplicadas en el navegador.
- [ ] T17. Crear escena Blender métrica con colecciones separadas de arquitectura, equipamiento, decoración, referencias y colisiones.
- [ ] T18. Preparar exportación de prueba con regla de 1 m, marca ocular de 1,60 m, muro y puerta con bisagra.
- [ ] T19. Cargar la prueba en web, confirmar orientación y escala y aplicar collider que respete el vano.
- [ ] T20. Implementar el manifiesto y comprobación de revisión común para Blender, exportaciones y colisiones; reservar comprobación Unreal para su instalación operativa.

## E04. Arquitectura y edificio

Dependencia: E02 y E03. Hito: arquitectura comprobada sin muebles.

- [ ] T21. Modelar perímetro y pavimentos con terraza separada; crear todos los muros respetando caras, ejes y espesores.
- [ ] T22. Abrir cada vano y construir puertas, marcos, ventanas, dinteles y antepechos con sus medidas registradas.
- [ ] T23. Completar los tres dormitorios y circulaciones; comprobar acceso en extremo superior derecho sin reflejar la planta.
- [ ] T24. Completar baño longitudinal, cocina, estar/comedor y logia separada; revisar especialmente ausencia de tabiques falsos.
- [ ] T25. Añadir piso continuo, losa/cielo, pasillo común, vecinos opacos y pisos superiores de contexto; documentar límites provisionales.
- [ ] T26. Producir superposición ortográfica y tabla de desviaciones; corregir la fuente hasta pasar V01–V04.
- [ ] T27. Revisar isométricas desde lados opuestos y referencia; pasar V05 y guardar hito estructural versionado.

## E05. Recorrido básico

Dependencia: E04. Hito: todo el departamento recorrible antes de decorar.

- [ ] T28. Crear colliders por suelo, muro, vano, ventana y límite; evitar cajas que tapen puertas o huecos válidos.
- [ ] T29. Implementar cápsula, gravedad, física fija, movimiento, mirada y cámara a 1,60 m; normalizar movimiento diagonal.
- [ ] T30. Implementar apertura desde ambos lados, pivote común y barrido seguro de hojas; comprobar umbrales.
- [ ] T31. Implementar pausa, liberación del puntero y reinicio al acceso; inicio y reanudación en posición válida.
- [ ] T32. Recorrer acceso–cada recinto–acceso, probar esquinas, vidrios, marcos y límites; pasar V07–V09 en arquitectura vacía.
- [ ] T33. Guardar rutas de prueba y evidencias del hito; registrar defectos sin ocultarlos con reinicios automáticos.

## E06. Mobiliario, recinto por recinto

Dependencia: E05. Hito: inventario exacto y circulación conservada.

- [ ] T34. Dormitorio 1: cama matrimonial adosada, veladores y TV enfrentada; comprobar volumen y accesos antes de avanzar.
- [ ] T35. Dormitorio 2: una cama, un velador y ningún escritorio ni cama adicional; comprobar volumen y accesos.
- [ ] T36. Dormitorio 3: cama individual y velador; comprobar volumen y accesos.
- [ ] T37. Completar armario de dos puertas de cada dormitorio: hojas, tiradores, zócalo, coronación, jambas y remates del muro; comprobar abiertos/cerrados.
- [ ] T38. Baño: sanitarios, apoyos y ducha accesible al fondo; conservar giro, transferencias y recorrido longitudinal.
- [ ] T39. Cocina: muebles y equipos completos; comprobar que ningún equipo invade baño, huecos o paso.
- [ ] T40. Estar: sofá y TV directamente enfrentados, sin bloquear circulación.
- [ ] T41. Comedor: mesa y sillas; comprobar aproximación, sillas recogidas y posición de uso.
- [ ] T42. Logia: lavadero y lavadora; comprobar acceso, puerta y separación del baño.
- [ ] T43. Ejecutar V06–V08 y V11 con todo el mobiliario; corregir penetraciones, hojas y pasos antes de pasar al acabado.

## E07. Materiales, luz y ambientación

Dependencia: E06. Hito: escena terminada visualmente y con circulación comprobada.

- [ ] T44. Aplicar materiales PBR coherentes, UV a escala y acabado gris provisional de terraza; revisar normales y transparencias.
- [ ] T45. Configurar iluminación y sombras con techo y edificio presentes; evitar fugas y exposición que oculte errores.
- [ ] T46. Añadir alfombras, plantas, lámparas, cuadros, cojines y accesorios sin obstruir muebles ni rutas.
- [ ] T47. Repetir interferencias y recorridos afectados por decoración; obtener planta e isométricas de la versión amueblada.

## E08. Unreal Engine

Dependencia: E03 para prueba mínima; E07 para integración final. Instalación necesaria para cerrar, sin bloquear tareas independientes.

- [ ] T48. Revalidar instalación de Unreal, abrir proyecto nuevo, fijar versión y comprobar guardado; si sigue instalándose, registrar pendiente y continuar E09.
- [ ] T49. Importar la prueba de escala de T18; medir 100 cm y altura ocular de 160 cm, orientación y pivote sin doble conversión.
- [ ] T50. Importar departamento y contexto de la misma revisión; reconstruir colisiones e interacciones a partir de los mismos datos.
- [ ] T51. Configurar materiales/iluminación Unreal y personaje de recorrido; mantener geometría sincronizada con Blender.
- [ ] T52. Comparar dimensiones y vistas; recorrer todas las estancias en Unreal y guardar evidencia V04–V11.
- [ ] T53. Guardar proyecto y comprobar reapertura; documentar importación/actualización y subir el hito con sus activos reproducibles.

## E09. Web final y optimización

Dependencia: E07 y E05. Hito: simulador completo, medido y preparado para revisión final.

- [ ] T54. Optimizar GLB web, materiales y texturas; conservar IDs, pivotes y escala; mantener GLB de intercambio compatible con Unreal.
- [ ] T55. Cargar GLB y colliders de forma atómica y comprobar su revisión; añadir progreso, reintento y estado de error útil.
- [ ] T56. Finalizar controles en español, ayuda, pausa, reinicio, pantalla completa y táctiles; priorizar la escena en la pantalla.
- [ ] T57. Añadir modos planta/isométrica que restauren techo, vecinos y posición segura al volver al recorrido.
- [ ] T58. Medir FPS, memoria y carga en dispositivos identificados; ajustar calidad y resolver V12–V14.
- [ ] T59. Probar modificación controlada y reexportación; verificar que web y Unreal reciben geometría y colisiones de la misma revisión, V10.

## E10. Validación de entrega

Dependencia: E08 y E09. Hito: informe completo sin pendientes críticos.

- [ ] T60. Generar evidencias finales de V01–V05: plano superpuesto, isométricas, superficie, escala y POV.
- [ ] T61. Cerrar V06, V07 y V11: inventario exacto, cero penetraciones y barridos correctos; revisar cada requisito del usuario.
- [ ] T62. Cerrar V08–V09: recorrido completo y casos adversos en versión final; ninguna ruta depende de reiniciar para salir.
- [ ] T63. Cerrar V10 y V12–V14: sincronización, rendimiento, carga e interfaz; identificar límites de dispositivos realmente probados.
- [ ] T64. Corregir fallos en su fuente, regenerar y repetir pruebas afectadas; producir informe con archivos y revisiones reales.

## E11. GitHub, publicación y entrega

Dependencia: E10. Hito: V15 superada y todos los entregables accesibles.

- [ ] T65. Compilar producción de la revisión validada y comprobar que incluye modelo, texturas y colliders correctos.
- [ ] T66. Actualizar documentación, tareas, activos y reporte en el repositorio GitHub nuevo; registrar commit de entrega.
- [ ] T67. Guardar y desplegar esa misma versión en Sites con el acceso registrado; esperar resultado exitoso real.
- [ ] T68. Abrir la URL publicada y comprobar carga, manifiesto y recorrido esencial; resolver fallos antes de entregar.
- [ ] T69. Entregar URL, repositorio, Blender, proyecto Unreal, GLB, colliders, informe y controles de uso; registrar cómo reproducir y actualizar.
- [ ] T70. Marcar completo únicamente tras verificar los entregables; mantener las siguientes correcciones dentro de este mismo proyecto y repositorio.

## Continuación concreta

La siguiente tarea de implementación es T11: registrar muros, caras, esquinas, retranqueos y vanos; para cada puerta, soporte, ancho, bisagra y sentido de apertura. Reutilizar la transformación de `architecture/calibration/t10-calibracion.json` y las imágenes intactas de `references/derived/p20-t7/`. Registrar puntos geométricos nuevos, sin extruir cajas de clasificación T08 o recortes de textos T09. Respetar la incertidumbre de la calibración, marcar dimensiones inferidas y resolver remates y carpinterías ambiguos donde haya evidencia. Los códigos F y los componentes genéricos de p23-p24 no son espesores del T7. No convertir tramas del baño, líneas de ducha, mobiliario ni arcos en tabiques; conservar la separación de logia. Mantener los pendientes de T08/T09 hasta su resolución específica y no forzar el perímetro para producir 76,66 m². La raíz Git es `simulador-t7/` y `origin` apunta al repositorio privado `BenjaAranda/los-altos-algarrobo-t7`. El seguimiento de E02 corresponde a la issue #3; actualizar esta lista, sincronizar sus casillas y subir la revisión con evidencia. Reutilizar el sitio registrado en `web/.openai/hosting.json`, privado y sin publicar. El PDF original permanece en la carpeta superior. La topología detallada del baño/logia, alturas y superficies siguen en T12-T15. Si Unreal sigue instalándose, continuar por tareas independientes y conservar E08 pendiente.
