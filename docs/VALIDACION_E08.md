# E08 · Integración Unreal Engine

Revisión geométrica: `3eed66c9dd62ba833406046c8f68ca7710ce3516de9e1333030586aa22b68c71`. Unreal Engine 5.8.2, Windows 11, MSVC 14.44.35228, Windows SDK 10.0.22621 y .NET Framework SDK 4.8. Compilación C++ final aprobada.

El nivel `/Game/T7/Apartment` contiene el departamento completo y su contexto. El importador comprobó los 40 muros contra las caras originales, 499 mallas y doce pivotes. Se generan 248 colisiones desde el mismo JSON que usa la web. Conversión única: glTF `(x,y,z)` metros → Unreal `(x,z,y) × 100` centímetros.

El personaje recorre veinte rutas de ida y regreso, con armarios cerrados y abiertos, mediante CharacterMovement. Doce hojas completaron sus barridos; ante el visitante activo, la puerta se detuvo con desplazamiento horizontal observado de 0 cm. La cámara permaneció entre 160 y 160,000122 cm sobre el piso. Evidencia: `validation/e08/runtime-check.json`, 15.405 cuadros de simulación. Estas son pruebas automatizadas del controlador real; no se presentan como un recorrido manual por el editor.

Se conservaron materiales/texturas del GLB, doce luminarias, luz de cielo y luz direccional. La exposición fija se ajustó a 32 en la escala de brillo de este proyecto para preservar detalles interiores. Los exteriores en inspección reciben menos luz. Doce capturas reales de Unreal muestran planta, isométrica y diez ubicaciones del recorrido, sin interfaz superpuesta: `validation/e08/views/`. Las cámaras de evidencia se sitúan a 160 cm en los puntos previamente recorridos; no sustituyen la prueba de desplazamiento. La planta no está reflejada, el baño es continuo hasta la ducha y la logia sigue separada.

La reimportación se divide en dos procesos: guardar primero las mallas importadas, reabrir después y configurar su perfil persistente `NoCollision` y movilidad. Esto evita modificar cuerpos mientras Interchange conserva actualizaciones pendientes de Chaos. La física pertenece exclusivamente a los proxies compartidos. La segunda reapertura no requirió reparar perfiles. Tras guardar y volver a abrir, las 499 mallas conservan ese perfil y los doce pivotes están presentes, sin reparaciones pendientes. La ejecución y captura finales terminaron normalmente, sin errores ni avisos `ensure`. Evidencia: `reopen-check.json` y `capture-check.json`.

## Reproducción

Recuperar Git LFS y abrir `unreal/T7/DepartamentoT7.uproject` con Unreal 5.8. Compilar con `unreal/run-t7.ps1 build`; el SDK de .NET Framework debe estar instalado además de C++ para escritorio.

`unreal/run-t7.ps1 import` reconstruye el nivel desde el GLB de intercambio y los JSON vigentes. `check` vuelve a abrirlo y ejecuta la prueba física; el resultado se escribe en `unreal/T7/Saved/t7-runtime-check.json`. `capture` genera las doce vistas en `Saved/T7Captures`. `play` inicia el recorrido interactivo. No editar a mano geometría de importación para evitar divergencias; corregir su fuente y reexportar.

Controles: W A S D, ratón, E para puertas, Esc para pausa, R para volver al acceso. No hay salto. El editor y los binarios compilados no se distribuyen dentro de la web: se entrega el proyecto reproducible; el navegador usa la misma arquitectura mediante GLB/Rapier.
