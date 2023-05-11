import random
from Inf_Instancia import Instancia_Pl_Ed, Actividad, DatosSubtema

class BusquedaTabu:
    def __init__(self, instancia: Instancia_Pl_Ed, iteraciones: int, tamaño_tabu: int):
        self.instancia = instancia
        self.iteraciones = iteraciones
        self.tamaño_tabu = tamaño_tabu

    def generar_solucion_inicial(self):
        solucion = []
        for subtema, datos_subtema in self.instancia.subtemas.items():
            actividades_subtema = list(datos_subtema.nums_actividades)
            random.shuffle(actividades_subtema)
            solucion.extend(actividades_subtema[:])
        return solucion

    def evaluar_solucion(self, solucion):
        calificaciones = {subtema: 0 for subtema in self.instancia.subtemas.keys()}
        tiempo_total = 0

        for num_actividad in solucion:
            actividad = self.instancia.actividades[num_actividad]
            subtema = actividad.subtema
            calificaciones[subtema] += actividad.valor
            tiempo_total += actividad.tiempo

        penalizacion = sum(1 for calif in calificaciones.values() if calif < self.instancia.kmin)
        return tiempo_total + penalizacion * 1000

    def vecindario(self, solucion):
        vecinos = []
        for i in range(len(solucion)):
            for j in range(i+1, len(solucion)):
                nuevo_vecino = solucion.copy()
                nuevo_vecino[i], nuevo_vecino[j] = nuevo_vecino[j], nuevo_vecino[i]
                if self.es_factible(nuevo_vecino):
                    vecinos.append(nuevo_vecino)
        return vecinos

    def es_factible(self, solucion):
        actividades_realizadas = set()
        for num_actividad in solucion:
            actividad = self.instancia.actividades[num_actividad]
            if not actividades_realizadas.issuperset(actividad.requiere):
                return False
            actividades_realizadas.add(num_actividad)
        return True

    def buscar_mejor_vecino(self, solucion, tabu_list):
        mejor_vecino = None
        mejor_evaluacion = float('inf')
        for vecino in self.vecindario(solucion):
            if vecino not in tabu_list:
                evaluacion_vecino = self.evaluar_solucion(vecino)
                if evaluacion_vecino < mejor_evaluacion:
                    mejor_vecino = vecino
                    mejor_evaluacion = evaluacion_vecino
        return mejor_vecino

    def ejecutar(self):
        solucion_actual = self.generar_solucion_inicial()
        mejor_solucion = solucion_actual
        mejor_evaluacion = self.evaluar_solucion(solucion_actual)
        tabu_list = []

        for _ in range(self.iteraciones):
            vecino = self.buscar_mejor_vecino(solucion_actual, tabu_list)
            if vecino is not None:
                evaluacion_vecino = self.evaluar_solucion(vecino)
                if evaluacion_vecino < mejor_evaluacion:
                    mejor_solucion = vecino
                    mejor_evaluacion = evaluacion_vecino

                solucion_actual = vecino
                tabu_list.append(solucion_actual)
                if len(tabu_list) > self.tamaño_tabu:
                    tabu_list.pop(0)

        return mejor_solucion, mejor_evaluacion

if __name__ == "__main__":
    instancia = Instancia_Pl_Ed("instancias/f_5_2.csv", 70)
    busqueda_tabu = BusquedaTabu(instancia, iteraciones=1000, tamaño_tabu=10)
    mejor_solucion, mejor_evaluacion = busqueda_tabu.ejecutar()

    print("Mejor solución encontrada:", mejor_solucion)
    print("Mejor evaluación:", mejor_evaluacion)

