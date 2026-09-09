# T03: estructura y almacenamiento preparados

Fecha: 8 de septiembre de 2026. Resultado: T03 completada.

## Organización creada

Se prepararon `architecture/`, `blender/`, `unreal/`, `assets/`, `references/` y `validation/`, con documentación de su función. Se reservaron 17 subcarpetas para herramientas, texturas, proyecto Unreal, intercambio, colliders, referencias, evidencias y recursos web. Las carpetas vacías contienen únicamente `.gitkeep`; no se generaron archivos que simulen ser modelos o resultados de validación.

La aplicación permanece en `web/` y el seguimiento principal en `docs/TODO_T7.md`. El PDF original sigue fuera de la raíz del repositorio nuevo, en la carpeta de trabajo superior.

## Configuración realizada

- `.gitignore` en la raíz, con exclusiones de cachés, archivos de recuperación Blender, compilaciones y estado local de Unreal, credenciales y entregables voluminosos.
- `.gitattributes`, con finales de línea definidos para el código y tratamiento LFS de fuentes y binarios de intercambio.
- Exclusión explícita del filtro LFS para todo `web/public/`, de modo que los recursos del navegador se conserven como archivos completos.
- Archivos `.env.example` permitidos tanto en la raíz como en la web; los archivos de valores privados permanecen excluidos.
- Repositorio Git local inicializado en `simulador-t7/`, rama `main`, sin commits ni remotos. GitHub corresponde a T04.
- Git LFS 3.7.1 disponible y configurado con `--local`, incluidos filtros requeridos y hook de pre-push. No se modificó su configuración global.
- Política de almacenamiento documentada en `ALMACENAMIENTO.md`, incluyendo distribución de videos y paquetes como entregables de versión.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| Rutas incluidas/excluidas | 37 casos correctos mediante `git check-ignore --no-index`. |
| Filtros de almacenamiento | 18 casos correctos mediante `git check-attr filter`. |
| Raíz de Git | Coincide con `simulador-t7/`, sin absorber la carpeta superior. |
| Configuración local LFS | `filter.lfs.required=true`; hook de pre-push con llamada a Git LFS. |
| Remotos | Ninguno, coherente con T04 pendiente. |
| Archivos actuales candidatos a Git | Ninguno supera el umbral de revisión de 25 MiB. |

Los casos comprueban tanto archivos que deben excluirse como archivos que deben conservarse: contenido y código de plugins Unreal, mapas, materiales, `.uproject`, configuración, fuentes Blender, paquete de dependencias web, manifiestos, ejemplos de entorno y evidencias. También comprueban que GLB, BIN, HDR y JSON destinados al navegador no reciben el filtro LFS, incluidos archivos en subcarpetas.

Los resultados por ruta están en `VALIDACION_T03.json`. Se usan nombres representativos para comprobar las reglas; esos nombres no implican la existencia de modelos todavía pendientes de crear.

No se repitió la compilación web de T02: en T03 solo cambiaron organización, documentación y reglas de versionado, sin cambios en el código o las dependencias de la aplicación. Tampoco se validó aún la sincronización de modelos ni una transferencia de objetos LFS a GitHub: no existen esos modelos ni el remoto.

## Siguiente tarea

T04: comprobar autenticación y disponibilidad del nombre, definir visibilidad y crear el repositorio nuevo de BenjaAranda. Reutilizar este repositorio local y verificar las condiciones de almacenamiento LFS de la cuenta antes de subir binarios grandes.
