#include <algorithm> // Ordenamiento y límites mínimo/máximo.
#include <chrono> // Cronómetro monotónico.
#include <cmath> // Desviación estándar.
#include <fstream> // Archivos de entrada y CSV.
#include <iomanip> // Precisión suficiente para tiempos pequeños.
#include <iostream> // Consola.
#include <random> // Casos aleatorios reproducibles.
#include <stdexcept> // Fallos explícitos de validación.
#include <string> // Nombres y rutas.
#include <vector> // Arreglos dinámicos contiguos.
using namespace std; // Simplifica los nombres de la biblioteca estándar.
long long comparaciones = 0; // Contador usado solo en la ejecución instrumentada.
template<bool contar> bool igual(int a, int b) { // Comparación de claves con instrumentación opcional.
    if constexpr(contar) ++comparaciones; // El compilador elimina este código si contar=false.
    return a == b; // Evalúa igualdad.
}
template<bool contar> bool menor(int a, int b) { // Comparación estricta de claves.
    if constexpr(contar) ++comparaciones; // Cuenta solo en la pasada no cronometrada.
    return a < b; // Evalúa menor que.
}
template<bool contar> int lineal(const vector<int>& a, int x) { // No requiere orden.
    for (int i=0; i<static_cast<int>(a.size()); ++i) { // Recorre cada posición.
        if (igual<contar>(a[i],x)) return i; // Devuelve la primera coincidencia.
    }
    return -1; // No encontró la clave.
}
template<bool contar> int binariaRango(const vector<int>& a, int x, int lo, int hi) { // Intervalo ordenado inclusivo.
    while (lo<=hi) { // Hay posiciones candidatas.
        int medio=lo+(hi-lo)/2; // Evita sumar directamente los extremos.
        if (igual<contar>(a[medio],x)) return medio; // Coincidencia encontrada.
        if (menor<contar>(a[medio],x)) lo=medio+1; // Conserva mitad derecha.
        else hi=medio-1; // Conserva mitad izquierda.
    }
    return -1; // Intervalo agotado.
}
template<bool contar> int binaria(const vector<int>& a, int x) { // Entrada ordenada.
    return binariaRango<contar>(a,x,0,static_cast<int>(a.size())-1); // Busca en todo el arreglo.
}
template<bool contar> int exponencial(const vector<int>& a, int x) { // Acota antes de aplicar binaria.
    if (a.empty()) return -1; // Protege el acceso inicial.
    if (igual<contar>(a[0],x)) return 0; // Resuelve la primera posición.
    size_t i=1; // Inicia las potencias de dos.
    while (i<a.size() && menor<contar>(a[i],x)) i*=2; // Amplía la cota mientras sea necesario.
    return binariaRango<contar>(a,x,static_cast<int>(i/2),static_cast<int>(min(i,a.size()-1))); // Refina el rango válido.
}
template<bool contar> int interpolacion(const vector<int>& a, int x) { // Usa el valor para estimar posición.
    int lo=0, hi=static_cast<int>(a.size())-1; // Intervalo inicial; vacío si hi=-1.
    while (lo<=hi && !menor<contar>(x,a[lo]) && !menor<contar>(a[hi],x)) { // Comprueba límites antes de acceder.
        if (igual<contar>(a[lo],a[hi])) return lo; // Evita división entre cero; x coincide por el control previo.
        long long numerador=(static_cast<long long>(x)-a[lo])*(hi-lo); // Amplía antes de restar y multiplicar.
        int pos=lo+static_cast<int>(numerador/(static_cast<long long>(a[hi])-a[lo])); // Posición entera exacta.
        if (igual<contar>(a[pos],x)) return pos; // Comprueba la estimación.
        if (menor<contar>(a[pos],x)) lo=pos+1; // Avanza el extremo inferior.
        else hi=pos-1; // Retrocede el extremo superior.
    }
    return -1; // Fuera del intervalo restante.
}
using Funcion=int(*)(const vector<int>&,int); // Tipo de las funciones de búsqueda.
vector<Funcion> funciones={lineal<false>,binaria<false>,exponencial<false>,interpolacion<false>}; // Versiones cronometradas sin contador.
vector<Funcion> contadas={lineal<true>,binaria<true>,exponencial<true>,interpolacion<true>}; // Versiones instrumentadas aparte.
vector<string> nombres={"lineal","binaria","exponencial","interpolacion"}; // Nombres exportados.
void verificar(const vector<int>& a,int x,int i) { // Valida cualquier índice correcto con duplicados.
    bool existe=find(a.begin(),a.end(),x)!=a.end(); // Oráculo independiente fuera del cronómetro.
    if (!((i==-1 && !existe)||(i>=0 && i<static_cast<int>(a.size()) && a[i]==x))) throw runtime_error("Resultado incorrecto"); // Detiene ante error.
}
int main(int argc,char** argv) { // Ejecutar desde raíz o pasar la ruta como argumento.
    string raiz=argc>1?argv[1]:"."; // Directorio del proyecto.
    cout<<setprecision(12); // No oculta mediciones diminutas.
    mt19937 rng(456); // Semilla de pruebas.
    vector<vector<int>> casos={{},{7},{5,5,5},{-9,-2,0,4,12},{-2147483647-1,0,2147483647}}; // Casos límite.
    for(int k=1;k<=50;++k) { // Genera arreglos cortos con repetidos.
        vector<int> a(k); // Reserva el tamaño del caso.
        for(int& v:a) v=static_cast<int>(rng()%61)-30; // Valores negativos, positivos y cero.
        sort(a.begin(),a.end()); // Cumple la precondición.
        casos.push_back(a); // Agrega a las pruebas.
    }
    for(const auto& a:casos) { // Prueba algoritmos ordinarios e instrumentados.
        vector<int> q=a; // Incluye extremos e intermedios presentes.
        for(int x=-35;x<=35;++x) q.push_back(x); // Incluye huecos y valores externos.
        for(int x:q) for(int j=0;j<4;++j) { // Todas las combinaciones válidas.
            verificar(a,x,funciones[j](a,x)); // Comprueba la versión cronometrada.
            verificar(a,x,contadas[j](a,x)); // Comprueba la versión contada.
        }
    }
    for(int x:{9,1,7,3,2}) verificar({9,1,7,3},x,lineal<false>({9,1,7,3},x)); // Solo lineal en desordenado.
    cout<<"Correctitud C++: casos limite y aleatorios OK.\n"; // Evidencia verificable.
    ofstream salida(raiz+"/resultados/resultados_cpp.csv"), raw(raiz+"/resultados/repeticiones_cpp.csv"), cnt(raiz+"/resultados/comparaciones.csv"); // Salidas separadas.
    if(!salida || !raw || !cnt) throw runtime_error("No se pueden abrir salidas"); // Impide una falsa ejecución exitosa.
    salida<<setprecision(12); raw<<setprecision(12); cnt<<setprecision(12); // Conserva precisión.
    salida<<"lenguaje,algoritmo,dataset,n,ms_por_busqueda,sd_ms,repeticiones,hits,misses,consultas\n"; // Resumen.
    raw<<"lenguaje,dataset,n,algoritmo,repeticion,ms_por_busqueda,checksum\n"; // Tiempos individuales.
    cnt<<"dataset,n,algoritmo,comparaciones_promedio\n"; // Comparaciones entre valores, no controles de índices.
    for(int n:{10000,100000,500000}) for(string tipo:{"uniforme","sesgado","desordenado"}) { // Matriz experimental.
        ifstream entrada(raiz+"/datos/"+tipo+"_"+to_string(n)+".txt"); // Datos compartidos con Python.
        int tam=0,m=0; entrada>>tam>>m; // Lee cabecera.
        if(tam!=n || m!=1000) throw runtime_error("Cabecera invalida"); // Exige tamaño y consultas oficiales.
        vector<int>a(n),q(m); // Arreglo y consultas separados.
        for(int& v:a) entrada>>v; // Carga fuera del cronómetro.
        for(int& x:q) entrada>>x; // Conserva idéntico orden de consultas.
        if(!entrada) throw runtime_error("Entrada incompleta"); // Detecta truncamientos.
        int cantidad=tipo=="desordenado"?1:4; // Restringe algoritmos a sus precondiciones.
        if(cantidad==4 && !is_sorted(a.begin(),a.end())) throw runtime_error("Falta orden"); // Verifica orden real.
        for(int j=0;j<cantidad;++j) for(int x:q) verificar(a,x,funciones[j](a,x)); // Todas las consultas antes de medir.
        volatile long long calentamiento=0; // Resultado observable para impedir eliminación.
        for(int j=0;j<cantidad;++j) for(int k=0;k<20;++k) calentamiento+=funciones[j](a,q[k]); // Calentamiento no medido.
        vector<vector<double>> tiempos(cantidad); // Tres muestras por algoritmo.
        for(int rep=0;rep<3;++rep) for(int k=0;k<cantidad;++k) { // Lotes secuenciales con orden rotado.
            int j=(k+rep)%cantidad; // Alterna el algoritmo que empieza.
            long long checksum=0; // Acumula resultados usados en el CSV.
            auto inicio=chrono::steady_clock::now(); // Cronómetro monotónico.
            for(int x:q) checksum+=funciones[j](a,x); // Mil búsquedas con la misma lista.
            double ms=chrono::duration<double,milli>(chrono::steady_clock::now()-inicio).count()/m; // Media por búsqueda.
            tiempos[j].push_back(ms); // Preserva medición real.
            raw<<"C++,"<<tipo<<','<<n<<','<<nombres[j]<<','<<rep+1<<','<<ms<<','<<checksum<<'\n'; // Evidencia cruda.
        }
        for(int j=0;j<cantidad;++j) { // Calcula estadísticos.
            double media=0,sd=0; // Acumuladores.
            for(double t:tiempos[j]) media+=t/3; // Media aritmética de lotes iguales.
            for(double t:tiempos[j]) sd+=(t-media)*(t-media)/2; // Varianza muestral, tres observaciones.
            salida<<"C++,"<<nombres[j]<<','<<tipo<<','<<n<<','<<media<<','<<sqrt(sd)<<",3,700,300,1000\n"; // Resumen persistido.
            cout<<tipo<<','<<n<<','<<nombres[j]<<','<<media<<" ms/busqueda\n"; // Resultado en consola.
            comparaciones=0; // Reinicia el contador fuera de toda medición temporal.
            for(int x:q) { // Misma mezcla de hits y misses.
                int i=contadas[j](a,x); // Cuenta comparaciones efectivamente evaluadas.
                if(i!=funciones[j](a,x)) throw runtime_error("Instrumentacion divergente"); // Verifica equivalencia exacta.
            }
            cnt<<tipo<<','<<n<<','<<nombres[j]<<','<<comparaciones/static_cast<double>(m)<<'\n'; // Promedio estructural.
        }
    }
    return 0; // Finalización correcta.
}
