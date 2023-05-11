from Inf_Instancia import get_problema
from alg_metaheuristica import BusquedaTabu

archivos = [
    "f_1_0.csv", "f_1_1.csv", "f_1_2.csv", "f_2_0.csv", "f_2_1.csv", "f_2_2.csv",
    "f_3_0.csv", "f_3_1.csv", "f_3_2.csv", "f_4_0.csv", "f_4_1.csv", "f_4_2.csv",
    "f_5_0.csv", "f_5_1.csv", "f_5_2.csv", "i_1_0.csv", "i_1_1.csv", "i_1_2.csv",
    "i_2_0.csv", "i_2_1.csv", "i_2_2.csv", "i_3_0.csv", "i_3_1.csv", "i_3_2.csv",
    "i_4_0.csv", "i_4_1.csv", "i_4_2.csv", "i_5_0.csv", "i_5_1.csv", "i_5_2.csv"
]

carpetaInstancias = "./instancias"

def probar_instancia(nombre_archivo, kmin=70, iteraciones=50, tamaño_tabu=10):
    archivo_a_leer = f"{carpetaInstancias}/{nombre_archivo}"
    instancia = get_problema(archivo_a_leer, kmin)
    busqueda_tabu = BusquedaTabu(instancia, iteraciones=iteraciones, tamaño_tabu=tamaño_tabu)
    mejor_solucion, mejor_evaluacion = busqueda_tabu.ejecutar()

    print(f"Archivo: {nombre_archivo}")
    print("Mejor solución encontrada:", mejor_solucion)
    print("Mejor evaluación:", mejor_evaluacion)
    print()

if __name__ == "__main__":
    for archivo in archivos:
        probar_instancia(archivo)

