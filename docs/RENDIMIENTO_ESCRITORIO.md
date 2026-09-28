# Rendimiento del paquete de escritorio

## Síntoma y diagnóstico · 28 de septiembre de 2026

Se informó menos de 10 FPS al abrir el paquete descargable, mientras la versión local del proyecto funcionaba bien. El ejecutable Go solo entrega la misma web y los mismos recursos a `127.0.0.1`; el navegador ejecuta la escena. La revisión de geometría y colisiones observada en las comparaciones fue `02abe9c3`.

En Windows, la asociación predeterminada para HTTP de este equipo es `Opera GXStable`. Antes de este cambio, el ejecutable pedía a Windows abrir el navegador predeterminado. Un navegador distinto puede elegir otra GPU, otra escala de píxeles o aplicar límites propios. Opera GX ofrece límites de CPU y RAM en GX Control, pero **no se confirmó cuál ajuste produjo el caso informado**.

| Prueba controlada | Navegador y GPU | Resultado observado |
|---|---|---|
| Web estática local, vista de recorrido | Chromium automatizado, RTX 4070 Laptop, 1280 × 800 CSS, DPR 1 | ~163 FPS en una ventana de cinco segundos |
| Ejecutable beta 1 descargado, misma vista y navegador | Mismos navegador, GPU, tamaño y DPR | ~163 FPS en una ventana de cinco segundos |
| Ejecutable beta 1, Opera GX en perfil temporal limpio | RTX 4070 Laptop, DPR 1 | ~93 FPS en una prueba activa de tres segundos; no representa el perfil habitual del usuario |
| Simulación de carga extrema sobre la nueva web | Chromium, ~9 FPS provocados deliberadamente | Cambió a «Modo ligero» y mostró aviso visible |

Estas mediciones no demuestran el rendimiento del perfil habitual de Opera GX ni el de otros equipos. Sí descartan una pérdida general causada por servir la web desde el ejecutable, bajo el mismo navegador y la misma GPU. Las cifras de FPS de pruebas breves varían con la carga del sistema; se usan para contrastar rutas, no como garantía de un mínimo.

## Corrección de la beta 2

- Windows abre Chrome cuando está disponible, después Edge, y utiliza la asociación predeterminada si no encuentra ninguno. La opción `-browser=default` conserva la elección del sistema.
- La web calcula FPS en una ventana de cinco segundos. Si la calidad estándar baja de 25 FPS, activa automáticamente «Modo ligero» y lo informa.
- «Modo ligero» limita el DPR del lienzo a 1 y desactiva las sombras dinámicas. El usuario puede alternarlo manualmente desde Ayuda.
- Información muestra GPU, DPR efectivo y FPS recientes. Esto permite distinguir entre GPU dedicada, integrada o renderizado por software.
- El modelo, la revisión, las puertas, la física y los colliders no se modificaron.

## Validación y límite

Se comprobaron `go test`, `go vet`, lint, tipos, compilación estática, manifiesto y hashes. El nuevo ejecutable Windows cargó la revisión esperada, abrió Chrome instalado, permitió caminar a altura ocular de 1,60 m y no mostró errores de navegador. En una simulación de ~9 FPS se observó el aviso y el cambio de calidad; la vista isométrica siguió siendo legible.

La mejora automática puede reducir el coste de renderizado, pero no puede reparar un navegador que renderiza por software o tiene una restricción de CPU/GPU impuesta por el sistema. Para cerrar el caso informado hay que comprobar los FPS y el campo GPU en Información en el equipo y perfil de navegador donde ocurrió.
