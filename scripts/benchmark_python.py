"""Pruebas previas, calentamiento y tres repeticiones; E/S fuera del cronómetro."""
import sys  # Permite importar el módulo del proyecto.
from pathlib import Path  # Construye rutas independientes del directorio actual.
import time  # Cronómetro monotónico de alta resolución.
import csv  # Resultados tabulares.
import statistics  # Media y desviación muestral.
import random  # Casos aleatorios de prueba.
RAIZ = Path(__file__).resolve().parents[1]  # Raíz del repositorio.
sys.path.insert(0, str(RAIZ / 'python'))  # Habilita la importación local.
from busquedas import ALGORITMOS  # Implementaciones manuales.

def verificar(a, consultas, funciones):  # Valida índices, no igualdad entre índices con duplicados.
    presentes = set(a)  # Oráculo independiente y rápido.
    for nombre, fn in funciones:  # Prueba cada algoritmo permitido.
        for x in consultas:  # Comprueba cada consulta.
            i = fn(a, x)  # Obtiene la respuesta real.
            assert (i == -1 and x not in presentes) or (0 <= i < len(a) and a[i] == x), (nombre, x, i)  # Exige corrección.

rng = random.Random(456)  # Semilla separada para las pruebas.
casos = [[], [7], [5, 5, 5], [-9, -2, 0, 4, 12], [-2147483648, 0, 2147483647]]  # Vacío, único, duplicados, extremos.
casos += [sorted(rng.randrange(-30, 31) for _ in range(k)) for k in range(1, 51)]  # Casos adicionales con huecos.
for a in casos:  # Pruebas antes de medir.
    verificar(a, list(range(-35, 36)) + a, list(ALGORITMOS.items()))  # Incluye hits, misses y extremos.
verificar([9, 1, 7, 3], [9, 1, 7, 3, 2], [('lineal', ALGORITMOS['lineal'])])  # Desordenado solo con lineal.
print('Correctitud Python: casos límite y aleatorios OK.', flush=True)  # Evidencia en consola.
campos = ['lenguaje', 'algoritmo', 'dataset', 'n', 'ms_por_busqueda', 'sd_ms', 'repeticiones', 'hits', 'misses', 'consultas']  # Esquema resumen.
with (RAIZ / 'resultados/resultados_python.csv').open('w', newline='') as resumen, (RAIZ / 'resultados/repeticiones_python.csv').open('w', newline='') as crudo:  # Abre salidas.
    w, raw = csv.writer(resumen), csv.writer(crudo)  # Escritores CSV.
    w.writerow(campos)  # Cabecera del resumen.
    raw.writerow(['lenguaje', 'dataset', 'n', 'algoritmo', 'repeticion', 'ms_por_busqueda', 'checksum'])  # Cabecera de tiempos crudos.
    for n in (10000, 100000, 500000):  # Tamaños oficiales.
        for tipo in ('uniforme', 'sesgado', 'desordenado'):  # Distribuciones oficiales.
            numeros = list(map(int, (RAIZ / 'datos' / f'{tipo}_{n}.txt').read_text().split()))  # Lee fuera del cronómetro.
            a, q = numeros[2:2+n], numeros[2+n:]  # Separa arreglo y consultas.
            assert len(q) == 1000  # Evita mediciones incompletas.
            funciones = list(ALGORITMOS.items())[:1] if tipo == 'desordenado' else list(ALGORITMOS.items())  # Respeta precondiciones.
            assert tipo == 'desordenado' or a == sorted(a)  # Comprueba el orden real.
            print(f'Validando {tipo} n={n}', flush=True)  # Progreso previo a medir.
            verificar(a, q, funciones)  # Valida todas las consultas antes del benchmark.
            muestras = {nombre: [] for nombre, _ in funciones}  # Acumula tres tiempos por algoritmo.
            for nombre, fn in funciones:  # Calentamiento de todos los algoritmos.
                for x in q[:20]:  # Veinte consultas no medidas.
                    fn(a, x)  # Prepara código y datos parcialmente.
            for rep in range(3):  # Tres lotes de exactamente mil búsquedas.
                orden = funciones[rep % len(funciones):] + funciones[:rep % len(funciones)]  # Rota el orden para reducir sesgo temporal.
                for nombre, fn in orden:  # Ejecuciones secuenciales.
                    checksum = 0  # Consume los índices obtenidos.
                    inicio = time.perf_counter()  # Inicio del lote medido.
                    for x in q:  # Usa idénticas consultas entre algoritmos.
                        checksum += fn(a, x)  # Ejecuta y acumula un resultado observable.
                    ms = (time.perf_counter() - inicio) * 1000 / len(q)  # Milisegundos por búsqueda.
                    muestras[nombre].append(ms)  # Guarda la medición sin redondearla.
                    raw.writerow(['Python', tipo, n, nombre, rep + 1, ms, checksum])  # Persiste evidencia por repetición.
            for nombre, _ in funciones:  # Resume tras todas las repeticiones.
                fila = ['Python', nombre, tipo, n, statistics.mean(muestras[nombre]), statistics.stdev(muestras[nombre]), 3, 700, 300, 1000]  # Media y dispersión.
                w.writerow(fila)  # Guarda resultados reales.
                print(*fila, sep=',', flush=True)  # Muestra también en consola.
