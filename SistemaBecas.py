import random
import time
import sys
import tracemalloc
import matplotlib.pyplot as plt


# ==========================================
# 1. ESTRUCTURA DE DATOS
# ==========================================

class Estudiante:
    def __init__(self, matricula, nombre, promedio):
        self.matricula = matricula
        self.nombre = nombre
        self.promedio = promedio

    def __repr__(self):
        # Formato de texto para visualizar el objeto en consola
        return f"[ID: {self.matricula} | Promedio: {self.promedio:.2f}] {self.nombre}"

    def __eq__(self, other):
        # Permite comparar si dos estudiantes son iguales basándose en sus datos
        return (self.matricula == other.matricula and
                self.promedio == other.promedio)


# ==========================================
# 2. ALGORITMOS DE ORDENAMIENTO
# ==========================================

class Ordenador:

    @staticmethod
    def seleccion_directa(lista_original):
        """
        Implementación del algoritmo de Selección Directa.
        Busca el elemento mayor de la lista no ordenada y lo coloca en la posición correcta.
        Nota: Este método realiza múltiples pasadas sobre la lista, por lo que es menos
        performante en grandes volúmenes de datos.
        """
        # Se trabaja sobre una copia para mantener la inmutabilidad de la lista original
        lista = list(lista_original)
        n = len(lista)

        for i in range(n):
            # Asumimos inicialmente que el elemento actual es el mayor
            indice_mayor = i
            # Iteramos sobre el resto de la lista para encontrar un candidato mejor
            for j in range(i + 1, n):
                if lista[j].promedio > lista[indice_mayor].promedio:
                    indice_mayor = j

            # Intercambiamos los valores para colocar el mayor en su posición
            lista[i], lista[indice_mayor] = lista[indice_mayor], lista[i]

        return lista

    @staticmethod
    def mergesort(lista):
        """
        Implementación de MergeSort utilizando recursividad.
        Divide la colección en sublistas más pequeñas hasta llegar a la unidad,
        para luego mezclarlas ordenadamente. Es ideal para manejar grandes datasets.
        """
        # Condición de parada para la recursividad
        if len(lista) <= 1:
            return lista

        # División del problema en dos mitades
        medio = len(lista) // 2
        izquierda = Ordenador.mergesort(lista[:medio])
        derecha = Ordenador.mergesort(lista[medio:])

        # Fase de conquista: mezclar las mitades ordenadas
        return Ordenador._mezclar(izquierda, derecha)

    @staticmethod
    def _mezclar(izquierda, derecha):
        """Método auxiliar encargado de fusionar dos listas pre-ordenadas."""
        resultado = []
        i = 0
        j = 0

        # Comparación elemento a elemento entre ambas listas
        while i < len(izquierda) and j < len(derecha):
            # Criterio de ordenamiento: Descendente (Mayor promedio primero)
            if izquierda[i].promedio >= derecha[j].promedio:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        # Concatenación de los elementos remanentes
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado


# ==========================================
# 3. ALGORITMOS DE BÚSQUEDA
# ==========================================

class Buscador:

    @staticmethod
    def secuencial(lista, id_buscado):
        """
        Búsqueda lineal estándar.
        Itera sobre cada elemento de la colección hasta encontrar la coincidencia.
        No requiere que los datos estén ordenados previamente.
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
        Búsqueda binaria optimizada.
        Reduce el espacio de búsqueda a la mitad en cada iteración.
        Requisito crítico: La lista debe estar ordenada por el campo de búsqueda (Matrícula).
        """
        izquierda = 0
        derecha = len(lista) - 1
        pasos = 0

        while izquierda <= derecha:
            pasos += 1
            medio = (izquierda + derecha) // 2
            est_medio = lista[medio]

            if est_medio.matricula == id_buscado:
                return est_medio, pasos
            elif est_medio.matricula < id_buscado:
                # El valor buscado está en la mitad superior
                izquierda = medio + 1
            else:
                # El valor buscado está en la mitad inferior
                derecha = medio - 1

        return None, pasos


# ==========================================
# 4. GENERACIÓN DE DATOS Y MEDICIÓN
# ==========================================

def generar_estudiantes(cantidad):
    """Genera un dataset de prueba con estudiantes y calificaciones aleatorias."""
    nombres = ["Ana", "Luis", "Pepe", "Maria", "Juan", "Sofia", "Carlos", "Fernanda", "Diego", "Lucia"]
    lista = []
    print(f"\nGenerando {cantidad} registros aleatorios...")
    for i in range(cantidad):
        # Se genera un ID secuencial con offset y un promedio flotante
        mat = 1000 + i
        nom = random.choice(nombres) + f"_{i}"
        prom = round(random.uniform(60.0, 100.0), 2)
        lista.append(Estudiante(mat, nom, prom))

    # Se mezcla la lista para simular datos sin procesar
    random.shuffle(lista)
    return lista


def medir_rendimiento(funcion, datos, **kwargs):
    """
    Wrapper para ejecución de algoritmos.
    Captura métricas de tiempo de ejecución (wall-clock) y consumo pico de memoria RAM.
    """
    tracemalloc.start()
    inicio_tiempo = time.time()

    funcion(datos, **kwargs)

    fin_tiempo = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tiempo_total = fin_tiempo - inicio_tiempo
    return tiempo_total, peak


# ==========================================
# 5. VALIDACIÓN Y BENCHMARKING
# ==========================================

class Validador:
    @staticmethod
    def prueba_correccion():
        """Verifica la integridad lógica de los algoritmos comparándolos contra métodos nativos."""
        print("\n--- EJECUTANDO PRUEBAS DE INTEGRIDAD ---")
        datos = generar_estudiantes(50)

        # Validación del módulo de Ordenamiento
        esperado = sorted(datos, key=lambda x: x.promedio, reverse=True)
        resultado = Ordenador.mergesort(datos)

        # Verificación de consistencia en el orden descendente
        es_descendente = all(resultado[i].promedio >= resultado[i + 1].promedio for i in range(len(resultado) - 1))

        if es_descendente:
            print("[Ordenamiento] La lógica de MergeSort es correcta.")
        else:
            print("[Ordenamiento] ERROR: La lista no se ordenó correctamente.")

        # Validación del módulo de Búsqueda
        objetivo = datos[25]  # Selección aleatoria de un objetivo

        # Prueba Secuencial
        res_lin, _ = Buscador.secuencial(datos, objetivo.matricula)
        if res_lin and res_lin.matricula == objetivo.matricula:
            print("[Búsqueda] Secuencial encontró el registro esperado.")
        else:
            print("[Búsqueda] Secuencial falló.")

        # Prueba Binaria (Pre-ordenamiento requerido)
        datos_ordenados_id = sorted(datos, key=lambda x: x.matricula)
        res_bin, _ = Buscador.binaria(datos_ordenados_id, objetivo.matricula)
        if res_bin and res_bin.matricula == objetivo.matricula:
            print("[Búsqueda] Binaria encontró el registro esperado.")
        else:
            print("[Búsqueda] Binaria falló.")

    @staticmethod
    def reporte_masivo():
        """Ejecuta un benchmark completo variando la carga de datos."""
        print("\n--- INICIANDO BENCHMARK DE RENDIMIENTO ---")
        cantidades = [100, 500, 1000, 2500, 5000]

        res_tiempo_sel, res_tiempo_mer = [], []
        res_tiempo_lin, res_tiempo_bin = [], []

        print(f"{'Cant.':<6} | {'MergeSort(s)':<12} | {'Selección(s)':<12} | {'Binaria(s)':<10} | {'Lineal(s)':<10}")
        print("-" * 65)

        for n in cantidades:
            # Silenciamos la salida del generador para el reporte masivo
            temp_lista = []
            nombres = ["Ana", "Luis", "Pepe", "Maria"]
            for i in range(n):
                mat = 1000 + i
                nom = random.choice(nombres)
                prom = round(random.uniform(60.0, 100.0), 2)
                temp_lista.append(Estudiante(mat, nom, prom))
            random.shuffle(temp_lista)
            datos = temp_lista

            # Benchmark Ordenamiento
            t_mer, _ = medir_rendimiento(Ordenador.mergesort, datos)

            # Omitimos Selección en cargas altas para evitar bloqueos por tiempo excesivo
            if n < 3000:
                t_sel, _ = medir_rendimiento(Ordenador.seleccion_directa, datos)
            else:
                t_sel = 0.0

                # Benchmark Búsqueda (Peor caso: elemento no existente o último)
            objetivo = datos[-1].matricula
            datos_ord_id = sorted(datos, key=lambda x: x.matricula)

            t_lin, _ = medir_rendimiento(Buscador.secuencial, datos, id_buscado=objetivo)
            t_bin, _ = medir_rendimiento(Buscador.binaria, datos_ord_id, id_buscado=objetivo)

            res_tiempo_mer.append(t_mer)
            res_tiempo_sel.append(t_sel)
            res_tiempo_lin.append(t_lin)
            res_tiempo_bin.append(t_bin)

            txt_sel = f"{t_sel:.5f}" if t_sel > 0 else "N/A"
            print(f"{n:<6} | {t_mer:.5f}      | {txt_sel:<12} | {t_bin:.6f}   | {t_lin:.6f}")

        Validador.graficar(cantidades, res_tiempo_sel, res_tiempo_mer, res_tiempo_lin, res_tiempo_bin)

    @staticmethod
    def graficar(x, y_sel, y_mer, y_lin, y_bin):
        """Genera y visualiza las gráficas de rendimiento comparativo."""

        plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif'})

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Análisis de Rendimiento del Sistema', fontsize=16, fontweight='bold', color='#333333')

        # Configuración Gráfica Ordenamiento
        x_sel = [x[i] for i in range(len(y_sel)) if y_sel[i] > 0]
        y_sel_fil = [v for v in y_sel if v > 0]

        ax1.plot(x_sel, y_sel_fil, color='#e74c3c', marker='o', linestyle='-', linewidth=2, label='Selección Directa')
        ax1.plot(x, y_mer, color='#2ecc71', marker='s', linestyle='-', linewidth=2, label='MergeSort')

        ax1.set_title("Tiempos de Ordenamiento", fontsize=12, fontweight='bold')
        ax1.set_xlabel("Cantidad de Registros")
        ax1.set_ylabel("Tiempo (segundos)")
        ax1.legend(loc="upper left")
        ax1.grid(True, linestyle='--', alpha=0.6)

        # Configuración Gráfica Búsqueda
        ax2.plot(x, y_lin, color='#f39c12', marker='^', linestyle='-', linewidth=2, label='Búsqueda Lineal')
        ax2.plot(x, y_bin, color='#3498db', marker='D', linestyle='-', linewidth=2, label='Búsqueda Binaria')

        ax2.set_title("Tiempos de Búsqueda", fontsize=12, fontweight='bold')
        ax2.set_xlabel("Cantidad de Registros")
        ax2.set_ylabel("Tiempo (segundos)")
        ax2.legend(loc="upper left")
        ax2.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        print("\nAbriendo ventana de gráficas...")
        plt.show()


# ==========================================
# 6. MENÚ E INTERFAZ DE USUARIO
# ==========================================

def solicitar_entero(mensaje):
    """Valida la entrada de datos numéricos del usuario."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número.")


def mostrar_encabezado():
    print("\n" + "=" * 50)
    print("      SISTEMA DE GESTIÓN DE BECAS UNIVERSITARIAS")
    print("=" * 50)


def menu():
    # Inicialización por defecto con 50 estudiantes (se puede cambiar luego)
    cantidad_actual = 50
    lista_actual = generar_estudiantes(cantidad_actual)

    while True:
        mostrar_encabezado()
        print(f"Estudiantes cargados actualmente: {len(lista_actual)}")
        print("-" * 50)
        print("1. [CONFIG] Generar nueva lista de estudiantes")
        print("2. [VISTA]  Ver lista actual (Primeros 10)")
        print("3. [ORDEN]  Ordenar Ranking por Promedio (MergeSort)")
        print("4. [BUSCAR] Buscar Estudiante por Matrícula")
        print("5. [TEST]   Ejecutar Diagnóstico de Rendimiento (Benchmark)")
        print("6. Salir")
        print("-" * 50)

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nueva_cantidad = solicitar_entero("\n¿Cuántos estudiantes desea generar? (Ej: 100, 5000): ")
            if nueva_cantidad > 0:
                lista_actual = generar_estudiantes(nueva_cantidad)
                print(f"✅ Se han generado {nueva_cantidad} nuevos registros.")
            else:
                print("❌ La cantidad debe ser mayor a 0.")

        elif opcion == '2':
            print(f"\n--- VISTA PREVIA ({len(lista_actual)} registros) ---")
            # Limitamos la visualización a los primeros 10 registros
            for e in lista_actual[:10]: print(e)
            if len(lista_actual) > 10:
                print(f"... y {len(lista_actual) - 10} registros más ocultos.")

        elif opcion == '3':
            print("\n>>> Procesando ordenamiento...")
            inicio = time.time()
            lista_actual = Ordenador.mergesort(lista_actual)
            fin = time.time()
            print(f"✅ Lista ordenada en {fin - inicio:.6f} segundos.")
            print("--- TOP 5 MEJORES PROMEDIOS ---")
            for i, e in enumerate(lista_actual[:5]): print(f"#{i + 1} {e}")

        elif opcion == '4':
            id_buscado = solicitar_entero("\nIngrese Matrícula a buscar: ")

            # Medición en tiempo real
            t0 = time.time()
            res_lin, pasos_lin = Buscador.secuencial(lista_actual, id_buscado)
            t1 = time.time()

            # Ordenamiento temporal requerido para búsqueda binaria
            # (Nota: Si ya ordenaste con la opción 3, esto podría ser redundante,
            # pero lo mantenemos para asegurar que Binaria funcione siempre)
            lista_id = sorted(lista_actual, key=lambda x: x.matricula)
            t2 = time.time()
            res_bin, pasos_bin = Buscador.binaria(lista_id, id_buscado)
            t3 = time.time()

            if res_bin:
                print(f"\n✅ Registro encontrado: {res_bin}")
                print("-" * 40)
                print(f"MÉTODO      | TIEMPO (s)   | PASOS")
                print("-" * 40)
                print(f"Lineal      | {t1 - t0:.6f}     | {pasos_lin}")
                print(f"Binaria     | {t3 - t2:.6f}     | {pasos_bin}")
                print("-" * 40)
            else:
                print("\n❌ Estudiante no encontrado en la base de datos.")

        elif opcion == '5':
            # Ejecución de pruebas automáticas
            Validador.prueba_correccion()
            Validador.reporte_masivo()

        elif opcion == '6':
            print("\nCerrando sesión... ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no reconocida, intente de nuevo.")


if __name__ == "__main__":
    menu()