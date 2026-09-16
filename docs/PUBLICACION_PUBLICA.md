# Demo pública · preparación

Destino previsto: `https://benjaaranda.github.io/DepartamentoT7/`. No considerar esta URL publicada hasta completar D04–D07.

El usuario autorizó el 16 de septiembre de 2026 hacer público `BenjaAranda/DepartamentoT7` y revisar la seguridad. GitHub Pages sustituye la propuesta inicial de Cloudflare Pages porque el repositorio público permite alojamiento gratuito sin otra cuenta.

## Seguimiento

- [x] D01. Compilación estática independiente, reutilizando el simulador y sin servidor de aplicación.
- [x] D02. Paquete permitido: modelo optimizado, colisiones, manifiesto, referencia, icono y aplicación compilada; comprobaciones de hashes y rutas.
- [x] D03. Compilación, tipos, lint, pruebas de carga y puertas y revisión inicial de navegador sin autenticación.
- [ ] D04. Resolver el hallazgo histórico de seguridad, hacer público el repositorio y habilitar Pages con HTTPS.
- [ ] D05. Ejecutar satisfactoriamente el flujo de publicación desde main y verificar sus permisos.
- [ ] D06. Añadir el enlace público confirmado al README, About y entrega.
- [ ] D07. Comprobar la URL publicada sin sesión, modelos, recorrido y errores; registrar el despliegue.

Preparación verificada: [informe](../validation/public-demo/preflight.json) y [ejecución de GitHub Actions aprobada](https://github.com/BenjaAranda/DepartamentoT7/actions/runs/35161341069). La compilación en GitHub terminó correctamente; el despliegue se omitió deliberadamente al seguir privado el repositorio.

## Compilar y probar

Desde `web/`:

```sh
npm ci
npm run build:static
npm run check:static
npm run preview:static
```

Abrir `http://127.0.0.1:4173/DepartamentoT7/`. La entrada `static/index.html` define el prefijo para que modelo y referencia funcionen bajo la ruta del repositorio. `T7_BASE_PATH=/` permite compilar para otro alojamiento en la raíz. La escena, física y recursos mantienen una única fuente compartida con la versión Sites.

La variante estática utiliza fuentes del sistema y no descarga fuentes ni ejecuta scripts de terceros. La política CSP permite WebAssembly y blobs de las texturas internas del GLB. No utiliza cookies de aplicación, cuentas, analítica ni servicios de datos.

## Publicación

`.github/workflows/pages.yml` ejecuta instalación reproducible, auditoría de dependencias, lint, tipos, pruebas de carga/puertas, compilación y validación del paquete. Solo publica desde main cuando el repositorio es público. Los pull requests se comprueban con permisos de lectura y no se despliegan. Las acciones están fijadas a hashes completos y Dependabot propone actualizaciones semanales.

El trabajo de despliegue utiliza el token efímero de GitHub y OIDC; no requiere claves personales. Se debe configurar el entorno `github-pages` para admitir únicamente main. Los archivos de autoría permanecen en el repositorio y no se incluyen en el sitio; no se descargan objetos LFS en CI, ya que `web/public` contiene archivos Git normales.

Para volver a una versión anterior, revertir mediante un nuevo commit el cambio que causó el problema y dejar que se publique el estado validado; no sobrescribir manualmente modelos sueltos.

## Revisión de seguridad

- Gitleaks 8.30.1 descargado desde su repositorio oficial y comprobado contra su archivo de checksums.
- Revisados los 34 commits existentes y todas las referencias locales, además del contenido de las 12 issues y el paquete estático.
- Dependencias: cero vulnerabilidades reportadas por `npm audit` al preparar esta versión.
- Demo e issues: cero hallazgos de secretos en el escaneo.
- GitHub no tenía ejecuciones de Actions, artefactos, releases ni tags que auditar adicionalmente.
- Hallazgo histórico real: `SecurityToken` del Android File Server en `unreal/T7/Config/DefaultEngine.ini`, introducido en `615376b`. La configuración se retiró y el plugin quedó desactivado en `40e4d58`, pero el valor permanece en el historial. No es una credencial de GitHub o Cloudflare. No se imprime ni copia a este informe. Se prepara una copia saneada del historial antes de cambiar visibilidad.
- Una credencial generada de prerender de Vinext existe únicamente en `web/dist/server`, ignorado por Git; el paquete estático excluye por construcción toda salida del servidor.
- Ver [SECURITY.md](../SECURITY.md) para el alcance de CSP y los límites de cabeceras en GitHub Pages.

Cambiar la visibilidad hará públicos código, modelos, referencias derivadas y metadatos de commits. El PDF original y el trabajo local permanecen excluidos. La revisión automatizada reduce riesgos, pero no constituye una garantía de ausencia de cualquier vulnerabilidad.

Se preparó una copia local del historial con el valor sensible eliminado: 35 commits escaneados, cero hallazgos y árbol final idéntico al commit de implementación. El historial original tiene respaldo local excluido de Git. Sustituir el historial remoto requiere autorización específica para una actualización forzada; no se ha realizado. Antes del cambio público se deben revisar también las nuevas referencias de pull requests creadas por Dependabot, habilitar alertas/protección de secretos disponibles y limitar el entorno Pages a main. No basta con borrar el token en un commit nuevo.
