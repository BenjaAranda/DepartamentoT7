Beta 2 de los paquetes descargables del simulador DepartamentoT7. Conserva el mismo modelo y las mismas colisiones y funciona sin conexión después de la descarga.

Elige el ZIP correspondiente a tu sistema, extráelo y abre `DepartamentoT7.exe` (Windows) o `DepartamentoT7` (macOS/Linux). Mantén abierta su ventana mientras recorres el departamento. Lee `LEEME.txt` dentro del ZIP para controles y requisitos.

En Windows el programa ahora abre Chrome cuando está disponible, luego Edge y por último el navegador predeterminado. Para usar este último deliberadamente, se puede iniciar `DepartamentoT7.exe -browser=default`. Si el navegador mide menos de 25 FPS durante unos cinco segundos, activa «Modo ligero»; Información muestra GPU y resolución efectiva. Esta medida no garantiza buen rendimiento si el navegador está limitado por su configuración o utiliza renderizado por software.

La automatización comprobó la compilación web, el manifiesto del modelo, los tipos y los tests del servidor local en Windows, macOS Intel, macOS Apple Silicon y Linux. La experiencia gráfica completa se verificó manualmente en Windows; el renderizado 3D en hardware macOS/Linux necesita revisión en equipos de esos sistemas. Los ejecutables no están firmados digitalmente y pueden provocar advertencias del sistema operativo. Verifica cada descarga con `SHA256SUMS.txt`.
