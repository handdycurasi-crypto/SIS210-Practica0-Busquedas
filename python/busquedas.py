"""Algoritmos manuales: índice válido o -1; cualquier coincidencia si hay duplicados."""

def lineal(a, x):  # No exige orden previo.
    for i, valor in enumerate(a):  # Recorre índices y valores de izquierda a derecha.
        if valor == x:  # Comprueba si encontró la clave.
            return i  # Devuelve la posición encontrada.
    return -1  # Agotó los elementos sin encontrar la clave.

def binaria_rango(a, x, lo, hi):  # Busca dentro de un intervalo inclusivo ordenado.
    while lo <= hi:  # Continúa mientras queden candidatos.
        medio = lo + (hi - lo) // 2  # Calcula la posición central.
        if a[medio] == x:  # Comprueba la coincidencia.
            return medio  # Devuelve el índice encontrado.
        if a[medio] < x:  # La clave solo puede estar a la derecha.
            lo = medio + 1  # Descarta centro y mitad izquierda.
        else:  # La clave es menor que el valor central.
            hi = medio - 1  # Descarta centro y mitad derecha.
    return -1  # El intervalo quedó vacío.

def binaria(a, x):  # Exige arreglo ordenado de menor a mayor.
    return binaria_rango(a, x, 0, len(a) - 1)  # Inicia con todo el arreglo.

def exponencial(a, x):  # Exige orden; primero obtiene una cota.
    if not a:  # Evita acceder a un arreglo vacío.
        return -1  # No existen elementos.
    if a[0] == x:  # Resuelve inmediatamente el primer elemento.
        return 0  # Índice del primer elemento.
    i = 1  # Primera posición que se probará al acotar.
    while i < len(a) and a[i] < x:  # No sale del arreglo ni supera la clave.
        i *= 2  # Duplica la posición: 1, 2, 4, 8...
    return binaria_rango(a, x, i // 2, min(i, len(a) - 1))  # Refina el rango.

def interpolacion(a, x):  # Exige orden; estima la posición usando los valores.
    lo, hi = 0, len(a) - 1  # Define extremos inclusivos; el vacío tiene hi=-1.
    while lo <= hi and a[lo] <= x <= a[hi]:  # Verifica intervalo y límites de valor.
        if a[lo] == a[hi]:  # Evita dividir entre cero cuando todos son iguales.
            return lo  # El control anterior garantiza que ese valor es x.
        pos = lo + (x - a[lo]) * (hi - lo) // (a[hi] - a[lo])  # Estimación entera exacta.
        if a[pos] == x:  # Comprueba la posición estimada.
            return pos  # Devuelve una coincidencia válida.
        if a[pos] < x:  # La clave debe estar más a la derecha.
            lo = pos + 1  # Garantiza avance incluso con duplicados.
        else:  # El valor estimado excede la clave.
            hi = pos - 1  # Reduce el extremo superior.
    return -1  # La clave no pertenece al intervalo restante.

ALGORITMOS = {'lineal': lineal, 'binaria': binaria, 'exponencial': exponencial, 'interpolacion': interpolacion}  # Registro común.

if __name__ == '__main__':  # Ejecuta un ejemplo solo al abrir este archivo como programa.
    datos = [2, 4, 8, 12, 18]  # Arreglo ordenado para los cuatro algoritmos.
    for nombre, funcion in ALGORITMOS.items():  # Recorre las implementaciones.
        print(nombre, 'buscar 8:', funcion(datos, 8), 'buscar 7:', funcion(datos, 7))  # Muestra hit y miss.
