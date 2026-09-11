# Práctica 01 — Búsquedas y Notación Asintótica

Universidad Nacional del Altiplano – Puno · Escuela Profesional de Ingeniería de Sistemas  
**Curso:** Algoritmos y Estructuras de Datos – SIS210  
**Docente:** ZANABRIA GALVEZ ALDO HERNAN

**Integrantes:**

- YANA MENDOZA CARLOS BENEDICTO
- BELIZARIO YANA DAVID VICTOR
- CURASI ZEVALLOS HANDDY RONALD

El nombre de carpeta `SIS210-Practica0-Busquedas` usa «Práctica 0» solo como referencia interna indicada por el docente. El título oficial se conserva en el informe. Proyecto preparado para publicar posteriormente; no se creó ni publicó un repositorio remoto.

## Objetivo y contenido

Implementar manualmente lineal, binaria, exponencial e interpolación en Python y C++; verificar correctitud y comparar tiempos reales con el análisis asintótico. No se usa `bisect` ni una búsqueda de biblioteca como implementación principal. Las líneas relevantes están comentadas y [la guía por bloques](docs/EXPLICACION.md) explica el funcionamiento y propone preguntas de estudio.

- `cpp/busquedas.cpp`: cuatro algoritmos, pruebas, benchmark y conteo separado de comparaciones.
- `python/busquedas.py`: cuatro algoritmos manuales y ejemplo interactuable editando datos y clave.
- `python/heuristica.py`: selector orientativo con pruebas.
- `scripts/`: generación, detección de entorno, benchmark Python, gráficos, validación y reproducción.
- `datos/`: nueve archivos de enteros compartidos por ambos lenguajes, semilla y huellas SHA-256.
- `resultados/`: CSV resumidos y por repetición, comparaciones, entorno, tablas completas y registros de consola.
- `graficos/`: figuras PNG y PDF vectorial; manifiesto que identifica sus CSV de origen.
- `informe/`: `informe.tex`, tablas/métricas/entorno derivados y `informe.pdf` (versión ampliada con 12 núcleos teóricos).
- `referencias/FUENTES.md`: bibliografía APA 7, enlaces verificables y alcance de consulta.
- `docs/CONTROL_CALIDAD.md`: alcance y límites de la verificación final.

## Requisitos

Python 3.10 o superior; g++ compatible con C++17; Matplotlib 3.8 o superior y menor que 4 para gráficos; pdfLaTeX (TeX Live o equivalente) con babel, lmodern, microtype, amsmath, amssymb, booktabs, tabularx, graphicx, xcolor, enumitem, fancyhdr, titlesec hyperref y xurl. El benchmark Python solo usa biblioteca estándar; Matplotlib se necesita al graficar.

Ejecución original: Python 3.12.14 y g++ 13.3.0 en Ubuntu 24.04.3 LTS remoto. Información detectada completa en `resultados/entorno.json`; no corresponde al equipo personal de los integrantes. `resultados/dependencias.txt` registra las versiones de las herramientas de figuras y PDF.

Desde la carpeta raíz del proyecto en Linux Mint/Ubuntu (g++ y TeX Live deben estar instalados):

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Actualización teórica del 10 de septiembre de 2026

Se amplió el marco teórico a 12 núcleos y se actualizaron citas y referencias APA 7. Esta actualización no ejecutó benchmarks ni modificó código, datos, resultados, gráficos o métricas. Las evidencias originales se conservan byte por byte; véase `docs/INTEGRIDAD_AMPLIACION.json`. La nueva extensión sustituye el límite anterior de tres páginas de contenido. La propuesta de preparación para los tres integrantes está en `docs/SUSTENTACION_TRES_INTEGRANTES.md`.

Para recompilar solo el informe, sin alterar experimentos:

```bash
cd informe
pdflatex -interaction=nonstopmode -halt-on-error informe.tex
pdflatex -interaction=nonstopmode -halt-on-error informe.tex
```

No ejecute los comandos de reproducción siguientes si solo quiere conservar y estudiar la entrega existente.

## Reproducir todo

```bash
python3 scripts/reproducir.py
```

Este comando regenera datos, detecta el entorno, compila C++, ejecuta las pruebas previas y ambos benchmarks **secuencialmente**, genera gráficos/tablas, audita CSV y compila el PDF dos veces. Muestra resultados y los conserva en registros. Puede tardar varios minutos, principalmente por búsqueda lineal en Python. Reemplaza las mediciones incluidas por las nuevas: guarde una copia si desea comparar ejecuciones. Datos y consultas son reproducibles con el generador documentado; los tiempos no serán idénticos por equipo y ruido del sistema.

El informe usa cifras y entorno generados, pero su discusión corresponde al experimento original: revise interpretaciones y maquetación si ejecuta en otro equipo o modifica el diseño. No agregue datos nuevos al informe sin volver a producir figuras y tablas.

## Ejecutar por etapas

Ejemplo breve para estudiar los algoritmos:

```bash
python3 python/busquedas.py
python3 python/heuristica.py
```

Datos compartidos y entorno:

```bash
python3 scripts/generar_datos.py
python3 scripts/entorno.py
```

C++ (pruebas, tiempos en consola y CSV):

```bash
mkdir -p build
g++ -std=c++17 -O2 -Wall -Wextra -pedantic cpp/busquedas.cpp -o build/busquedas
./build/busquedas .
```

`-std=c++17` habilita el estándar; `-O2` optimiza; los demás flags activan diagnósticos. No se usa `-march=native` ni `-ffast-math`. El contador se elimina en compilación de la versión cronometrada mediante `if constexpr`; se activa solo para la pasada de comparaciones.

Python (pruebas y benchmark, `time.perf_counter()`):

```bash
python3 -u scripts/benchmark_python.py
```

Gráficos, auditoría y PDF:

```bash
python3 scripts/graficar.py
python3 scripts/validar_resultados.py
cd informe
pdflatex -interaction=nonstopmode -halt-on-error informe.tex
pdflatex -interaction=nonstopmode -halt-on-error informe.tex
```

Compile desde `informe/` para resolver las rutas relativas de figuras. La configuración de babel usa `provide=*`, compatible con la configuración de español disponible en el entorno original.

## Diseño experimental

Tamaños exactos: 10 000, 100 000 y 500 000. Uniforme: enteros consecutivos `0..n-1`, sin duplicados. Sesgado: exactamente 80% en `[0,n/10-1]` y 20% en `[n/10,5n]`, sorteados con reemplazo y ordenados; los rangos no se solapan. Desordenado: permutación del uniforme. Semilla `123`, generador `random.Random` de Python; exportar una vez evita las diferencias entre generadores de C++ y Python.

Formato de cada `.txt`: primera línea `n 1000`; segunda línea arreglo; tercera línea consultas. Hay 700 hits seleccionados por posición con reemplazo y 300 misses distintos `10*n+i`, luego mezclados. Los nueve archivos contienen 9000 consultas en total, con posibles claves repetidas; cada combinación repite su mismo lote tres veces.

Solo lineal trabaja sobre desordenados. En los ordenados se ejecutan los cuatro. Total: 27 combinaciones por lenguaje, 54 medias, 162 lotes medidos y 162 000 búsquedas cronometradas. Las validaciones y el calentamiento son ejecuciones adicionales excluidas de ese total. Veinte consultas de calentamiento por combinación; se rota el orden entre lotes.

CSV de medias: lenguaje, algoritmo, dataset, n, `ms_por_busqueda`, `sd_ms` (desviación muestral entre tres lotes), repeticiones, hits, misses y consultas. CSV crudos: tiempo por lote y checksum. [Tabla completa](resultados/TABLAS.md).

`comparaciones.csv` cuenta en C++ las comparaciones de claves efectivamente evaluadas, incluidos extremos de interpolación, fuera del cronómetro. No cuenta índices ni aritmética. No se presenta como conteo medido en Python. Con duplicados cada algoritmo puede devolver un índice distinto y seguir siendo correcto.

## Principales conclusiones y límites

- Binaria reduce drásticamente el trabajo frente a lineal para los tamaños ordenados evaluados.
- Interpolación gana en el uniforme consecutivo; pierde claramente frente a binaria en el sesgado. El caso consecutivo permite estimación exacta y no debe extrapolarse a cualquier distribución uniforme aleatoria.
- Exponencial sirve para acotar cuando el fin no se conoce y hay acceso indexado seguro; el experimento usa arreglos finitos y no mide una fuente ilimitada.
- Lineal no necesita ordenar. Para pocas consultas puede convenir evitar el costo de preparación; el costo de ordenar no está incluido en estos tiempos.
- Los misses externos permiten a interpolación descartarlos de inmediato. Misses interiores podrían cambiar la comparación.
- No hay aislamiento exclusivo, afinidad fijada ni medición de caché fría. Tres lotes C++ muy cortos exhiben ruido; las barras son dispersión, no intervalos de confianza. Se priorizan tendencias amplias y conteos sobre diferencias temporales pequeñas.
- C++ y Python comparten datos y lógica, pero no representación física ni costos de ejecución. Los ratios describen estas implementaciones, no una ley universal entre lenguajes.
- La evidencia es compatible con la teoría; no constituye una demostración matemática de complejidad.

## Publicar posteriormente en GitHub

Descomprima el ZIP y abra una terminal en esta carpeta. Cree usted un repositorio vacío en GitHub y siga sus instrucciones para conectar esta carpeta. El ZIP no contiene un remoto configurado ni una carpeta `.git`, binarios, entornos virtuales o cachés. Sí contiene datos, resultados y gráficos para reproducibilidad. El material oficial del docente no se redistribuye en el repositorio; la referencia está documentada. La licencia de publicación queda a elección de los autores.
