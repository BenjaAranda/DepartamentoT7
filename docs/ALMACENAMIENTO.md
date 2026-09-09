# Almacenamiento y distribución de archivos

Configuración definida en T03, 8 de septiembre de 2026. `.gitignore` define exclusiones; `.gitattributes` define tratamiento de texto y LFS. La aplicación web conserva además su `.gitignore` específico.

## Qué se conserva y dónde

| Archivos | Estrategia |
|---|---|
| Código, planes, medidas, JSON, configuración Unreal y manifiestos | Git normal, para poder revisar cambios. |
| `.blend`, `.uasset`, `.umap`, `.ubulk`, `.uexp` | Git LFS. |
| GLB, BIN y FBX de intercambio o proxies fuera de `web/public/` | Git LFS. |
| EXR, HDR, PSD, TIFF y las texturas de autoría PNG/JPEG/TGA/WebP bajo `blender/textures/` | Git LFS. |
| Todo `web/public/`, incluidos GLB y texturas optimizadas | Archivos completos en Git normal; el filtro LFS está expresamente desactivado en esa ruta. |
| Informes y capturas de validación de tamaño razonable | Git normal. |
| Compilaciones empaquetadas de Unreal, ZIP de entrega y grabaciones completas | Entregables de versión; producción local en `deliverables/` o `validation/recordings/`, excluidos del historial. |
| Cachés, dependencias descargadas, archivos de recuperación y credenciales locales | Excluidos. |

Git LFS guarda punteros en el historial y mantiene los binarios por separado; por eso se requiere LFS en las máquinas que abran las fuentes. Los recursos servidos directamente por la web deben contener los bytes reales del modelo o textura. [Descripción oficial de Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).

## Límites de trabajo

Los presupuestos iniciales del plan para la web siguen vigentes: hasta 25 MB transferidos para activos esenciales y 50 MB para la escena completa. Son objetivos del proyecto que se medirán durante optimización, no cuotas de GitHub.

Revisar cualquier archivo individual de Git normal que supere 25 MiB antes de subirlo. Si es un recurso web, reducir, dividir o cambiar su distribución con una solución comprobada; no trasladarlo a LFS sin preparar también la carga real del navegador. Si es una fuente editable, aplicar una regla LFS precisa antes de incorporarla al historial.

GitHub advierte sobre archivos de Git normal mayores de 50 MiB y bloquea los mayores de 100 MiB. Los paquetes de entrega pueden distribuirse mediante Releases. Las cuotas y límites de LFS dependen de la cuenta; no contratar capacidad adicional automáticamente. [Límites de archivos de GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

En T04 se confirmó el repositorio privado nuevo y se revisaron las condiciones documentadas de LFS: Free y Pro incluyen 10 GiB de almacenamiento y 10 GiB de ancho de banda. La API no informó el plan ni el consumo de esta cuenta; esas cantidades no representan su saldo disponible. Comprobar la cuota efectiva antes de subir los primeros binarios LFS. No existen objetos LFS ni se contrató capacidad en T04. Ver `VALIDACION_T04.md` y la [documentación de facturación de LFS](https://docs.github.com/en/billing/concepts/product-billing/git-lfs).

## Preparación de una copia o entrega

1. Usar una sola raíz de repositorio, `simulador-t7/`; `web/` es la aplicación dentro de ese proyecto.
2. Instalar Git LFS para esta copia con `git lfs install --local` y recuperar objetos con `git lfs pull` cuando exista un remoto.
3. Comprobar que `.blend`, contenido Unreal y binarios de intercambio se materializaron; un puntero de texto no es un modelo válido.
4. Revisar que `web/public/` contiene archivos completos y que no se empaquetan punteros LFS en el sitio.
5. Al publicar con Sites, empaquetar el sitio desde `web/`. Si el servicio requiere un repositorio cuyo árbol raíz sea la aplicación, generar una copia de publicación de esa subcarpeta, conservando el vínculo con la revisión del repositorio principal; no mover `docs/`, Blender ni Unreal al directorio público. El procedimiento concreto se comprobará al integrar la publicación.
6. Comprobar tamaños, dependencias de texturas y el manifiesto común de Blender, GLB, colliders y Unreal antes de generar los entregables.

El GLB optimizado y los colliders deben publicarse como un mismo conjunto de revisión. La estrategia de almacenamiento no sustituye la comprobación de sincronización de T20 y V10.

## Referencias y exclusiones

El PDF original permanece fuera del repositorio nuevo, en la carpeta de trabajo superior. `references/originals/` admite copias locales sin subirlas automáticamente. `references/derived/` queda disponible para los resultados de extracción y calibración con procedencia documentada.

Unreal: conservar `Content/`, `Config/`, `Source/`, `.uproject` y plugins propios; excluir `Binaries/`, `Intermediate/`, `Saved/` y `DerivedDataCache/`, también dentro de plugins. Documentar por separado cualquier plugin futuro que requiera binarios no regenerables.

Blender: conservar el maestro `.blend`; excluir archivos de recuperación numerados. Web: conservar código y archivo de bloqueo; excluir dependencias, compilaciones y estado local. Los `.env.example` con nombres y valores ficticios sí pueden versionarse; los valores privados deben quedar fuera.
