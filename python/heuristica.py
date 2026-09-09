"""Selector orientativo; los umbrales son propuestos, no óptimos demostrados."""
import math  # Estima costos por crecimiento asintótico.

def seleccionar(a, consultas=1, orden_certificado=False, limite_conocido=True):  # Metadatos y carga prevista.
    if not limite_conocido:  # Interfaz conceptual sin tamaño efectivo conocido.
        return 'exponencial con acceso seguro' if orden_certificado else 'lineal hasta fin de fuente'  # No aplica exponencial sin orden.
    n = len(a)  # Aquí sí está disponible la longitud.
    if n < 64:  # Umbral didáctico para conjuntos pequeños.
        return 'lineal'  # Evita preparación desproporcionada.
    ordenado = orden_certificado or all(a[i-1] <= a[i] for i in range(1, n))  # Un muestreo no certifica orden; revisar una vez cuesta O(n).
    if not ordenado:  # Considera amortizar el ordenamiento.
        costo_lineal = consultas * n  # Modelo simple: hasta n pasos por consulta.
        costo_ordenar = n * math.log2(n) + consultas * math.log2(n)  # Ordenar y luego buscar.
        return 'ordenar una copia y usar binaria' if costo_ordenar < costo_lineal else 'lineal'  # Decisión orientativa sin mutar datos.
    if a[0] == a[-1]:  # Evita normalizar por cero.
        return 'binaria'  # Alternativa segura para valores iguales.
    indices = [i * (n-1) // 32 for i in range(33)]  # Muestra posiciones repartidas, incluidos extremos.
    error = max(abs((a[i]-a[0])/(a[-1]-a[0]) - i/(n-1)) for i in indices)  # Desviación de la relación lineal valor-posición.
    return 'interpolacion' if error <= 0.05 else 'binaria'  # Uniformidad aproximada; sin garantía de rapidez.

if __name__ == '__main__':  # Demostración sin incorporarla a los tiempos principales.
    assert seleccionar(list(range(100))) == 'interpolacion'  # Caso uniformemente espaciado.
    assert seleccionar(list(range(100, 0, -1)), consultas=1) == 'lineal'  # Pocas consultas sin orden.
    assert seleccionar(list(range(100, 0, -1)), consultas=1000) == 'ordenar una copia y usar binaria'  # Amortización propuesta.
    assert seleccionar(None, orden_certificado=True, limite_conocido=False) == 'exponencial con acceso seguro'  # No requiere len en esta rama.
    print('Heurística: cuatro casos de decisión OK.')  # Evidencia de funcionamiento.
