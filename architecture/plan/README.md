# Levantamiento T11

La planta queda registrada en **40 paños, 13 vanos/pasos, seis puertas de recinto y cinco hojas de mobiliario visibles en la fuente**. Se identifican ocho grupos de encuentros y retranqueos, con 106 vértices del borde combinado. El [registro legible](REGISTRO_T11.md) reúne las tablas y las cuestiones aún pendientes.

Los paños se trazan entre caras del raster nativo, separados en encuentros y huecos. No se reutilizan los rectángulos localizadores de T08 como sólidos. Cada paño conserva IDs T08 y, cuando corresponde, lecturas T09; los códigos de tipo no se convierten en espesores. Los nominales de 15 cm se guardan aparte del ancho que se lee en el dibujo.

## Archivos y actualización

- [t11-trazado.json](t11-trazado.json): observaciones de autoría en píxeles, coordenadas compartidas, paños, vanos, pivotes, giros, procedencia y límites. Se edita este archivo para corregir el levantamiento.
- [t11-registro.json](t11-registro.json): resultado generado con caras, ejes, esquinas y bisagras en metros. Reutiliza exclusivamente la transformación de [T10](../calibration/t10-calibracion.json). No editar sus coordenadas a mano.
- [Evidencias visuales y tablas](../../references/derived/t11-trazado/README.md): planta superpuesta, puertas ampliadas, remates, inventarios TSV y controles.
- [Validación T11](../../docs/VALIDACION_T11.md): comprobaciones realizadas y alcance.

Regenerar con `scripts/build-t11-plan.py` usando Python con NumPy y Pillow. El generador comprueba las huellas del PDF, planta y calibración, registra su entrada y exporta los mismos datos métricos para todas las etapas futuras. Los ejes de un paño son puntos medios de sus caras; sus extremos coinciden con la sección dibujada, sin prolongaciones automáticas a ejes vecinos.

## Interpretación y límites

El acceso O01 interrumpe el **borde derecho**, inmediatamente bajo el muro superior. D3 accede mediante O02 junto al extremo del nicho. La puerta P05 del baño abre hacia la circulación superior. O06 comunica cocina con logia, con bisagra derecha. O13 es un paso abierto cocina–estar: no hay marco ni hoja que modelar.

Los 106 vértices corresponden al borde de la unión de paños, incluidos remates y jambas. No representan 106 esquinas de habitaciones. Los ocho anillos no equivalen a ocho recintos: hay componentes separados por vanos y un hueco del volumen técnico. El inventario no sustituye la definición de recintos o superficies de T12/T13.

Los anchos de hueco y hoja son **inferidos**; no existe una cota nominal de puerta legible que los certifique. El paso libre terminado permanece nulo hasta definir marcos y holguras. P06 presenta una diferencia gráfica de 1 px entre hoja y hueco, conservada en el registro para resolver en T22 antes de generar una hoja física. Las bisagras se sitúan en los símbolos de marco, con sensibilidad local de 2 px, no obligatoriamente en el eje del tabique.

La cara exterior superior toca el recorte; se usa provisionalmente el trazo visible `v=1`. No se oculta su incertidumbre usando el nominal de 15 cm para mover todo el perímetro. La sensibilidad de escala de T10 sigue vigente: los pequeños residuos locales no acreditan exactitud global. No se ha forzado ninguna dimensión para producir 76,66 m².

La logia presenta celosía probable en la isométrica; su apertura y carpintería concreta no están demostradas. El nicho D3 tiene una hoja pequeña en el dibujo, pero el armario final tendrá **dos hojas** por solicitud del usuario. El panel añadido en D1 se excluye de los muros; su diseño de mobiliario continúa en T34/T37. La segunda cama de D2 permanece solamente en la imagen original de referencia y se excluye del programa final.

T12 debe confirmar la lectura funcional del baño y la separación de logia a partir de estos bordes y la isométrica. T13 resuelve áreas y T14 alturas, antepechos, dinteles y espesores no acreditados. T16 convertirá el levantamiento revisado en el contrato de datos para Blender, GLB, colliders y Unreal. **No extruir directamente este registro como arquitectura validada**: hay medidas y detalles explícitamente provisionales.

Actualización T12: la [distribución de baño y logia](../topology/README.md) quedó confirmada reutilizando este registro sin cambiar sus coordenadas. Se conserva un baño longitudinal hasta la ducha y una logia con entrada desde cocina. Equipos, áreas de uso e incertidumbres funcionales se documentan allí; superficies y alturas siguen en T13/T14.
