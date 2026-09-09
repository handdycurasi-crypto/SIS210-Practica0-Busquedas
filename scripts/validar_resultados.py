"""Audita archivos finales, proporciones, estadísticas y trazabilidad de figuras."""
from pathlib import Path  # Rutas portables.
import csv  # Lee los resultados reales.
import json  # Manifiestos y auditoría.
import hashlib  # Verifica identidad de entradas y fuentes de figuras.
import math  # Tolerancias numéricas.
import statistics  # Recalcula estadísticos desde tiempos crudos.
RAIZ = Path(__file__).resolve().parents[1]  # Directorio del proyecto.
manifest = json.loads((RAIZ / 'datos/manifest.json').read_text())  # Metadatos de entradas.
conteos = list(csv.DictReader((RAIZ / 'resultados/comparaciones.csv').open()))  # Conteos instrumentados.
for r in manifest:  # Verifica todos los archivos compartidos.
    ruta = RAIZ / 'datos' / f"{r['dataset']}_{r['n']}.txt"  # Archivo correspondiente.
    assert hashlib.sha256(ruta.read_bytes()).hexdigest() == r['sha256']  # No sufrió cambios.
    valores = list(map(int, ruta.read_text().split()))  # Interpreta enteros.
    n, m = valores[:2]  # Cabecera.
    a, q = valores[2:2+n], valores[2+n:]  # Datos y consultas.
    assert n in (10000,100000,500000) and m == len(q) == 1000  # Tamaños exactos.
    assert len(a) == n  # Longitud real del arreglo.
    presentes = set(a)  # Oráculo reutilizado.
    assert sum(x in presentes for x in q) == 700  # Hit/miss efectivo.
    assert len([x for x in q if x not in presentes]) == 300  # Fallos efectivos.
    if r['dataset'] != 'desordenado':  # Solo entradas con precondición de orden.
        assert all(a[i-1] <= a[i] for i in range(1,n))  # Verifica todo el orden.
    if r['dataset'] == 'uniforme':  # Caso consecutivo sin duplicados.
        assert a == list(range(n))  # Correspondencia exacta con el diseño.
    if r['dataset'] == 'sesgado':  # Distribución diseñada sin solapar rangos.
        assert sum(0 <= v < n//10 for v in a) == 4*n//5  # Concentración exacta del 80%.
    primeras = {}  # Oráculo eficiente de comparaciones lineales.
    for i,v in enumerate(a):  # Primera posición de cada valor.
        primeras.setdefault(v,i)  # No reemplaza duplicados posteriores.
    esperado = statistics.mean(primeras[x]+1 if x in primeras else n for x in q)  # Comparaciones realmente necesarias.
    medido = next(float(c['comparaciones_promedio']) for c in conteos if c['dataset']==r['dataset'] and int(c['n'])==n and c['algoritmo']=='lineal')  # Conteo C++.
    assert math.isclose(esperado, medido, rel_tol=1e-10)  # Verificación independiente.
checksums = {}  # Control adicional entre lenguajes.
for sufijo in ['cpp','python']:  # Dos implementaciones y sus CSV.
    resumen = list(csv.DictReader((RAIZ / 'resultados' / f'resultados_{sufijo}.csv').open()))  # Medias exportadas.
    crudos = list(csv.DictReader((RAIZ / 'resultados' / f'repeticiones_{sufijo}.csv').open()))  # Mediciones individuales.
    assert len(resumen) == 27 and len(crudos) == 81  # Matriz completa.
    claves = set()  # Detecta filas repetidas.
    for r in resumen:  # Audita cada combinación.
        clave = (r['dataset'],r['n'],r['algoritmo'])  # Identidad experimental.
        assert clave not in claves  # No debe duplicarse.
        claves.add(clave)  # Registra combinación revisada.
        assert r['dataset'] != 'desordenado' or r['algoritmo'] == 'lineal'  # Respeta orden.
        assert (int(r['hits']),int(r['misses']),int(r['consultas']),int(r['repeticiones'])) == (700,300,1000,3)  # Protocolo exacto.
        lote = [s for s in crudos if (s['dataset'],s['n'],s['algoritmo'])==clave]  # Recupera tres repeticiones.
        assert sorted(int(s['repeticion']) for s in lote) == [1,2,3]  # No faltan lotes.
        tiempos = [float(s['ms_por_busqueda']) for s in lote]  # Mediciones sin redondeo significativo.
        assert all(math.isfinite(t) and t > 0 for t in tiempos)  # Valores medidos válidos.
        assert math.isclose(statistics.mean(tiempos),float(r['ms_por_busqueda']),rel_tol=1e-9)  # Media correctamente calculada.
        assert math.isclose(statistics.stdev(tiempos),float(r['sd_ms']),rel_tol=1e-8)  # Dispersión correctamente calculada.
        assert len(set(s['checksum'] for s in lote)) == 1  # Mismas respuestas en tres repeticiones.
        if clave in checksums:  # El segundo lenguaje debe producir las mismas posiciones en estas implementaciones.
            assert checksums[clave] == lote[0]['checksum']  # Control de consistencia adicional.
        checksums[clave] = lote[0]['checksum']  # Guarda el checksum de esta combinación.
for nombre, huella in json.loads((RAIZ / 'graficos/fuentes_sha256.json').read_text()).items():  # Verifica origen de figuras.
    assert hashlib.sha256((RAIZ / 'resultados' / nombre).read_bytes()).hexdigest() == huella  # No usar gráficos obsoletos.
resultado = dict(estado='OK', datasets=9, consultas_en_archivos=9000, combinaciones_temporales=54, lotes_medidos=162, busquedas_cronometradas=162000, conteos_cpp=27, comprobaciones=['SHA-256 de datos y fuentes de gráficos','700 hits y 300 misses por archivo','precondiciones de orden','medias y desviaciones recalculadas','checksums estables e iguales entre lenguajes','comparaciones lineales verificadas por oráculo independiente'])  # Resumen verificable.
(RAIZ / 'resultados/control_calidad.json').write_text(json.dumps(resultado, indent=2, ensure_ascii=False))  # Evidencia persistida.
print(json.dumps(resultado, indent=2, ensure_ascii=False))  # Resultado visible.
