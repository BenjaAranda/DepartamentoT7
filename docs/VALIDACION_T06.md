# T06: estado inicial en GitHub y seguimiento preparado

Fecha: 8 de septiembre de 2026, America/Santiago. Resultado: T06 completada con seguimiento en Issues; Projects no disponible con la autenticación actual.

## Archivos subidos

Se creó y subió la revisión inicial `229027e610fe38c8e593b2ae9ae9a48ff8df50cd` a `main` del [repositorio privado T7](https://github.com/BenjaAranda/los-altos-algarrobo-t7). La consulta de la rama remota confirmó exactamente esa revisión el `2026-09-09T02:44:49.338Z`.

Esta primera revisión contiene 117 archivos: base web, plan, organización de fuentes y evidencias, configuración Git/LFS, registro del sitio y herramienta de seguimiento. El cierre de T06 agrega su informe, mapa de issues y guía de continuidad en una revisión posterior del mismo repositorio.

Antes de subir se revisaron los archivos candidatos y sus tamaños, se comprobaron los cambios preparados con `git diff --cached --check` y se verificó la ausencia de objetos LFS en la revisión. No se encontraron coincidencias de los patrones de credenciales examinados. El PDF original, dependencias descargadas, cachés y herramientas temporales permanecieron fuera del historial. No se subieron modelos ficticios.

## Seguimiento y permisos

La consulta autenticada confirmó la cuenta `BenjaAranda`, el repositorio privado con ID `1362108111` y permiso de administración. El intento de crear un tablero mediante `createProjectV2` devolvió `INSUFFICIENT_SCOPES`: requiere `project`, mientras la conexión tiene `gist`, `repo` y `workflow`. No se creó un tablero ni se modificaron los permisos de la cuenta. La documentación oficial distingue los permisos de consulta y escritura de Projects. [API de Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects).

Se crearon [12 issues por etapa](https://github.com/BenjaAranda/los-altos-algarrobo-t7/issues), desde E00 hasta E11, con los 78 identificadores originales: 8 de planificación y 70 de implementación. No son 78 issues: cada etapa agrupa sus tareas en casillas individuales. La lista local sigue siendo la fuente principal.

El cierre de esta tarea deja P01–P08 y T01–T06 completos: 14 casillas verificadas, 64 pendientes, E00 y E01 cerradas y las otras 10 etapas abiertas. La siguiente es T07 dentro de [E02, issue #3](https://github.com/BenjaAranda/los-altos-algarrobo-t7/issues/3).

## Verificación y continuidad

`scripts/sync-github-tasks.mjs` conserva IDs y números remotos, actualiza solo los bloques administrados, respeta notas externas al bloque y confirma por lectura el contenido y estado tras cada cambio. El modo `--check` verifica la coincidencia sin escribir. Los resultados de sincronización y sus fechas quedan en `GITHUB_TRACKING.json`; el procedimiento está en `SEGUIMIENTO_GITHUB.md`.

La comprobación independiente `--check` terminó con código 0 el `2026-09-09T02:48:39.831Z`: las 12 etapas y las 78 casillas coinciden, con 14 completas y 64 pendientes. La huella del TODO comprobado, en UTF-8 con saltos LF, es `e0df316ea27551f65ca697ce1e605f38b7dfe3ed968b3d01ce7e3746e96944a8`. No quedaron etapas que requirieran otra sincronización. La revisión de sintaxis de la herramienta también terminó sin errores.

La aplicación no cambió en T06. Las pruebas de compilación, tipos y código de T02 conservan su alcance; no se repitieron por cambios de documentación y seguimiento. El sitio registrado en T05 sigue sin publicar; las validaciones arquitectónicas, el modelo y el recorrido aún están pendientes.
