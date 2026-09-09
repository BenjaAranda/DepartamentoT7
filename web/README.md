# Web del simulador T7

Base web independiente de Los Altos de Algarrobo, creada con el inicializador oficial de Sites 0.3.0 y el complemento shadcn.

Estado de T02: completada; consultar `../docs/VALIDACION_T02.md` para resultados y alcance. El modelo, la física y el recorrido se incorporan en etapas posteriores del plan. La página inicial informa de esa ausencia sin mostrar una reconstrucción ficticia.

## Desarrollo

Ejecutar desde esta carpeta `web/`. La versión de Node usada para validar la base se registra en `.node-version`; usar npm y conservar `package-lock.json`.

```powershell
npm ci
npm run dev
```

## Comprobaciones

```powershell
npm run typecheck
npm run lint
npm run build
```

La compilación utiliza Vinext, Vite y la integración de Sites para Cloudflare. `dist/` es generado y no debe editarse manualmente. Las dependencias directas tienen versiones exactas y `.npmrc` mantiene ese criterio para futuras incorporaciones.

`lint` revisa el código propio y la configuración del sitio. El catálogo generado de shadcn (`components/ui/` y `hooks/use-mobile.ts`) se conserva como código de terceros: el análisis de tipos y la compilación sí lo incluyen. `npm run lint:vendor` permite revisar por separado los avisos originales del catálogo. Al incorporar un control, comprobar su uso y accesibilidad en contexto; la exclusión del catálogo no es una certificación de esos controles.

## Organización

- `app/`: ruta inicial, idioma español, metadatos y estilos.
- `components/ui/`: componentes del inicializador; reutilizarlos al implementar controles.
- `.openai/hosting.json`: configuración de Sites con el identificador remoto registrado en T05; reutilizarlo en todas las actualizaciones.
- `../docs/TODO_T7.md`: seguimiento principal de todas las etapas.
- `../docs/PLAN_MAESTRO_T7.md`: arquitectura y validaciones previstas.

Las carpetas para Blender, Unreal, las medidas y la evidencia quedaron organizadas junto a `web/` en T03. Consultar `../docs/ALMACENAMIENTO.md` para los archivos grandes: todo `public/` se conserva como archivos completos, sin filtros LFS. La publicación está prevista tras validar el simulador completo, en E11.

El sitio quedó registrado en T05 con acceso privado solo para el propietario, sin versiones ni despliegues. Consultar `../docs/VALIDACION_T05.md` y `../docs/SITE_REGISTRATION.json` para la evidencia y la dirección prevista. No confundir el registro con una publicación ni volver a crear el sitio.
