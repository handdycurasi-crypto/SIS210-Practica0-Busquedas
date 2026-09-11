# Propuesta de preparación y sustentación para tres integrantes

Esta distribución es una propuesta de estudio. No atribuye tareas ya realizadas ni declara quién programó o ejecutó los experimentos. Todos deben poder explicar el contrato de búsqueda y los límites del benchmark.

| Integrante | Núcleos | Responsabilidad conceptual propuesta |
|---|---|---|
| YANA MENDOZA CARLOS BENEDICTO | 1–4 | Especificación, RAM, notación asintótica y casos de análisis. |
| BELIZARIO YANA DAVID VICTOR | 5–8 | Correctitud, búsqueda lineal, binaria y exponencial. |
| CURASI ZEVALLOS HANDDY RONALD | 9–12 | Interpolación, distribución, mediciones y selección de algoritmos. |

## Bloque 1: explicar qué se compara y bajo qué supuestos

Preparar una explicación del contrato usando `[4,4,9]`: devolver 0 o 1 al buscar 4 es correcto, pero devolver cualquier posición al buscar 7 es incorrecto. Después distinguir entrada, memoria auxiliar y costo de una operación. El objetivo es que el público entienda por qué el orden de un arreglo es una precondición y por qué no se puede tratar el equipo real como si todas sus operaciones duraran igual.

Derivar en la pizarra `3n ≤ 3n+7 ≤ 10n` para n≥1 y explicar la diferencia entre una cota y una medición. Derivar también `0.7(n+1)/2 + 0.3n` para lineal con claves únicas y hits uniformes por posición. Aclarar que esa esperanza teórica no reemplaza las cifras del CSV ni describe exactamente el sesgado con duplicados.

Preguntas de preparación: ¿qué distribución exige un promedio?, ¿por qué Ω no significa mejor caso?, ¿por qué una semilla fija no fija los tiempos? Fuentes centrales: Cormen, Morin, Sedgewick y Wayne; Erickson para la lógica de justificación.

## Bloque 2: defender la corrección y el crecimiento de cada procedimiento

Mostrar una traza breve de lineal y binaria en `[2,4,8,12,18]`. En binaria, identificar el invariante: si x está presente y no se ha encontrado, debe seguir dentro del intervalo. Explicar la actualización de extremos y por qué la longitud disminuye. Relacionar la reducción sucesiva con `n/2^k` y con el costo logarítmico, distinguiendo número de iteraciones de comparaciones de claves.

Para exponencial, usar una posición objetivo 13 y las sondas 1, 2, 4, 8, 16. Justificar por separado la acotación y la búsqueda dentro del intervalo; explicar por qué una fuente sin n necesita acceso indexado seguro. Precisar que el programa entregado sí conoce la longitud y que esa prueba no simula una fuente infinita.

Preguntas de preparación: ¿qué ocurre con vacío y duplicados?, ¿qué actualización podría causar un ciclo que no termina?, ¿por qué exponencial no debe superar siempre a binaria? Fuentes centrales: Sedgewick y Wayne, Erickson y Morin. La prueba por invariantes y las trazas son razonamientos; los tests existentes son evidencia adicional de implementación.

## Bloque 3: interpretar los resultados sin exagerar sus conclusiones

Partir de la fórmula de interpolación. Sustituir `a[i]=i` para demostrar por qué el uniforme consecutivo es un caso especialmente favorable. Luego explicar cómo el 80% concentrado desajusta la relación valor/posición. Usar el ejemplo analítico `[0,1,...,n−2,n²]` para mostrar que existe un riesgo de avance casi unitario; aclarar que no fue un nuevo experimento del proyecto.

Interpretar las figuras originales indicando unidades, ejes logarítmicos y desviación entre tres lotes. Distinguir tiempo medido de comparaciones contadas; no atribuir diferencias de tiempo a fallos de caché que no se midieron. Terminar con la heurística: certificado de orden, tamaño, uniformidad aproximada, límite conocido y amortización del ordenamiento. Los umbrales 64 y 0.05 son propuestos, no óptimos demostrados.

Preguntas de preparación: ¿por qué importan los misses exteriores?, ¿por qué 80% en el dataset no obliga a 80% en los hits?, ¿cuándo el costo de ordenar invalida la aparente ventaja de binaria? Fuentes centrales: Perl et al., Van Sandt et al., Sedgewick y Wayne; documentación oficial de Python y Google Benchmark para medición.

## Cierre compartido

Cada integrante debe conectar una garantía teórica, una cifra o figura original y una limitación del diseño. La transición sugerida es: **contrato y modelo → corrección y reducción del trabajo → distribución y costo real**. No atribuir resultados de artículos a la ejecución del grupo ni afirmar que tres tamaños prueban una complejidad matemática.
