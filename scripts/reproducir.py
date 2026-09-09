"""Reproduce secuencialmente datos, pruebas, mediciones, figuras y PDF."""
from pathlib import Path  # Rutas portables.
import subprocess  # Ejecuta herramientas y detiene ante errores.
import sys  # Reutiliza el intérprete seleccionado.
RAIZ = Path(__file__).resolve().parents[1]  # Raíz independiente del directorio actual.

def ejecutar(comando, registro=None, directorio=RAIZ):  # Ejecuta y conserva consola.
    print('Ejecutando:', ' '.join(map(str,comando)), flush=True)  # Informa la etapa.
    if registro is None:  # Comando corto sin registro especial.
        subprocess.run(comando, cwd=directorio, check=True)  # Falla de manera explícita ante código no cero.
    else:  # Conserva evidencia de comandos de prueba y benchmark.
        with (RAIZ / registro).open('w') as salida:  # Reemplaza el registro de la nueva ejecución.
            proceso = subprocess.Popen(comando, cwd=directorio, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)  # Combina salida y errores.
            for linea in proceso.stdout:  # Transmite mientras el proceso trabaja.
                print(linea, end='', flush=True)  # Muestra cada resultado en consola.
                salida.write(linea)  # Guarda exactamente el mismo texto.
            if proceso.wait() != 0:  # Comprueba la finalización.
                raise RuntimeError('Comando fallido; revise '+registro)  # No continúa con resultados incompletos.

(RAIZ / 'build').mkdir(exist_ok=True)  # Carpeta ignorada por Git.
ejecutar([sys.executable,'scripts/generar_datos.py'])  # Misma semilla y archivos para ambos lenguajes.
ejecutar([sys.executable,'scripts/entorno.py'], 'resultados/entorno.log')  # Detecta el equipo de esta ejecución.
ejecutar(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic','cpp/busquedas.cpp','-o','build/busquedas'], 'resultados/compilacion_cpp.log')  # Compila con flags documentados.
ejecutar([str(RAIZ / 'build/busquedas'),str(RAIZ)], 'resultados/ejecucion_cpp.log')  # C++ primero; prueba y mide.
ejecutar([sys.executable,'-u','scripts/benchmark_python.py'], 'resultados/ejecucion_python.log')  # Python después, sin benchmark simultáneo.
ejecutar([sys.executable,'python/heuristica.py'], 'resultados/heuristica.log')  # Prueba decisiones de la propuesta.
ejecutar([sys.executable,'scripts/graficar.py'])  # Actualiza tablas y métricas desde CSV.
ejecutar([sys.executable,'scripts/validar_resultados.py'], 'resultados/validacion.log')  # Audita el conjunto final.
for _ in range(2):  # Resuelve referencias y marcadores de LaTeX.
    ejecutar(['pdflatex','-interaction=nonstopmode','-halt-on-error','informe.tex'], 'resultados/compilacion_latex.log', RAIZ / 'informe')  # Compila realmente en su carpeta.
print('Proceso completo. Revise visualmente informe/informe.pdf antes de entregar una nueva ejecución.')  # La inspección visual no se sustituye por compilar.
