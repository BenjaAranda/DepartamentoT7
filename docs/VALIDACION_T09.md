# T09: inventario de cotas y espesores

Fecha: 9 de septiembre de 2026, America/Santiago. Resultado: T09 completada como inventario de lo legible, con lecturas y unidades pendientes de confirmación explícitas.

El [inventario](../architecture/measurements/README.md) contiene 58 registros y sus posiciones: 14 cotas locales, ocho menciones de espesor, 28 códigos, cuatro menciones de superficie y cuatro referencias complementarias. La lectura tiene confianza alta en 53 registros, media en cuatro y baja en uno. La confianza de lectura se conserva separada del estado de la unidad y de la aplicabilidad al T7.

## Verificación documental y visual

Se extrajo texto de las 42 páginas y se revisó un índice visual completo. Se ampliaron los sectores de p20 con cotas y rótulos, plantas nativas de los edificios A y B en p15/p17, sus sectores T7 y núcleos comunes, y detalles técnicos de p22-p24. La [revisión por páginas](../architecture/measurements/t09-revision-pdf.json) distingue la revisión general de la ampliación detallada.

Se localizaron ocho rótulos M.H.A. 15cm. Los números de los 28 códigos de tabiques no se convirtieron en espesor. Se conservaron con confianza media dos cotas sobre achurados y un tipo parcialmente legible del nicho de cocina. No se encontró una cadena general de dimensiones del T7 ni un cuadro de espesores aplicable a sus códigos en esta presentación.

Las medidas 150 MM y 110 MM de p23 corresponden a componentes de un detalle genérico. El diagrama acotado de p24 también se registró como referencia no atribuida al T7; una lectura horizontal es probable y otras cotas quedan sin certificar. No se usaron para declarar altura o espesor de la vivienda.

Se inspeccionaron las tres láminas finales de recortes. Se corrigió la tipografía inicial para mostrar correctamente acentos, ñ y símbolo de diámetro. La revisión final comprobó transcripciones, recortes, separación de las tarjetas y avisos de unidad inferida o referencia genérica. Los recortes de cifras giradas y de la figura reflejada de p24 incluyen su transformación de lectura en el catálogo.

## Comprobación de datos

El generador `scripts/build-t09-inventory.py` terminó correctamente y produjo [comprobacion.json](../references/derived/t09-medidas/comprobacion.json):

- PDF original y referencias T07 con huellas intactas.
- 58 IDs únicos y todos los localizadores dentro del marco de su fuente.
- Vínculos de T08 válidos y cobertura de las 42 páginas sin omisiones ni duplicados en el registro de revisión.
- Códigos sin conversión numérica de espesor; cotas locales con unidad propuesta cm, marcada como inferida.
- Los 58 registros impiden su uso directo como geometría. La transformación métrica sigue sin definir.
- Huellas del catálogo y las tres láminas guardadas, junto a la tipografía usada.

Las comprobaciones automáticas validan estructura, integridad y políticas de datos; no sustituyen la interpretación de los símbolos ni certifican por sí mismas la lectura manual.

## Alcance y continuación

T09 no calibra el plano ni valida 76,66 m², escala real, altura ocular, espesores desconocidos o recorrido. Conserva la diferencia 76,66/76,80 m² para T13. La búsqueda registra limitaciones de la fuente; no las rellena con medidas supuestas de camas, sillas o baldosas.

No cambió el código de `web/`, las referencias originales ni el catálogo T08. No se generan todavía Blender, GLB, colliders o Unreal, y no se publica el sitio. Las pruebas pertinentes fueron la validación del inventario y la revisión de las evidencias; no correspondía repetir la compilación web.

La siguiente tarea es T10: fijar origen, ejes y escala con referencias horizontales y verticales, separando puntos de ajuste de controles independientes y documentando los residuos y la incertidumbre.
