# T04: repositorio GitHub nuevo y vinculado

Fecha: 8 de septiembre de 2026, America/Santiago. Resultado: T04 completada.

## Destino confirmado

- Repositorio: [BenjaAranda/los-altos-algarrobo-t7](https://github.com/BenjaAranda/los-altos-algarrobo-t7).
- ID de GitHub: `1362108111`.
- Visibilidad: **privado**, elegida como configuración inicial; requiere acceso autorizado a esa cuenta o repositorio.
- Creación confirmada: `2026-09-09T02:22:00Z` (8 de septiembre en Chile).
- Remoto local: `origin`, con URL `https://github.com/BenjaAranda/los-altos-algarrobo-t7.git` tanto para lectura como para escritura.
- Raíz local: `simulador-t7/`. Rama local y rama predeterminada del remoto: `main`.

Se creó un repositorio vacío propio de este proyecto. La primera confirmación de cambios y subida de archivos corresponde a T06. Por ello, la rama remota aún no contiene commits. El proyecto anterior no se utilizó ni se modificó.

## Evidencia de verificación

| Comprobación | Resultado |
|---|---|
| Cuenta autenticada | `GET /user` confirmó `BenjaAranda`; autenticación existente de Git Credential Manager. |
| Disponibilidad del nombre | Consulta autenticada del destino devolvió HTTP 404 antes de crearlo. |
| Creación | `POST /user/repos` devolvió HTTP 201 e ID `1362108111`. |
| Lectura posterior | `GET /repos/BenjaAranda/los-altos-algarrobo-t7` devolvió HTTP 200, mismo ID, propietario correcto y `private=true`. |
| Permisos informados por GitHub | Lectura, escritura y administración habilitadas para la cuenta autenticada. La primera escritura Git se comprobará en T06. |
| Vínculo local | `origin` apunta al repositorio nuevo; no había otros remotos que reemplazar. |
| Conexión Git autenticada | `git ls-remote origin` terminó con código 0 y cero referencias, coherente con un repositorio recién creado sin commits. |

Los identificadores, respuestas resumidas y fechas de comprobación están en [GITHUB_REPOSITORY.json](GITHUB_REPOSITORY.json). Las credenciales se usaron en memoria mediante el gestor existente; no se guardaron en archivos, documentación ni URL del remoto.

La comprobación Git desde la sesión de Windows del usuario detectó que la carpeta recién creada pertenece al usuario del entorno aislado de Codex. Se verificó su ruta y se utilizó una excepción `safe.directory` limitada a ese comando y a esta carpeta. No se cambió la configuración global. Para operaciones Git posteriores ejecutadas fuera del entorno aislado puede ser necesario aplicar la misma excepción puntual.

## Almacenamiento y alcance

La API de cuenta no proporcionó el plan ni el saldo de almacenamiento de Git LFS. La documentación vigente indica 10 GiB de almacenamiento y 10 GiB de ancho de banda incluidos para Free y Pro, pero **eso no acredita el saldo disponible de esta cuenta**. Comprobar su consumo y límites efectivos antes de la primera subida de binarios LFS; no se contrataron servicios ni capacidad adicional. [Facturación de Git LFS](https://docs.github.com/en/billing/concepts/product-billing/git-lfs).

No hay modelos ni objetos LFS que transferir en esta tarea. Se conserva la estrategia de [ALMACENAMIENTO.md](ALMACENAMIENTO.md).

T04 solo cambia el destino Git y documentación. Las comprobaciones de compilación, tipos y código de T02 siguen siendo las últimas comprobaciones de la aplicación; no se repitieron porque no cambió el código ni sus dependencias. El registro del sitio pertenece a T05, el seguimiento y la subida inicial a T06, y la publicación validada a E11.

## Siguiente tarea

T05: registrar un sitio nuevo para la aplicación `web/`, guardar su identificador persistente y documentar el acceso previsto. Reutilizar el repositorio e identificadores ya registrados, sin crear duplicados.
