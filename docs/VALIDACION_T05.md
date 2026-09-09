# T05: sitio nuevo registrado

Fecha: 8 de septiembre de 2026, America/Santiago. Resultado: T05 completada.

Se registró un sitio independiente para la aplicación `web/`, con el título **Departamento Tipo T7 · Los Altos de Algarrobo**. Su identificador es `appgprj_6aa0c4d0ff688191a8421e732e9b5d35` y debe reutilizarse en todas las actualizaciones.

## Configuración conservada

Antes de registrar, `web/.openai/hosting.json` no tenía `project_id`. Se creó el sitio una vez y se incorporó el ID exacto de la respuesta mediante escritura atómica, preservando `d1: null` y `r2: null`. El registro no inicializó otra aplicación ni reutilizó el proyecto anterior.

La dirección prevista devuelta al crear es `https://los-altos-algarrobo-t7.benjaaranda.chatgpt.site`. **No es todavía una web publicada ni un recorrido disponible.** La consulta posterior no devolvió `expected_url`; se conserva la dirección de la respuesta de creación con su procedencia explícita.

## Acceso y verificación

Una consulta posterior al ID creado confirmó:

| Comprobación | Resultado |
|---|---|
| Identidad | Mismo ID, título y nombre de sitio. |
| Estado administrativo | `active`. Este estado no significa que exista una publicación. |
| Rol de la cuenta actual | `owner`. |
| Acceso | `custom`, con una única cuenta autorizada. |
| Grupos y visitantes externos | Cero grupos de trabajo, cero grupos de organización y cero visitantes externos. |
| Editores adicionales | Cero. |
| Versiones guardadas | Cero. |
| URL publicada y vista previa remota | Ambas nulas. |

El acceso inicial previsto es privado, solo para el propietario. No se cambió la audiencia ni se enviaron invitaciones. La entrega de E11 usará ese acceso mientras no haya una instrucción de cambiarlo y deberá verificarlo de nuevo al publicar.

Los datos de creación y comprobación están en [SITE_REGISTRATION.json](SITE_REGISTRATION.json); el ID que usarán las herramientas reside en `web/.openai/hosting.json`. La credencial temporal de escritura recibida se mantuvo únicamente en memoria. En la etapa de publicación, obtener una credencial nueva para **este mismo ID** si la anterior no está disponible o ha expirado; no volver a crear el sitio.

## Continuidad

El repositorio GitHub principal sigue siendo [BenjaAranda/los-altos-algarrobo-t7](https://github.com/BenjaAranda/los-altos-algarrobo-t7), con raíz en `simulador-t7/`. La aplicación que se preparará para Sites está en `web/`; el procedimiento de publicación debe conservar esa distinción y vincular la copia web con la revisión principal, según `ALMACENAMIENTO.md`.

No cambió el código ni las dependencias web. Se comprobó la persistencia del manifiesto y su coherencia con el sitio remoto. La compilación validada de T02 no se presenta como una versión desplegada; la compilación y publicación del simulador completo permanecen en E11.

Siguiente tarea: T06, preparar seguimiento en GitHub Projects si está disponible y subir el estado inicial al repositorio, conservando los IDs de tareas.
