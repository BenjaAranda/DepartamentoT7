# Seguridad

La demo pública ejecuta el recorrido en el navegador. No tiene cuentas de usuario, formularios, base de datos, claves de API ni servidor de aplicación. No introduzcas credenciales en el código o en los modelos.

Para informar una vulnerabilidad, utiliza **Security → Report a vulnerability** en GitHub. No publiques credenciales ni detalles explotables en una issue pública. Se mantiene la última revisión de `main`; las revisiones históricas no están soportadas.

La publicación admite únicamente recursos estáticos seleccionados. El manifiesto verifica SHA-256 y revisión de geometría/colisiones antes de cargar. Esta comprobación detecta desincronización, no sustituye la confianza en el alojamiento HTTPS.

GitHub Actions usa acciones fijadas por SHA y permisos de lectura durante la compilación. Solo el trabajo de despliegue desde `main` obtiene permisos de Pages/OIDC. Los pull requests no reciben credenciales de despliegue. No se utilizan tokens personales para publicar la demo.

La política CSP permite scripts y conexiones del mismo origen, WebAssembly para la física, imágenes integradas y estilos dinámicos de React. GitHub Pages no permite configurar libremente cabeceras HTTP; la CSP se aplica mediante meta y no implementa `frame-ancestors`. No hay datos privados ni sesiones en la demo.

El servidor de archivos Android de Unreal está desactivado en el proyecto actual. No habilitarlo reutilizando configuraciones históricas: cualquier entorno de depuración Android nuevo debe generar su propia credencial.
