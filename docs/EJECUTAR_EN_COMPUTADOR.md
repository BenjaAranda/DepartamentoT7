# Ejecutar DepartamentoT7 en un computador

## Para quien quiere recorrerlo

Descargar un paquete desde la [primera versión para computador](https://github.com/BenjaAranda/DepartamentoT7/releases/tag/desktop-v0.1.0-beta.1), según el sistema:

| Sistema | Archivo |
|---|---|
| Windows 64 bits | `DepartamentoT7-windows-amd64.zip` |
| Mac con Intel | `DepartamentoT7-macos-intel.zip` |
| Mac con Apple Silicon | `DepartamentoT7-macos-apple-silicon.zip` |
| Linux 64 bits | `DepartamentoT7-linux-amd64.zip` |

Extraer el ZIP completo y abrir `DepartamentoT7.exe` o `DepartamentoT7`. Se inicia el navegador predeterminado; la ventana del programa debe permanecer abierta. Al cerrarla, el servidor local se detiene. El puerto temporal se elige automáticamente. No se requiere instalar el código fuente, Node, Blender o Unreal. La conexión a internet solo se necesita para descargar el ZIP.

Requisitos reales: navegador actual con WebGL2, aceleración gráfica y capacidad para ejecutar programas descargados. No se fija una cantidad de VRAM o versión mínima de sistema que no haya sido medida. Si el navegador no aparece, copiar la dirección local mostrada en la ventana del programa. Si Linux carece de `xdg-open`, usar esa misma dirección. El programa escucha únicamente en `127.0.0.1`, acepta GET/HEAD y no ofrece API de datos ni escritura.

Los ejecutables de esta primera versión no están firmados. Es posible que Windows SmartScreen o macOS adviertan sobre una aplicación desconocida; las políticas de equipos administrados pueden impedir su ejecución. Nunca recomendamos desactivar protecciones del sistema. La identidad de la descarga se puede verificar con `SHA256SUMS.txt` en la misma Release. [Microsoft explica la reputación de aplicaciones descargadas](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation).

## Para mantener el proyecto

La web estática se genera desde `web/` con `T7_BASE_PATH=/` y `npm run build:static`. `scripts/prepare-desktop.mjs` comprueba la revisión y hashes del GLB/colisiones, y copia solo la salida aprobada al directorio incluido en el ejecutable. Go 1.27.1 compila `launcher/cmd/departamentot7` sin módulos externos. `launcher/cmd/packager` crea el ZIP y conserva el permiso de ejecución en macOS/Linux.

El workflow `.github/workflows/desktop-release.yml` compila el sitio una vez, ejecuta pruebas nativas del servidor y crea paquetes en cuatro runners. En una etiqueta `desktop-v*` añade los paquetes y sumas SHA-256 a una GitHub Release preliminar. Una publicación no certifica la aceleración gráfica en todas las GPU; el recorrido 3D completo se probó manualmente en Windows. Antes de declarar estable la versión de macOS/Linux se necesita una prueba gráfica en dispositivos reales de esos sistemas.

La versión Sites y la web estática comparten `web/components/t7` y los recursos de `web/public`; editar ambas por separado desincronizaría el modelo. El PDF original y los archivos de Blender y Unreal no se incluyen en las descargas para usuarios.
