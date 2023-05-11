from collections import defaultdict

# Guarda la información de cada actividad
# Subtema al que pertenece, tiempo que dura, su valor o calificación,
# booleano que indica si es obligatoria, sus requisitos, y las actividades que la requieren
class Actividad:
    __slots__ = ("num_act", "subtema", "tiempo", "valor", "obligatoria", "requiere", "requerido_por")
    def __init__(self, num_act: int, subtema: int=None, tiempo: float=None, valor: float=None, obligatorio: bool=None, requiere: set[int]=None) -> None:
        self.num_act: int = num_act        
        self.subtema: int = subtema    # Subtema al que pertenece la actividad
        self.tiempo: float = tiempo         # Tiempo que toma la actividad
        self.valor: float = valor           # Valor que contribuye la actividad
        self.obligatoria: bool = obligatorio  # True si es obligatoria, False si no
        self.requiere: set[int] = requiere  # Set con los numeros de actividad de las que depende la actividada actual
        self.requerido_por: set[int] = set()

    def __str__(self) -> str:
        return f"subtema: {self.subtema: 2}, tiempo: {self.tiempo: >4}, valor: {self.valor: >4}, oblig: {self.obligatoria: 3}, reqs: {self.requiere}, req_por: {self.requerido_por}"

# Guarda los numeros de las actividades de cada subtema
# y la calificación mímima restante
class DatosSubtema:
    __slots__ = ("nums_actividades", "calif_min")
    
    def __init__(self, calif_min) -> None:
        self.nums_actividades: set[int] = set()
        self.calif_min: float = calif_min

# Guarda todas las actividades en .actividades, dado su numero de actividad me da sus datos
# Guarda los datos de cada subtema en .subtemas, dado su numero de subtema me da sus datos
# Guarda la calificación mínima por subtema en kmin (solo es necesaria para la creación)
class Instancia_Pl_Ed:
    __slots__ = ("actividades", "subtemas", "kmin")
    
    def __init__(self, kmin: float) -> None:
        self.kmin = kmin
        self.actividades: dict[int, Actividad] = {}
        self.subtemas: dict[int, DatosSubtema] = {}

    def add_actividad(self, actividad: Actividad):
        num = actividad.num_act
        
        # Agrega los datos de la actividad
        if num in self.actividades:
            actividad.requerido_por = self.actividades[num].requerido_por
        self.actividades[num] = actividad

        # Crea subtema de la actividad si no existe
        if actividad.subtema not in self.subtemas:
            self.subtemas[actividad.subtema] = DatosSubtema(self.kmin)
        
        # Agrega la actividad al subtema
        self.subtemas[actividad.subtema].nums_actividades.add(num)

        # Crea arbol de dependencias en sentido opuesto
        for act_requerida in actividad.requiere:
            if act_requerida not in self.actividades:
                self.actividades[act_requerida] = Actividad(act_requerida)
            self.actividades[act_requerida].requerido_por.add(num)
                
    def __str__(self) -> str:
        retorno = ""
        for subtema in sorted(self.subtemas.keys()):
            for num_actividad in sorted(self.subtemas[subtema].nums_actividades):
                retorno += f"Act {num_actividad:2}: {self.actividades[num_actividad]}\n"
        return retorno

# Crea una instancia del problema dado el nombre de un archivo
# y una calificación mínima kmin para todos los subtemas
def get_problema(nombre_archivo: str, kmin: float) -> Instancia_Pl_Ed:
    with open(f"{nombre_archivo}") as archivo:
        instancia = Instancia_Pl_Ed(kmin)
        
        for linea in archivo.readlines():
            datos_activ = list(map(float, linea.split(',')))
            
            num_activ = int(datos_activ[3])
            subtema = int(datos_activ[2])
            tiempo = float(datos_activ[4])
            valor = float(datos_activ[5])
            obligatorio = bool(datos_activ[9])
            reqs = { int(datos_activ[i]) for i in (7,8) if int(datos_activ[i]) != 0}
            
            nueva_act = Actividad(num_activ, subtema , tiempo, valor, obligatorio, reqs)
            instancia.add_actividad(nueva_act)
        return instancia

if __name__ == "__main__":
    # E J E M P L O   D E   C R E A C I Ó N   D E   I N S T A N C I A
    # Primero paso el nombre del archivo y la calificación mínima por subtema
    # La función me crea la instancia de tipo Instancia_Pl_Ed
    inst = get_problema("instancias/f_5_2.csv", 70)
    # podemos ver la instancia así:
    print(inst)