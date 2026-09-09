"""Produce tablas y gráficos exclusivamente desde los CSV de ejecuciones."""
from pathlib import Path  # Rutas relativas al proyecto.
import csv  # Lectura de resultados.
import json  # Huellas de fuentes.
import hashlib  # Trazabilidad de gráficos.
import matplotlib  # Motor gráfico exportable.
matplotlib.use('Agg')  # No requiere escritorio.
import matplotlib.pyplot as plt  # Figuras científicas.
RAIZ = Path(__file__).resolve().parents[1]  # Carpeta raíz.
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42})  # Estilo legible.
colores = {'lineal':'#b04b37','binaria':'#16719b','exponencial':'#8262a4','interpolacion':'#23845d'}  # Identidad consistente.
tipos = ['uniforme','sesgado','desordenado']  # Orden de paneles.
filas = []  # Consolida ambos lenguajes.
fuentes = {}  # Registra exactamente qué CSV originaron las figuras.
for lenguaje in ['cpp', 'python']:  # Una figura independiente por lenguaje.
    ruta = RAIZ / 'resultados' / f'resultados_{lenguaje}.csv'  # Fuente de medias y desviaciones.
    datos = list(csv.DictReader(ruta.open()))  # Lee todas las filas.
    assert len(datos) == 27, 'Benchmark incompleto'  # Exige toda la matriz antes de publicar gráficos.
    filas += datos  # Conserva todas las mediciones para tablas.
    fuentes[ruta.name] = hashlib.sha256(ruta.read_bytes()).hexdigest()  # Vincula datos y gráficos.
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 2.65), sharey=True)  # Paneles por distribución.
    for ax, tipo in zip(axes, tipos):  # Cada panel presenta un conjunto.
        for algoritmo, color in colores.items():  # Misma codificación para ambos lenguajes.
            d = sorted([r for r in datos if r['dataset']==tipo and r['algoritmo']==algoritmo], key=lambda r:int(r['n']))  # Ordena por n.
            if not d:  # No existe búsqueda ordenada válida en desordenado.
                continue  # No dibuja resultados ficticios.
            ax.errorbar([int(r['n']) for r in d], [float(r['ms_por_busqueda']) for r in d], yerr=[float(r['sd_ms']) for r in d], marker='o', markersize=3, capsize=2, color=color, label=algoritmo)  # Media y desviación real.
        ax.set(xscale='log', yscale='log', title=tipo.capitalize(), xlabel='Tamaño n (escala log)')  # Escalas indicadas explícitamente.
        ax.set_xticks([10000,100000,500000], ['10 000','100 000','500 000'])  # Muestra los tamaños exactos.
        ax.grid(alpha=.2, which='major')  # Facilita lectura sin decoración.
    axes[0].set_ylabel('ms por búsqueda (escala log)')  # Unidad oficial.
    axes[0].legend(fontsize=7, loc='best')  # Leyenda de las cuatro curvas.
    fig.suptitle(('C++' if lenguaje=='cpp' else 'Python') + ' · Media de 3 lotes; barras: ±1 desviación muestral', fontsize=10)  # Estadístico representado.
    fig.tight_layout(pad=.6)  # Evita recortes.
    for extension in ['png','pdf']:  # Vista rápida y figura vectorial para LaTeX.
        fig.savefig(RAIZ / 'graficos' / f'tiempos_{lenguaje}.{extension}', dpi=200, bbox_inches='tight')  # Exporta resultados.
    plt.close(fig)  # Libera memoria.
ruta = RAIZ / 'resultados/comparaciones.csv'  # Conteo experimental separado.
conteos = list(csv.DictReader(ruta.open()))  # Lee conteos medidos.
fuentes[ruta.name] = hashlib.sha256(ruta.read_bytes()).hexdigest()  # Huella de la tercera fuente.
fig, axes = plt.subplots(1, 3, figsize=(10.8, 2.65), sharey=True)  # Igual disposición que tiempos.
for ax, tipo in zip(axes, tipos):  # Paneles por dataset.
    for algoritmo, color in colores.items():  # Curvas de comparaciones.
        d = [r for r in conteos if r['dataset']==tipo and r['algoritmo']==algoritmo]  # Selecciona observaciones válidas.
        if d:  # No representa algoritmos ausentes.
            ax.plot([int(r['n']) for r in d], [float(r['comparaciones_promedio']) for r in d], '-o', markersize=3, color=color, label=algoritmo)  # Conteos por búsqueda.
    ax.set(xscale='log', yscale='log', title=tipo.capitalize(), xlabel='Tamaño n (escala log)')  # Escalas comparables.
    ax.set_xticks([10000,100000,500000], ['10 000','100 000','500 000'])  # Tamaños oficiales.
    ax.grid(alpha=.2)  # Guías visuales.
axes[0].set_ylabel('Comparaciones por búsqueda (log)')  # Define la magnitud.
axes[0].legend(fontsize=7)  # Identifica algoritmos.
fig.suptitle('C++ instrumentado · Comparaciones entre claves; fuera del cronómetro', fontsize=10)  # Alcance del conteo.
fig.tight_layout(pad=.6)  # Ajusta márgenes.
for extension in ['png','pdf']:  # Dos formatos utilizables.
    fig.savefig(RAIZ / 'graficos' / f'comparaciones.{extension}', dpi=200, bbox_inches='tight')  # Guarda la figura.
plt.close(fig)  # Cierra figura.
(RAIZ / 'graficos/fuentes_sha256.json').write_text(json.dumps(fuentes, indent=2))  # Trazabilidad reproducible.
texto = '| Lenguaje | Dataset | n | Lineal | Binaria | Exponencial | Interpolación |\n|---|---|---:|---:|---:|---:|---:|\n'  # Tabla completa en ms/búsqueda.
latex = []  # Filas compactas de la tabla del informe.
for lenguaje in ['C++','Python']:  # Orden coherente.
    for tipo in tipos:  # Todas las distribuciones.
        for n in [10000,100000,500000]:  # Sin omitir tamaños.
            valores = {r['algoritmo']:float(r['ms_por_busqueda']) for r in filas if r['lenguaje']==lenguaje and r['dataset']==tipo and int(r['n'])==n}  # Recupera medias.
            celdas = [f'{valores[a]:.6g}' if a in valores else '--' for a in colores]  # Mantiene precisión y ausencias explícitas.
            texto += f'| {lenguaje} | {tipo} | {n} | ' + ' | '.join(celdas) + ' |\n'  # Añade fila legible.
            latex.append(f'{lenguaje} & {tipo} & {n:,}'.replace(',', r'\,') + ' & ' + ' & '.join(celdas) + r' \\')  # Tabla LaTeX derivada.
(RAIZ / 'resultados/TABLAS.md').write_text('# Tiempos reales: ms por búsqueda\n\n' + texto + '\n--: no aplicable por precondición de orden. Desviaciones en CSV.\n')  # Tabla de todos los resultados.
(RAIZ / 'informe/tabla_resultados.tex').write_text('\n'.join(latex) + '\n')  # Entrada automática del informe.
print('Gráficos y tablas generados desde 54 medias reales y 27 conteos.')  # Evidencia del origen.
def tiempo(lenguaje, tipo, n, algoritmo):  # Recupera una media ya leída para el análisis automático.
    return next(float(r['ms_por_busqueda']) for r in filas if r['lenguaje']==lenguaje and r['dataset']==tipo and int(r['n'])==n and r['algoritmo']==algoritmo)  # Exige una fila existente.
metricas = {}  # Macros del informe vinculadas al CSV.
for etiqueta, lenguaje in [('Cpp','C++'), ('Py','Python')]:  # Ratios dentro de cada lenguaje.
    metricas['VentajaBinaria'+etiqueta] = tiempo(lenguaje,'uniforme',500000,'lineal') / tiempo(lenguaje,'uniforme',500000,'binaria')  # Aceleración observada.
    metricas['PenalidadInterpolacion'+etiqueta] = tiempo(lenguaje,'sesgado',500000,'interpolacion') / tiempo(lenguaje,'sesgado',500000,'binaria')  # Efecto del sesgo.
    metricas['CrecimientoLineal'+etiqueta] = tiempo(lenguaje,'uniforme',500000,'lineal') / tiempo(lenguaje,'uniforme',10000,'lineal')  # Cambio frente a n multiplicado por 50.
    metricas['VentajaInterpolacion'+etiqueta] = tiempo(lenguaje,'uniforme',500000,'binaria') / tiempo(lenguaje,'uniforme',500000,'interpolacion')  # Caso consecutivo favorable.
(RAIZ / 'informe/metricas.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+f'{v:.1f}'+'}' for k,v in metricas.items()))  # Evita copiar cifras manualmente.
