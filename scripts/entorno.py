"""Detecta el entorno visible; no atribuye el hardware al equipo del estudiante."""
import platform  # Sistema y versión de Python.
import subprocess  # Versión del compilador.
import json  # Registro estructurado.
import os  # CPU permitidas al proceso.
from pathlib import Path  # Acceso al sistema y proyecto.
from datetime import datetime, timezone  # Fecha efectiva de ejecución.
raiz = Path(__file__).resolve().parents[1]  # Ubicación del repositorio.
def leer(ruta):  # Detecta campos no disponibles sin inventarlos.
    try:  # Intenta acceder a la información del contenedor.
        return Path(ruta).read_text().strip()  # Devuelve lo informado por el sistema.
    except OSError:  # El sistema puede no exponerlo.
        return 'No disponible'  # Señala explícitamente esa limitación.
cpu = next((s.split(':', 1)[1].strip() for s in leer('/proc/cpuinfo').splitlines() if s.startswith('model name')), 'No disponible')  # Modelo visible.
env = dict(fecha_utc=datetime.now(timezone.utc).isoformat(), so=platform.platform(), distribucion=leer('/etc/os-release'), cpu=cpu, ram_visible=leer('/proc/meminfo').splitlines()[0], limite_ram_cgroup=leer('/sys/fs/cgroup/memory.max'), cpu_cgroup=leer('/sys/fs/cgroup/cpu.max'), cpu_afinidad=sorted(os.sched_getaffinity(0)), python=platform.python_version(), compilador=subprocess.check_output(['g++','--version'], text=True).splitlines()[0], flags='-std=c++17 -O2 -Wall -Wextra -pedantic', nota='Entorno remoto de Work; RAM visible y límite de contenedor son distintos. Sin afinidad fija ni aislamiento exclusivo.')  # Solo datos detectados.
(raiz / 'resultados/entorno.json').write_text(json.dumps(env, indent=2, ensure_ascii=False))  # Evidencia del entorno.
print(json.dumps(env, indent=2, ensure_ascii=False))  # También lo muestra en consola.
def escapar(texto):  # Protege caracteres especiales de LaTeX.
    return str(texto).replace('&',r'\&').replace('_',r'\_').replace('%',r'\%').replace('#',r'\#')  # Los campos de entorno son texto simple.
ram_kib = int(env['ram_visible'].split()[1]) if env['ram_visible'].startswith('MemTotal:') else None  # Convierte solo si se detectó RAM.
ram_texto = f'{ram_kib} KiB (aprox. {ram_kib/1048576:.2f} GiB)' if ram_kib is not None else 'no disponible'  # Mantiene unidades explícitas.
limite = env['limite_ram_cgroup']  # Valor de cgroup disponible.
limite_texto = f'{int(limite)/1073741824:g} GiB' if limite.isdigit() else limite  # «max» significa sin límite informado.
distro = next((s.split('=',1)[1].strip('"') for s in env['distribucion'].splitlines() if s.startswith('PRETTY_NAME=')), 'No disponible')  # Nombre del sistema.
texto = f"Entorno remoto de Work: {distro}, {env['so']}; CPU visible {env['cpu']}; RAM visible {ram_texto}, límite del contenedor {limite_texto}. Python {env['python']}; {env['compilador']}."  # Datos reales del sistema.
latex = escapar(texto) + r' Flags: \texttt{' + escapar(env['flags']) + '}. '  # Flags monoespaciados.
latex += 'Ejecución secuencial, sin fijar afinidad ni aislamiento exclusivo; el nombre del procesador no representa núcleos dedicados. Registro UTC: ' + env['fecha_utc'][:10] + '.\n'  # Aclara alcance del entorno.
(raiz / 'informe/entorno.tex').write_text(latex)  # El informe se actualiza al reproducir.
