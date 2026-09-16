# DepartamentoT7

Proyecto independiente del simulador 3D del Departamento Tipo T7. El plan y el estado de ejecución se mantienen en [docs/TODO_T7.md](docs/TODO_T7.md).

Repositorio privado: [BenjaAranda/DepartamentoT7](https://github.com/BenjaAranda/DepartamentoT7). Fuentes de Blender, contenido Unreal, GLB, colisiones y aplicación web versionados. Las [12 etapas de seguimiento](https://github.com/BenjaAranda/DepartamentoT7/issues) conservan los IDs y casillas del plan; GitHub Projects requiere permisos que la conexión actual no tiene. Ver [docs/VALIDACION_T06.md](docs/VALIDACION_T06.md) y [cómo mantener el seguimiento](docs/SEGUIMIENTO_GITHUB.md).

**[Abrir simulador publicado](https://departamentot7.benjaaranda.chatgpt.site)** · Acceso privado con la cuenta propietaria de ChatGPT. Publicación y recorrido comprobados en producción el 12 de septiembre de 2026. [Entrega y archivos](docs/ENTREGA.md) · [Evidencia E11](validation/e11/publication-check.json).

## Organización

| Carpeta | Contenido |
|---|---|
| `architecture/` | Medidas, ejes, muros, vanos, recintos y fuentes de cada dato. |
| `blender/` | Modelo editable, texturas de autoría y herramientas de exportación. |
| `unreal/T7/` | Proyecto Unreal 5.8.2 con nivel, materiales, personaje y código propios. |
| `unreal/scripts/` | Importación y comprobaciones de Unreal. |
| `assets/interchange/` | GLB de intercambio exportado desde Blender. |
| `assets/colliders/` | Proxies y datos compartidos de colisión. |
| `references/` | Referencias de trabajo y derivados identificados. |
| `web/` | Aplicación Sites, dependencias y recursos publicados. |
| `validation/` | Evidencias de arquitectura, recorrido, rendimiento y entrega. |
| `docs/` | Plan, to-dos, decisiones y validación de cada tarea. |

Los archivos `.gitkeep` conservan carpetas vacías; no representan modelos, medidas ni validaciones realizadas.

## Trabajo con los archivos grandes

Se emplea Git LFS para fuentes de Blender, contenido Unreal, texturas de autoría e intercambio binario. El código, la documentación y los datos JSON se conservan en Git normal. Los recursos bajo `web/public/` también permanecen en Git normal para que la web reciba los archivos completos.

Antes de trabajar en otra máquina, instalar Git LFS y, desde la raíz de este proyecto, ejecutar:

```powershell
git lfs install --local
git lfs pull
```

Consultar [ALMACENAMIENTO.md](docs/ALMACENAMIENTO.md) para las reglas, límites de trabajo y distribución de entregables. La configuración local de LFS se aplica al repositorio; no cambia la configuración global de otros proyectos.

## Desarrollo web

Desde `web/`, usar `npm ci` y `npm run dev`. La base y sus comprobaciones están descritas en [web/README.md](web/README.md).

Demo estática independiente: `npm run build:static`, `npm run check:static` y `npm run preview:static`, desde `web/`. [Plan de publicación pública y revisión de seguridad](docs/PUBLICACION_PUBLICA.md). El destino GitHub Pages está pendiente de habilitación; el enlace privado anterior sigue siendo la publicación vigente.

Blender, GLB, colliders y Unreal se sincronizan según [el plan maestro](docs/PLAN_MAESTRO_T7.md). La calibración de trabajo T10, el [trazado 2D T11](architecture/plan/README.md) y la [distribución de baño/logia T12](architecture/topology/README.md) están registrados; se completó el análisis de superficies y alturas en [E02](docs/VALIDACION_E02.md), con aproximación exterior de 77,10 m² y supuestos explícitos. El estado comprobado de cada etapa figura en los to-dos.

## Modelo y recorrido

Abrir `blender/DepartamentoT7.blend` en Blender 5.2.1 LTS o `unreal/T7/DepartamentoT7.uproject` en Unreal 5.8.2. El GLB de intercambio está en `assets/interchange/`; los colliders compartidos, en `assets/colliders/`. [Informe de entrega](docs/VALIDACION_ENTREGA.md), [evidencias actuales](validation/e10/delivery-manifest.json) y [guía Unreal](docs/VALIDACION_E08.md).

En web: W A S D o flechas para caminar, ratón/arrastre para mirar, E para puertas, Esc para pausa. Ayuda permite activar botones en pantalla y modo ligero. Planta e isométrica permiten inspeccionar; el contexto del edificio se restaura al recorrer. En Unreal: W A S D, ratón, E, Esc y R para volver al acceso.

Superficie exterior aproximada 77,10 m² (+0,44 respecto a 76,66); útil 69,43 m² y terraza excluida. Ojos a 1,60 m. La incertidumbre gráfica máxima es 12,073 mm; las alturas no acotadas y el contexto del edificio son supuestos documentados.

## Actualizar sin desincronizar

1. Corregir los datos métricos de `architecture/` o los generadores de mobiliario/acabado en `blender/scripts/`.
2. Ejecutar Blender en segundo plano con `--python blender/scripts/build-apartment.py`; genera fuente, GLB, colliders y vistas.
3. Desde `web/`, ejecutar el optimizador y las comprobaciones descritas en su README.
4. Ejecutar `unreal/run-t7.ps1 import`, `check` y `capture`; comparar la misma revisión en todos los informes.
5. Repetir solo las comprobaciones afectadas, compilar la web, actualizar GitHub y publicar el mismo sitio registrado. No cambiar archivos generados de forma aislada.

Corrección posterior: [puertas, ejes de apertura y clóset D1](docs/CORRECCION_PUERTAS.md).
