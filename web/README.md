# Web del simulador T7

Base web independiente de Los Altos de Algarrobo, creada con el inicializador oficial de Sites 0.3.0 y el complemento shadcn.

Simulador amueblado con vistas de inspección, recorrido físico, puertas y armarios interactivos. Three.js/React Three Fiber renderiza el GLB optimizado; Rapier usa los colliders exportados desde la misma fuente de Blender.

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

## Validación actual

Desde `web/`:

```powershell
node scripts/optimize-model.mjs
node scripts/check-web-model.mjs
node scripts/check-apartment-assets.mjs
node scripts/check-loader.mjs
node scripts/check-furniture.mjs ../validation/e10
node scripts/check-walk.mjs ../validation/e10
node scripts/check-walk.mjs ../validation/e10/wardrobes-open --wardrobes-open
node scripts/check-walk-adverse.mjs ../validation/e10
node scripts/check-contact-soak.mjs
npm run lint
npm run typecheck
npm run build
npm start -- --port 3001
```

Detener la vista de producción antes de reconstruir en Windows, porque puede mantener bloqueado `dist/`. No sirve la carpeta de Blender en el sitio. La web carga `public/models/manifest.json`, verifica hashes y revisión, y publica el GLB comprimido de 1,50 MB. Conserva también el GLB original para intercambio.

Las mutaciones de escena Three.js y cámara suceden en efectos y callbacks de cuadro; se excluye únicamente ese adaptador de la regla de inmutabilidad del compilador React. Las reglas restantes, tipos y compilación siguen activas. El plano raster conserva sus píxeles originales intencionalmente.

Informe de resultados, hardware y límites: `../docs/VALIDACION_ENTREGA.md`. No se certifica rendimiento móvil con la emulación de tamaño de pantalla.
