# E05 · Recorrido básico

T28–T33 completadas en arquitectura vacía. El controlador de la web y las pruebas comparten WalkEngine: cápsula de radio 0,22 m, física fija a 60 Hz, gravedad, movimiento diagonal normalizado y ojo a 1,60 m. Los cambios de vista conservan la posición; caminar restaura techo y vecinos. Pausa, pérdida de foco, liberación del puntero y regreso voluntario al acceso están implementados.

Diez recorridos de ida y vuelta pasaron por el controlador real: D1, D2, D3, cocina, estar, comedor, baño, ducha, logia y pasillo común. Se ejecutaron 5601 pasos de seguimiento. Altura ocular observada: 1,598186–1,604383 m, dentro de ±5 mm. Caminos y medidas están en validation/e05/walk-check.json. La configuración abre la puerta del destino y cierra las innecesarias: la puerta del baño abierta hacia el pasillo estrecha el paso a dormitorios, como en el plano.

Se corrigió en la fuente de exportación el signo de los giros: Blender +Z se convierte a glTF +Y conservando el signo. El control adicional compara la orientación de cada pivote GLB con el registro de colisiones y detectaría una nueva inversión. Se regeneraron Blender, GLB, colliders y evidencias afectadas.

Las seis hojas abren y cierran sin chocar con la arquitectura en la prueba despejada. Una cápsula colocada en el barrido detuvo la puerta antes de la intersección; no fue empujada. Se prueban poses a incrementos angulares inferiores a 2 grados. La holgura numérica de consulta de hoja es de 2 mm. Las jambas de su propio vano se excluyen de la consulta por el contacto mecánico de bisagra; otros muros y objetos bloquean.

Casos adicionales: movimiento recto y diagonal de 0,399906/0,399933 m; muro bloquea incluso con cuadros de 100 ms; frente de ventana bloquea; pausa no deriva y reinicio queda en posición válida. Evidencia: adverse-check.json. No se usan reinicios automáticos para ocultar un fallo de recorrido; las pruebas solo restablecen el caso entre rutas independientes.

En el navegador se comprobó ingreso en primera persona, techo presente, pausa por Escape y regreso a vista general. El recorrido completo se verificó automáticamente con el mismo controlador, no se presenta como paseo manual completo. TypeScript y compilación de producción correctos. Las pruebas se repetirán con muebles y decoración en E06/E07; dispositivos, controles táctiles, rendimiento y WebMCP corresponden a E09.
