
from escenas.ES_base import EscenaBase
import os,json,pygame
from habitaciones import HabitacionEnemigos, HabitacionCura
from entidades import Jugador, Proyectil
from escenas.CO_victoria import MatarTodosEnemigos
def CargarNivel(NumeroNivel, MundoActual = 1):
    base = os.path.dirname(__file__)
    ruta = os.path.join(base,"..","mundos",f"mundo{MundoActual}","niveles", f"nivel{NumeroNivel}.json")
    with open(ruta,"r") as archivo:
        raw = json.load(archivo)
    return {
        "habitacion_inicial":raw["habitacion_inicial"],
        "c_hab":raw["cantidad_hab"],
        #Cargamos las caracteristicas de las habitaciones en un diccionario que tiene como clave el id
        "habitaciones":{h["id"]:h for h in raw["habitaciones"]}
    }


def ManejoHabitaciones(TipoHab,DatosHabitacion):
    match TipoHab:
        case "HabitacionEnemigo":
            return HabitacionEnemigos(DatosHabitacion)
        case "HabitacionCura":
            return HabitacionCura(DatosHabitacion)
        case _:
            return print("Tipo de habitacion no valida")

class EscenaJuego(EscenaBase):
    def __init__(self, numeroNivel = 1, habitacion_id = None, vida =3,  x= None ,y= None, currentData = None ) :
        self.nivel = currentData if currentData else CargarNivel(numeroNivel)
        
        habitacion_ACT = habitacion_id if habitacion_id else self.nivel["habitacion_inicial"]
        self.habitacion = ManejoHabitaciones(self.nivel["habitaciones"][habitacion_ACT]["tipoHab"],self.nivel["habitaciones"][habitacion_ACT]) 
        self.numeroNivel = numeroNivel
        if x is not None and y is not None:
            self.Jugador1 = Jugador(x,y)
        else:
            self.Jugador1 = Jugador(self.WIDTH//2,self.HEIGTH//2)
        self.Jugador1.vida = vida
        
    
    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x: 
                    self.habitacion.Proyectiles.append(Proyectil(self.Jugador1.x, self.Jugador1.y, self.Jugador1.direccion)) # type: ignore
                if event.key == pygame.K_RETURN:
                    from escenas.ES_estaticas import  MainMenu
                    return MainMenu()
        return self
    
    def Update(self, dt, keys):
        self.Jugador1.mover(dt,keys,self.WIDTH,self.HEIGTH)
        self.habitacion.update(dt,keys,self.Jugador1, self.WIDTH, self.HEIGTH)      # type: ignore
        if MatarTodosEnemigos(self.nivel):
            from escenas.ES_estaticas import EndGame
            return EndGame()
        conexiones = self.habitacion.conexiones # type: ignore
        if self.Jugador1.y <= 0 and conexiones["arriba"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x <420):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            return EscenaJuego(self.numeroNivel,conexiones["arriba"],self.Jugador1.vida, self.Jugador1.x, self.HEIGTH- 30, self.nivel)
        if self.Jugador1.y >= (self.HEIGTH -20)and conexiones["abajo"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x <420):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            return EscenaJuego(self.numeroNivel, conexiones["abajo"],self.Jugador1.vida, self.Jugador1.x, 30,self.nivel)
        if self.Jugador1.x <= 0 and conexiones["izquierda"] is not None and (self.Jugador1.y >280 and self.Jugador1.y < 320):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            return EscenaJuego(self.numeroNivel, conexiones["izquierda"],self.Jugador1.vida, self.WIDTH - 30, self.Jugador1.y,self.nivel)
        if self.Jugador1.x >= (self.WIDTH-20) and conexiones["derecha"] is not None and (self.Jugador1.y >280 and self.Jugador1.y < 320):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            return EscenaJuego(self.numeroNivel, conexiones["derecha"],self.Jugador1.vida, 30, self.Jugador1.y,self.nivel)
        if self.Jugador1.vida == 0:
            from escenas.ES_estaticas import EndGame
            return EndGame()
        
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        
        self.habitacion.draw(screen) # type: ignore
        for i in range(self.Jugador1.vida):
            pygame.draw.rect(screen,(255,0,0),(0+10*i, 10, 5,5))
        self.Jugador1.draw(screen)
