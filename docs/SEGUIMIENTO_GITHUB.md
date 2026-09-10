# Seguimiento de las tareas T7

La fuente principal es `docs/TODO_T7.md`. En [GitHub Issues](https://github.com/BenjaAranda/DepartamentoT7/issues) hay una lista por etapa, con los mismos IDs P01–P08 y T01–T70. Una casilla marcada indica una tarea verificada; una issue se cierra cuando todas sus casillas están completas. Al reabrir una tarea local, la sincronización reabre también su etapa.

El tablero GitHub Projects no se creó: la autenticación actual carece del permiso `project`, según la respuesta `INSUFFICIENT_SCOPES`. No se ampliaron permisos ni se solicitó otra credencial. Puede incorporarse un tablero más adelante si queda disponible, conservando este seguimiento.

## Mapa de etapas

| Etapa | Seguimiento |
|---|---|
| E00 · Planificación | [#1](https://github.com/BenjaAranda/DepartamentoT7/issues/1) |
| E01 · Proyecto independiente | [#2](https://github.com/BenjaAranda/DepartamentoT7/issues/2) |
| E02 · Interpretación y medidas | [#3](https://github.com/BenjaAranda/DepartamentoT7/issues/3) |
| E03 · Datos y prueba de intercambio | [#4](https://github.com/BenjaAranda/DepartamentoT7/issues/4) |
| E04 · Arquitectura y edificio | [#5](https://github.com/BenjaAranda/DepartamentoT7/issues/5) |
| E05 · Recorrido básico | [#6](https://github.com/BenjaAranda/DepartamentoT7/issues/6) |
| E06 · Mobiliario | [#7](https://github.com/BenjaAranda/DepartamentoT7/issues/7) |
| E07 · Materiales, luz y ambientación | [#8](https://github.com/BenjaAranda/DepartamentoT7/issues/8) |
| E08 · Unreal Engine | [#9](https://github.com/BenjaAranda/DepartamentoT7/issues/9) |
| E09 · Web final y optimización | [#10](https://github.com/BenjaAranda/DepartamentoT7/issues/10) |
| E10 · Validación de entrega | [#11](https://github.com/BenjaAranda/DepartamentoT7/issues/11) |
| E11 · Publicación y entrega | [#12](https://github.com/BenjaAranda/DepartamentoT7/issues/12) |

Los números y tareas asociadas están registrados en `GITHUB_TRACKING.json`. No crear duplicados ni modificar otro repositorio para continuar.

## Actualización al terminar una tarea

1. Guardar su evidencia y marcar únicamente las casillas verificadas en `docs/TODO_T7.md`.
2. Desde `simulador-t7/`, ejecutar `node scripts/sync-github-tasks.mjs --apply` para actualizar GitHub y el mapa local.
3. Ejecutar `node scripts/sync-github-tasks.mjs --check`; debe terminar con código 0 y `all_match: true`. Este modo solo lee GitHub y no escribe archivos.
4. Revisar los cambios, confirmarlos y subirlos a `origin/main`; comprobar que la revisión remota coincide con la local. La sincronización de casillas no sube archivos por sí sola.

La herramienta obtiene la sesión existente de Git Credential Manager en memoria y confirma cuenta, ID del repositorio, privacidad y permisos antes de actuar. Puede requerir ejecutarse fuera del entorno aislado para acceder al gestor de Windows. No guarda credenciales ni las introduce en URLs.

Solo reemplaza el bloque delimitado por marcadores `t7-stage` dentro de cada issue. Las notas fuera del bloque y los comentarios permanecen intactos. El título se establece al crear la issue; no se sobrescribe después. Detecta IDs repetidos, etapas vacías, duplicados remotos o diferencias con los números guardados y se detiene para revisarlos. Reutiliza los elementos existentes al reanudar una ejecución parcial.

La huella `last_sync.source_sha256` corresponde al texto UTF-8 del TODO con saltos LF. Las fechas y resultados son instantáneas de verificación, no un servicio automático en segundo plano.

Para comandos Git de red ejecutados desde Windows fuera del entorno aislado, puede ser necesaria la excepción puntual de propietario descrita en `VALIDACION_T04.md`, limitada a la ruta del proyecto. No usar excepciones globales para cualquier carpeta.
