"""Crea una única entrada persistida para ambos lenguajes; semilla 123."""
import random  # Generador pseudoaleatorio reproducible.
import hashlib  # Huellas para verificar identidad de archivos.
import json  # Metadatos legibles.
from pathlib import Path  # Rutas portables.
RAIZ = Path(__file__).resolve().parents[1]  # Localiza el proyecto.
rng = random.Random(123)  # Fija el estado inicial del generador.
manifest = []  # Acumula metadatos por conjunto.
for n in (10000, 100000, 500000):  # Tamaños exigidos.
    uniforme = list(range(n))  # Uniforme consecutivo sin duplicados, como el PDF.
    sesgado = [rng.randrange(n // 10) for _ in range(4 * n // 5)]  # Exactamente 80% en rango estrecho.
    sesgado += [rng.randint(n // 10, 5 * n) for _ in range(n // 5)]  # 20% disperso; duplicados permitidos.
    sesgado.sort()  # Cumple la precondición de orden.
    desordenado = uniforme.copy()  # Conserva los mismos valores que el uniforme.
    rng.shuffle(desordenado)  # Cambia únicamente su orden.
    for tipo, a in [('uniforme', uniforme), ('sesgado', sesgado), ('desordenado', desordenado)]:  # Tres distribuciones.
        q = [a[rng.randrange(n)] for _ in range(700)]  # Hits por posición con reemplazo.
        q += [10 * n + i for i in range(300)]  # Misses distintos por encima de todo valor posible.
        rng.shuffle(q)  # Mezcla aciertos y fallos.
        ruta = RAIZ / 'datos' / f'{tipo}_{n}.txt'  # Archivo de entrada compartido.
        ruta.write_text(f'{n} 1000\n' + ' '.join(map(str, a)) + '\n' + ' '.join(map(str, q)) + '\n')  # Cabecera, datos y consultas.
        presentes = set(a)  # Oráculo de pertenencia fuera del benchmark.
        assert sum(x in presentes for x in q) == 700  # Verifica la proporción exacta.
        manifest.append(dict(dataset=tipo, n=n, hits=700, misses=300, seed=123, sha256=hashlib.sha256(ruta.read_bytes()).hexdigest()))  # Traza reproducible.
(RAIZ / 'datos' / 'manifest.json').write_text(json.dumps(manifest, indent=2))  # Guarda las huellas.
print('Generados 9 datasets; 9000 consultas; semilla 123.')  # Informa el resultado.
