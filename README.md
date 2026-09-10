# Departamento Tipo T7 · Los Altos de Algarrobo

Proyecto independiente del simulador 3D del Departamento Tipo T7. El plan y el estado de ejecución se mantienen en [docs/TODO_T7.md](docs/TODO_T7.md).

Repositorio privado: [BenjaAranda/los-altos-algarrobo-t7](https://github.com/BenjaAranda/los-altos-algarrobo-t7). Estado inicial subido y comprobado en T06. Las [12 etapas de seguimiento](https://github.com/BenjaAranda/los-altos-algarrobo-t7/issues) conservan los IDs y casillas del plan; GitHub Projects requiere permisos que la conexión actual no tiene. Ver [docs/VALIDACION_T06.md](docs/VALIDACION_T06.md) y [cómo mantener el seguimiento](docs/SEGUIMIENTO_GITHUB.md).

El sitio web quedó registrado en T05, con acceso privado solo para el propietario. Sigue sin publicar; su configuración y evidencia están en [docs/VALIDACION_T05.md](docs/VALIDACION_T05.md). La publicación del simulador validado corresponde a E11.

## Organización

| Carpeta | Contenido |
|---|---|
| `architecture/` | Medidas, ejes, muros, vanos, recintos y fuentes de cada dato. |
| `blender/` | Modelo editable, texturas de autoría y herramientas de exportación. |
| `unreal/T7/` | Futuro proyecto Unreal con configuración, contenido y código propios. |
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

Blender, GLB, colliders y Unreal se sincronizarán según [el plan maestro](docs/PLAN_MAESTRO_T7.md). La calibración de trabajo T10, el [trazado 2D T11](architecture/plan/README.md) y la [distribución de baño/logia T12](architecture/topology/README.md) están registrados; quedan por cerrar superficies y alturas antes del modelo 3D. El estado comprobado de cada etapa figura en los to-dos.
