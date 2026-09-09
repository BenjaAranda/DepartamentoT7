# Proyecto Unreal

`T7/` queda reservado al proyecto Unreal del simulador; `scripts/` a su importación y comprobaciones. El archivo `.uproject` se creará cuando corresponda ejecutar la integración en Unreal.

Versionar `.uproject`, `Config/`, `Content/`, `Source/` y los plugins propios cuando existan. `.uasset`, `.umap` y datos binarios asociados usan LFS. Se excluyen `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, archivos de solución regenerados y estado del editor, también dentro de plugins.

No usar esta exclusión para omitir una dependencia necesaria: si en el futuro se incorpora un plugin que solo se distribuye como binario, documentar y comprobar su mecanismo de instalación o una excepción precisa antes de entregar. Esta tarea no añade plugins de ese tipo.

Unreal recibirá el modelo y los colliders de la misma revisión que la web. La conversión de metros a centímetros se hará una sola vez, con comprobación de 1 m y POV de 160 cm. No corregir muros únicamente en Unreal.
