# Guía de estudio por bloques

Las líneas relevantes de los archivos `.py` y `.cpp` están comentadas. Un resultado `-1` significa ausencia; cualquier otro resultado es un índice de base cero. Con duplicados aceptamos cualquier coincidencia: no se exige que binaria devuelva la primera.

## 1. Búsqueda lineal

**Recorrido:** `enumerate(a)` en Python y el `for` de C++ visitan las posiciones desde 0 hasta n−1. No se necesita orden.

**Decisión y salida:** se compara el valor con x. Si coincide, se devuelve el índice y se interrumpe toda la función. Si termina el ciclo, se devuelve −1. Ejemplo: `[8, 3, 6]`, buscar 6 examina 8, 3 y 6; devuelve 2.

**Costo:** primer elemento Θ(1); promedio Θ(n) para posiciones equiprobables; peor Θ(n), incluida la ausencia. Con claves únicas y nuestra mezcla, el número esperado de igualdades es `0.7(n+1)/2 + 0.3n = 0.65n + 0.35`. En datos repetidos encontrar la primera ocurrencia puede reducirlo.

## 2. Búsqueda binaria

**Inicialización:** intervalo inclusivo `[lo, hi] = [0, n−1]`. En un vacío hi=−1 y no se entra al ciclo.

**Reducción:** calcular el centro; si no coincide, comparar para elegir la mitad que todavía puede contener x. El orden garantiza que la mitad descartada no contiene la clave. Ejemplo `[2,4,8,12,18]`, buscar 12: centro 8, luego 12; devuelve 3.

**Terminación:** cada paso descarta al menos el centro y aproximadamente la mitad restante. Cuando lo>hi, no existe la clave. Mejor Θ(1), promedio Θ(log n) con claves distintas y posiciones equiprobables, peor Θ(log n). Se emplea una función auxiliar para reutilizar la lógica desde exponencial.

## 3. Búsqueda exponencial

**Protección:** resolver arreglo vacío y posición cero antes de acotar.

**Acotación:** inspeccionar índices 1, 2, 4, 8... hasta alcanzar un valor ≥x o el final. Entonces la posible coincidencia queda en `[i/2, min(i,n−1)]`.

**Refinamiento:** llamar a binaria dentro de esa cota. Mejor Θ(1); costo O(log(p+1)) respecto a la posición p alcanzada, y peor Θ(log n) para arreglos finitos. Promedio Θ(log n) bajo posiciones equiprobables. Puede ser útil para claves cercanas al inicio aunque n sea grande.

**Límite desconocido:** nuestra implementación recibe un vector/lista y conoce n; demuestra la fase de acotación, no un benchmark de fuente infinita. Para una fuente realmente desconocida se necesita `leer(i)` que devuelva un valor o una señal de fin segura, y acceso por índice. Un flujo exclusivamente secuencial no permite saltos gratuitos: habría que almacenar o consumir los elementos anteriores. No debe confundirse un arreglo de tamaño desconocido con cualquier flujo.

## 4. Búsqueda por interpolación

**Validación:** comprobar lo≤hi y que x esté entre los valores extremos. El cortocircuito evita acceder al vacío.

**Estimación:** `pos = lo + (x−a[lo]) (hi−lo) // (a[hi]−a[lo])`. Si el valor buscado está a la mitad del rango numérico, se estima que su índice también está a mitad. La división entera elimina decimales; se usa la misma fórmula exacta en ambos lenguajes. C++ amplía las operaciones a `long long` antes de restar; los enteros y tamaños del experimento caben con holgura. La implementación C++ supone n representable por int, como nuestros tamaños.

**Avance:** devolver pos si coincide; de lo contrario usar pos+1 o pos−1. Cuando los extremos valen lo mismo, se devuelve lo porque el control previo garantiza x igual a ese valor. Así se evita división entre cero.

**Distribución:** con claves aleatorias aproximadamente uniformes, el número esperado de accesos puede ser O(log log n), bajo ese modelo probabilístico; no es garantía para cualquier entrada. Mejor Θ(1), peor Θ(n). Con `[0,1,...,n−1]`, la fórmula obtiene exactamente x en un intento: es un caso especial más favorable que la uniformidad aleatoria. Un ejemplo adverso es `[0,1,...,n−2,n²]` buscando n−2: las primeras estimaciones avanzan casi de uno en uno, mostrando por qué puede degradarse a lineal.

## 5. Notaciones y casos no son sinónimos

O(g(n)) significa una cota superior eventual hasta un factor constante: existe c>0 y n₀ tal que T(n)≤cg(n) para n≥n₀. Ω es cota inferior y Θ exige ambas. No son respectivamente «peor, mejor y promedio»: cualquiera puede describir una función de mejor, promedio o peor caso. Debe indicarse qué función y qué supuestos se analizan. El promedio requiere una distribución de entradas.

Todas estas versiones iterativas usan O(1) espacio auxiliar, sin contar arreglo, consultas, pruebas y resultados.

## 6. Cómo leer el benchmark

1. Generar datos una vez con semilla 123 y exportarlos a texto.
2. Leer exactamente esos archivos en Python y C++.
3. Validar cada consulta contra pertenencia real antes de medir. Las pruebas adicionales incluyen vacío, único, repetidos, negativos, extremos enteros, huecos y aleatorios.
4. Calentar con 20 consultas por algoritmo. Las validaciones ya recorrieron los datos: no es un ensayo de caché fría.
5. Ejecutar tres lotes de 1000 consultas. Rotar el orden de algoritmos entre lotes; los lenguajes se ejecutan secuencialmente, C++ primero.
6. Dividir duración del lote entre 1000. La media de tres lotes es el tiempo promedio informado; `sd_ms` es desviación muestral entre lotes, no intervalo de confianza.
7. No cronometrar lectura, generación, ordenamiento, oráculo ni contador. Sí se incluyen ciclo, llamada y suma de índices; es el costo real de este protocolo.
8. El checksum se imprime/guarda para consumir resultados; no es suficiente por sí solo para demostrar correctitud. La validación individual sí comprueba cada consulta.

## 7. Comparaciones contadas

`comparaciones.csv` proviene de una segunda ejecución instrumentada C++. Cuenta cada igualdad o desigualdad entre claves/valores, incluidos los límites de interpolación y la igualdad entre extremos. No cuenta comparaciones de índices, aritmética ni llamadas. Las funciones plantilla `contar=false` eliminan el contador de las versiones cronometradas. Los gráficos identifican explícitamente este conteo como C++; no son tiempos ni conteos medidos en Python. Los algoritmos manuales siguen la misma estrategia, pero comparar tiempos entre lenguajes también compara representaciones de memoria y entornos de ejecución.

## 8. Heurística propuesta

```text
SI límite efectivo desconocido:
    SI orden certificado y acceso indexado seguro: elegir exponencial + binaria
    EN OTRO CASO: recorrido lineal hasta fin de fuente
SI n < 64: elegir lineal
SI orden no certificado: comprobar todo el orden una vez (O(n))
SI desordenado:
    comparar q*n con n*log2(n) + q*log2(n)
    SI ordenar se amortiza: ordenar copia y usar binaria
    EN OTRO CASO: lineal
SI extremos iguales: binaria
tomar 33 posiciones equiespaciadas
E = máximo |(a[i]-a[0])/(a[n-1]-a[0]) - i/(n-1)|
SI E <= 0.05: interpolación
EN OTRO CASO: binaria
```

Un muestreo NO certifica que el arreglo completo esté ordenado. La verificación completa se paga una vez y se conserva como metadato si los datos no cambian. Para una única consulta sin certificado puede convenir directamente lineal, evitando inspeccionar el arreglo dos veces. Los umbrales 64 y 0.05 son decisiones didácticas sin calibración empírica; no prometen optimalidad. El modelo de amortización supone constantes iguales y omite asignación/copias: es una orientación que debe ajustarse midiendo el ordenamiento y la carga real. Si importa el índice original, hay que ordenar pares (valor, índice original). Una muestra uniforme tampoco garantiza que interpolación sea rápida: binaria sigue siendo la opción conservadora.

La función `seleccionar` devuelve una recomendación; no ordena ni ejecuta automáticamente la consulta. Para límite desconocido su respuesta describe la interfaz necesaria, no conecta una fuente externa. Se prueba por separado y no integra la comparación de los cuatro algoritmos.

## 9. Preguntas para comprobar comprensión

- ¿Por qué ordenar es una precondición de binaria y no de lineal?
- ¿Qué ocurre con `hi` cuando el arreglo está vacío?
- ¿Por qué se actualiza `lo = pos + 1` y no `lo = pos`?
- ¿Por qué interpolación funciona de manera excepcional con enteros consecutivos?
- ¿Qué cambia si los misses están dentro del rango numérico?
- ¿Por qué tres mediciones no demuestran una complejidad matemática?
