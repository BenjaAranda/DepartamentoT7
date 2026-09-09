# T02: base del sitio creada y comprobada

Fecha: 8 de septiembre de 2026. Resultado: T02 completada.

## Alcance realizado

Se creó `web/` dentro de `simulador-t7/` con el inicializador oficial `@openai/create-sites@0.3.0`, npm y el complemento shadcn. Se utilizó una subcarpeta vacía porque el inicializador no admite una carpeta que ya contenga los documentos de T01. La raíz de `simulador-t7/` sigue siendo el proyecto general.

La base contiene React, TypeScript, Vinext, Vite e integración de Sites/Cloudflare. Se configuraron nombre del paquete, idioma español, metadatos del T7, estilos base y una página que informa claramente de que el recorrido aún está en preparación. Esta página es un estado inicial de desarrollo, no una vista previa del departamento modelado.

Quedaron registrados `.node-version`, `packageManager`, `.npmrc` con `save-exact=true` y `package-lock.json`. Se verificó que las versiones directas son exactas y coinciden con el archivo de bloqueo. El README de `web/` documenta instalación, desarrollo y comprobaciones.

## Entorno y versiones finales

| Componente | Versión |
|---|---|
| Node | 26.8.1 |
| npm | 11.19.0 |
| React / React DOM / React Server DOM | 19.2.8 |
| Vinext | 1.0.0-beta.9 |
| Vite | 8.2.2 |
| TypeScript | 5.9.3 |
| Sites Vite Plugin | 0.2.0 |
| Cloudflare Vite Plugin | 1.54.6 |
| Wrangler | 4.130.0 |
| Cloudflare Workers Types | 5.20260908.1 |

Las demás versiones están en `web/package.json` y el árbol completo está en `web/package-lock.json`.

SHA-256 del archivo de bloqueo validado:

`01e85f544d8d369f81a5127bca4569cfccd380765fa215373d490759e7408f03`

## Comprobaciones realizadas

| Comprobación | Resultado y límite |
|---|---|
| Instalación final | Terminó correctamente; 552 paquetes auditados. |
| Auditoría incluida en la instalación final | 0 vulnerabilidades reportadas en ese momento. |
| `npm ls --depth=0` | Finalizó sin dependencias directas inválidas o faltantes. |
| Coherencia de versiones | Dependencias directas exactas y coincidentes con `package-lock.json`. |
| `npm run build` | Compilación final completa, con salida `dist/server/index.js`, `dist/server/wrangler.json` y recursos del cliente. |
| `npm run typecheck` | Sin errores; incluye el código propio y el catálogo generado. |
| `npm run lint` | Sin errores en el código propio y la configuración, según el alcance detallado abajo. |
| Arranque de desarrollo | `npm run dev` inició el sitio en el puerto local anunciado. |
| Respuesta local | `GET http://localhost:3000/` devolvió HTTP 200 y `text/html; charset=utf-8`. |
| Cierre del proceso | Se detuvo el servidor de comprobación al terminar. |

El código servido no se inspeccionó como prueba visual. No se realizaron pruebas de arquitectura, cámara, colisiones ni recorrido 3D en esta etapa. Esas pruebas corresponden a los modelos e interacciones futuros.

## Correcciones de dependencias

La instalación original de la plantilla reportó 11 vulnerabilidades, 8 de severidad alta. Se consultaron los avisos y las dependencias entre versiones, y se actualizaron únicamente los paquetes afectados y sus requisitos de compatibilidad. No se utilizó `--force` ni `--legacy-peer-deps`.

La última incidencia provenía de Sharp 0.35.2, fijado por Miniflare. Se aplicó un `override` limitado a `miniflare → sharp: 0.35.4`, el parche de la misma serie que corrige el aviso. La auditoría final dejó de reportar vulnerabilidades y la compilación y el arranque se comprobaron después de aplicar el parche. Revisar si el override deja de ser necesario al actualizar Miniflare. Referencia: [aviso de Sharp](https://github.com/advisories/GHSA-rgj7-g3m4-5g8c).

## Alcance del análisis y avisos restantes

El catálogo de shadcn viene copiado por el inicializador. Su análisis original informó avisos de accesibilidad, patrones de efectos y expresiones de tipos en componentes que aún no se usan en el simulador. Se conserva ese código como tercero, con revisión separada mediante `npm run lint:vendor`; `lint` excluye únicamente `components/ui/**` y el hook generado `hooks/use-mobile.ts`. Las reglas del código propio siguen activas. La comprobación de TypeScript y la compilación sí incluyen el catálogo completo.

Al incorporar cada control, se deberá comprobar su uso y accesibilidad en contexto. No se declara que el catálogo completo pase lint ni que la interfaz final haya superado V14.

Persisten avisos del proveedor que no impidieron el resultado: deprecación de `module.register()` bajo Node 26, clasificación estática de ruta como desconocida en Vinext y advertencias de npm sobre la declaración de scripts de instalación de esbuild/workerd. No se alteró la política de scripts. En el arranque local, la descarga opcional de `Request.cf` falló por restricción de red y el emulador utilizó su valor predeterminado; la ruta respondió correctamente.

## Continuación

T03 es la siguiente tarea: organizar arquitectura, Blender, Unreal, activos y evidencias junto a `web/`, con exclusiones y estrategia para binarios grandes. T04 conserva la creación del repositorio GitHub y T05 el registro del sitio remoto. No hay todavía identificador de sitio en `web/.openai/hosting.json`. La publicación sigue reservada a E11 tras validar el simulador completo.
