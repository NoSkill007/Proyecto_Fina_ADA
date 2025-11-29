import random
import time
import tracemalloc
import matplotlib.pyplot as plt


# ============================================================
# 1. MODELO DE DATOS
# ============================================================

class Estudiante:
    """
    Representa un estudiante dentro del sistema.
    Se limita el índice académico al rango UTP Panamá (0.00 – 3.00).
    """

    def __init__(self, matricula, nombre, promedio):
        # Se asegura que el índice siga la escala UTP (0 a 3)
        self.matricula = matricula
        self.nombre = nombre
        self.promedio = max(0.0, min(3.0, promedio))

    def __repr__(self):
        # Formato legible para inspección rápida en consola
        return f"[ID: {self.matricula} | Índice: {self.promedio:.2f}] {self.nombre}"

    def __eq__(self, other):
        return (self.matricula == other.matricula and
                self.promedio == other.promedio)


# ============================================================
# 2. ORDENAMIENTO
# ============================================================

class Ordenador:

    @staticmethod
    def seleccion_directa(lista_original):
        """
        Implementación tradicional del algoritmo de Selección.
        Se elige el mayor índice en cada iteración y se coloca adelante.
        Este método es O(n²), por lo que es útil como comparación,
        pero no recomendable para grandes cantidades de estudiantes.
        """
        lista = list(lista_original)
        n = len(lista)

        for i in range(n):
            indice_mayor = i
            # Exploración del resto de la lista en busca de un índice mayor
            for j in range(i + 1, n):
                if lista[j].promedio > lista[indice_mayor].promedio:
                    indice_mayor = j

            # Intercambio de elementos
            lista[i], lista[indice_mayor] = lista[indice_mayor], lista[i]

        return lista

    @staticmethod
    def mergesort(lista):
        """
        MergeSort recursivo clásico (O(n log n)).
        Su ventaja principal es la estabilidad y un rendimiento muy consistente,
        incluso para tamaños grandes.
        """
        if len(lista) <= 1:
            return lista

        medio = len(lista) // 2
        izquierda = Ordenador.mergesort(lista[:medio])
        derecha = Ordenador.mergesort(lista[medio:])
        return Ordenador._mezclar(izquierda, derecha)

    @staticmethod
    def _mezclar(izquierda, derecha):
        """
        Fusiona dos listas previamente ordenadas.
        Esta fase domina la eficiencia del algoritmo.
        """
        resultado = []
        i = j = 0

        while i < len(izquierda) and j < len(derecha):
            if izquierda[i].promedio >= derecha[j].promedio:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        # Agrega cualquier remanente sin comparaciones adicionales
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado


# ============================================================
# 3. BÚSQUEDA
# ============================================================

class Buscador:

    @staticmethod
    def secuencial(lista, id_buscado):
        """
        Búsqueda lineal pura.
        Útil para listas pequeñas o no ordenadas.
        """
        pasos = 0
        for est in lista:
            pasos += 1
            if est.matricula == id_buscado:
                return est, pasos
        return None, pasos

    @staticmethod
    def binaria(lista, id_buscado):
        """
        Búsqueda binaria.
        Solo funciona correctamente si la lista está ordenada por matrícula.
        Su complejidad es O(log n), lo que la hace ideal para grandes volúmenes.
        """
        izquierda = 0
        derecha = len(lista) - 1
        pasos = 0

        while izquierda <= derecha:
            pasos += 1
            medio = (izquierda + derecha) // 2
            estudiante = lista[medio]

            if estudiante.matricula == id_buscado:
                return estudiante, pasos

            # Se reduce el espacio de búsqueda
            if estudiante.matricula < id_buscado:
                izquierda = medio + 1
            else:
                derecha = medio - 1

        return None, pasos


# ============================================================
# 4. GENERACIÓN Y MEDICIÓN
# ============================================================

def generar_estudiantes(cantidad):
    """
    Crea una lista aleatoria de estudiantes con índices dentro de la escala 0 Y 3.
    Se usa esta generación automática para poder medir rendimiento
    sin depender de entradas manuales.
    """
    nombres = ["Ana", "Luis", "Pepe", "Maria", "Sofia", "Carlos", "Fernanda", "Diego"]
    lista = []

    print(f"Generando {cantidad} estudiantes para pruebas...")

    for i in range(cantidad):
        matricula = 1000 + i
        nombre = random.choice(nombres) + f"_{i}"
        promedio = round(random.uniform(0.0, 3.0), 2)  # índice UTP
        lista.append(Estudiante(matricula, nombre, promedio))

    random.shuffle(lista)
    print("Datos generados.\n")
    return lista


def medir_rendimiento(funcion, datos, **kwargs):
    """
    Ejecuta un algoritmo y devuelve su tiempo de ejecución
    y el consumo pico de memoria.
    """
    tracemalloc.start()
    inicio = time.time()

    funcion(datos, **kwargs)

    fin = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return fin - inicio, peak


# ============================================================
# 5. VALIDACIÓN Y BENCHMARK
# ============================================================

class Validador:

    @staticmethod
    def prueba_correccion():
        """
        Valida que los algoritmos produzcan resultados correctos.
        Esto asegura que las comparaciones empíricas sean confiables.
        """
        print("Ejecutando pruebas de integridad...\n")
        datos = generar_estudiantes(50)

        # Validar MergeSort contra sorted()
        esperado = sorted(datos, key=lambda x: x.promedio, reverse=True)
        obtenido = Ordenador.mergesort(datos)

        if all(obtenido[i].promedio >= obtenido[i + 1].promedio
               for i in range(len(obtenido) - 1)):
            print("✔ MergeSort ordena correctamente.")
        else:
            print("✘ Error en MergeSort.")

        # Validación de búsquedas sobre el mismo elemento
        objetivo = datos[25]

        res_lin, _ = Buscador.secuencial(datos, objetivo.matricula)
        print("✔ Búsqueda lineal OK." if res_lin else "✘ Error en búsqueda lineal.")

        datos_ordenados = sorted(datos, key=lambda x: x.matricula)
        res_bin, _ = Buscador.binaria(datos_ordenados, objetivo.matricula)
        print("✔ Búsqueda binaria OK.\n" if res_bin else "✘ Error en búsqueda binaria.\n")

    @staticmethod
    def reporte_masivo():
        """
        Evalúa el rendimiento real con diferentes volúmenes de datos.
        Se recopilan tiempos de ejecución para graficarlos.
        """
        cantidades = [100, 500, 1000, 2500, 5000]

        tiempos_sel = []
        tiempos_mer = []
        tiempos_lin = []
        tiempos_bin = []

        print("Iniciando benchmark...\n")
        print(f"{'Registros':<12} | {'MergeSort':<12} | {'Selección':<12} | {'Binaria':<10} | {'Lineal'}")
        print("-" * 65)

        for n in cantidades:
            datos = generar_estudiantes(n)

            # Medición MergeSort
            t_mer, _ = medir_rendimiento(Ordenador.mergesort, datos)
            tiempos_mer.append(t_mer)

            # Selección Directa solo para tamaños razonables
            if n < 3000:
                t_sel, _ = medir_rendimiento(Ordenador.seleccion_directa, datos)
            else:
                t_sel = 0.0
            tiempos_sel.append(t_sel)

            # Búsqueda
            objetivo = datos[-1].matricula
            datos_por_id = sorted(datos, key=lambda x: x.matricula)

            t_lin, _ = medir_rendimiento(Buscador.secuencial, datos, id_buscado=objetivo)
            t_bin, _ = medir_rendimiento(Buscador.binaria, datos_por_id, id_buscado=objetivo)

            tiempos_lin.append(t_lin)
            tiempos_bin.append(t_bin)

            print(f"{n:<12} | {t_mer:.6f} | {t_sel if t_sel else 'N/A':<12} | {t_bin:.6f}   | {t_lin:.6f}")

        Validador.graficar(cantidades, tiempos_sel, tiempos_mer, tiempos_lin, tiempos_bin)

    @staticmethod
    def graficar(x, y_sel, y_mer, y_lin, y_bin):
        plt.style.use("ggplot")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle("Rendimiento Algorítmico", fontsize=18)

        # Ordenamiento
        ax1.plot(x, y_mer, marker="o", label="MergeSort")
        ax1.plot([x[i] for i in range(len(y_sel)) if y_sel[i] > 0],
                 [v for v in y_sel if v > 0],
                 marker="s", label="Selección Directa")

        ax1.set_title("Ordenamiento")
        ax1.set_xlabel("Cantidad de Estudiantes")
        ax1.set_ylabel("Tiempo (s)")
        ax1.legend()
        ax1.grid(True)

        # Búsqueda
        ax2.plot(x, y_lin, marker="^", label="Lineal")
        ax2.plot(x, y_bin, marker="D", label="Binaria")

        ax2.set_title("Búsqueda")
        ax2.set_xlabel("Cantidad de Estudiantes")
        ax2.set_ylabel("Tiempo (s)")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()


# ============================================================
# 6. MENÚ DEL SISTEMA
# ============================================================

def solicitar_entero(mensaje):
    """Solicita un entero válido sin interrumpir la ejecución."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada inválida. Intenta nuevamente.\n")


def mostrar_encabezado():
    print("\n" + "=" * 60)
    print("         SISTEMA DE GESTIÓN DE BECAS UNIVERSITARIAS")
    print("=" * 60)


def menu():
    lista_actual = generar_estudiantes(50)

    while True:
        mostrar_encabezado()
        print(f"Estudiantes cargados: {len(lista_actual)}\n")
        print("1. Generar una nueva lista de estudiantes")
        print("2. Mostrar los primeros 10 estudiantes")
        print("3. Ordenar ranking por índice (MergeSort)")
        print("4. Buscar estudiante por matrícula")
        print("5. Ejecutar análisis de rendimiento completo")
        print("6. Salir\n")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            cantidad = solicitar_entero("Cantidad de estudiantes a generar: ")
            lista_actual = generar_estudiantes(cantidad)

        elif opcion == "2":
            print("\nPrimeros 10 registros:\n")
            for e in lista_actual[:10]:
                print(e)
            print()

        elif opcion == "3":
            inicio = time.time()
            lista_actual = Ordenador.mergesort(lista_actual)
            fin = time.time()

            print(f"\nLista ordenada en {fin - inicio:.6f} segundos.\n")
            print("Top 5 por índice:\n")
            for i, est in enumerate(lista_actual[:5], start=1):
                print(f"{i}. {est}")
            print()

        elif opcion == "4":
            id_buscado = solicitar_entero("Matrícula del estudiante: ")

            # Comparación real entre métodos
            t0 = time.time()
            res_lin, pasos_lin = Buscador.secuencial(lista_actual, id_buscado)
            t1 = time.time()

            lista_id = sorted(lista_actual, key=lambda x: x.matricula)
            t2 = time.time()
            res_bin, pasos_bin = Buscador.binaria(lista_id, id_buscado)
            t3 = time.time()

            if res_bin:
                print(f"\nEncontrado: {res_bin}\n")
                print("Comparativa de métodos:")
                print(f"- Lineal : {t1 - t0:.6f}s | {pasos_lin} pasos")
                print(f"- Binaria: {t3 - t2:.6f}s | {pasos_bin} pasos\n")
            else:
                print("\nNo se encontró la matrícula especificada.\n")

        elif opcion == "5":
            Validador.prueba_correccion()
            Validador.reporte_masivo()

        elif opcion == "6":
            print("\nSaliendo del sistema...\n")
            break

        else:
            print("Opción no válida.\n")


if __name__ == "__main__":
    menu()
