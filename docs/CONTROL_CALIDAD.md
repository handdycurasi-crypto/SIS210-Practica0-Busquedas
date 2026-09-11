# Control de calidad de la ejecución original

**Actualización del 10 de septiembre de 2026:** este registro documenta la entrega experimental original. Sus referencias a cuatro páginas corresponden a esa versión. El informe ampliado y su nueva compilación se verifican en `CAMBIOS_MARCO_TEORICO.md`; los resultados experimentales originales permanecen intactos.

Estado: completado el 9 de septiembre de 2026 (UTC).

| Requisito | Verificación y evidencia |
|---|---|
| Cuatro algoritmos manuales en ambos lenguajes | Fuentes comentadas; Python no importa bisect. |
| Compilar y ejecutar C++ | g++ 13.3.0, C++17, O2, Wall, Wextra y pedantic; ejecución terminó correctamente. |
| Ejecutar Python | Python 3.12.14; ejecución completa y secuencial; resultados en `ejecucion_python.log`. |
| Correctitud antes de medir | Casos límite y aleatorios; todas las consultas experimentales validadas contra pertenencia independiente. |
| Precondición de orden | Solo lineal en desordenados; se verifica orden completo en los otros conjuntos. |
| Entradas comparables | Los dos lenguajes leen los mismos nueve archivos y las mismas consultas. |
| Proporción hit/miss | Auditoría confirma 700/300 para cada archivo. |
| Datos reales | 54 medias derivadas de 162 tiempos por lote guardados en CSV; no son simulaciones de tiempos. |
| Estadísticos | Media y desviación recalculadas desde las tres repeticiones; control automático satisfactorio. |
| Comparaciones | 27 conteos C++ separados del tiempo; los conteos lineales se contrastan con un oráculo independiente. |
| Consistencia de respuestas | Checksums coinciden entre repeticiones y lenguajes; complemento de las pruebas individuales, no sustituto. |
| Gráficos | Matplotlib lee CSV completos; SHA-256 enlaza cada figura con sus fuentes. |
| Heurística | Cuatro casos de decisión comprobados; umbrales propuestos y limitaciones documentadas. |
| Referencias | Editorial, recursos oficiales de autores y artículo académico primario; alcance de acceso en `referencias/FUENTES.md`. |
| LaTeX | Compilación efectiva; log guardado; PDF de cuatro páginas y sin cajas desbordadas. |
| Inspección visual | Portada, tres páginas de contenido, tablas, ecuaciones, figuras, márgenes y referencias revisados en imágenes renderizadas. |
| Repositorio | README, fuentes, datos, resultados, gráficos y documentación; sin publicación remota. |

La auditoría reproducible está en `scripts/validar_resultados.py` y su resultado en `resultados/control_calidad.json`. El informe final contiene portada + tres páginas, con las siete respuestas obligatorias. La guía extensa de estudio se entrega en Markdown para no sobrecargar el PDF.

Los benchmarks informan wall time del entorno remoto compartido. No se midieron contadores de hardware, energía, tiempos de ordenamiento ni una fuente de longitud realmente desconocida. No se presentan esas cuestiones como resultados experimentales. Los misses externos y el uniforme consecutivo son decisiones heredadas del diseño base que condicionan el análisis.

El script `reproducir.py` reúne las etapas que se ejecutaron durante la preparación; la validación final se hizo por etapas, sin afirmar una segunda ejecución integral de ese orquestador. Cambiar el equipo o el software puede cambiar tiempos y requerir revisar las conclusiones, aunque datos y consultas se mantengan.
