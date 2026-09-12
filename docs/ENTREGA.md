# DepartamentoT7 · Entrega

[**Abrir simulador**](https://departamentot7.benjaaranda.chatgpt.site) · [Repositorio GitHub](https://github.com/BenjaAranda/DepartamentoT7)

Publicado el 12 de septiembre de 2026. Sitio y repositorio privados. Para entrar en la web, usar la cuenta propietaria con «Continuar con ChatGPT».

Actualización publicada: puertas de logia y dormitorios 1/2 corregidas, baño y dormitorio 2 abren hacia dentro y clóset D1 cerrado al inicio. Blender, GLB, colisiones y Unreal sincronizados. Ver [corrección y pruebas](CORRECCION_PUERTAS.md) y [publicación verificada de la versión 2](../validation/door-fix/release.json). La evidencia E11 enlazada abajo corresponde a la publicación inicial.

## Archivos

- [Modelo editable Blender](../blender/DepartamentoT7.blend).
- [Proyecto Unreal Engine](../unreal/T7/DepartamentoT7.uproject) y [guía para abrirlo y actualizarlo](VALIDACION_E08.md).
- [GLB de intercambio](../assets/interchange/departamento-t7.glb), [GLB web optimizado](../web/public/models/departamento-t7-web.glb) y [colliders](../assets/colliders/departamento-t7.json).
- [Informe de validación y límites](VALIDACION_ENTREGA.md), [manifiesto de archivos](../validation/e10/delivery-manifest.json), [publicación comprobada](../validation/e11/publication-check.json) y [tareas](TODO_T7.md).

Para descargar las fuentes grandes desde GitHub, recuperar Git LFS; el README describe el proceso. La fuente Blender se abre con Blender 5.2.1 LTS. El proyecto Unreal incluye contenido y C++; abrir con Unreal 5.8.2 y compilar según la guía. La web usa el modelo compartido mediante Three.js y Rapier; no necesita instalar Unreal para recorrer.

## Uso

Pulsar «Recorrer departamento». W A S D o flechas para moverse, ratón o arrastre para mirar, E para abrir/cerrar y Esc para pausar. Ayuda activa controles en pantalla y modo ligero. «Volver al acceso» reinicia voluntariamente la posición. «Planta 3D» e «Isométrica» permiten inspeccionar la distribución. En Unreal se dispone también de R para regresar al acceso.

Superficie exterior aproximada: **77,10 m²**, diferencia **+0,44 m²** dentro de la tolerancia acordada. Superficie útil: **69,43 m²**, terraza excluida. Altura ocular **1,60 m**. Precisión gráfica máxima **12,073 mm**; no se oculta la diferencia respecto al objetivo inicial de 10 mm. Las pruebas de rendimiento identifican equipo y emulación; no certifican teléfonos físicos ni navegadores independientes no disponibles.

Las futuras correcciones se mantienen en este mismo proyecto, repositorio y sitio. Cambiar la fuente, regenerar, comprobar las pruebas afectadas y publicar la misma revisión conforme al README.
