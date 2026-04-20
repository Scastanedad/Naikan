
from escenas.ES_base import EscenaBase
import os,json,pygame
from habitaciones import HabitacionEnemigos, HabitacionCura # type: ignore
from entidades import Jugador, Proyectil
from escenas.CO_victoria import MatarTodosEnemigos, MiniBoss
from escenas.UT_guardado import completarNivel
#Esta clase es la que trae el json a un diccionario de python
#El que carga el nivel es el hub
def CargarNivel(NumeroNivel, MundoActual = 1):
    base = os.path.dirname(__file__)
    ruta = os.path.join(base,"..","mundos",f"mundo{MundoActual}","niveles", f"nivel{NumeroNivel}.json")
    with open(ruta,"r") as archivo:
        raw = json.load(archivo)
    return {
        "mundo":raw["mundo"],
        "habitacion_inicial":raw["habitacion_inicial"],
        "cond_victoria":raw["cond_victoria"],
        "c_hab":raw["cantidad_hab"],
        #Cargamos las caracteristicas de las habitaciones en un diccionario que tiene como clave el id
        "habitaciones":{h["id"]:h for h in raw["habitaciones"]}
    }


#Con esta clase definimos que tipo de habitacion vamos a retornar
def ManejoHabitaciones(TipoHab,DatosHabitacion):
    match TipoHab:
        case "HabitacionEnemigo":
            return HabitacionEnemigos(DatosHabitacion)
        case "HabitacionCura":
            return HabitacionCura(DatosHabitacion)
        case _:
            return print("Tipo de habitacion no valida")

#Que condicion de victoria vamos a utilizar
def ManejoCondicionVictoria(DatosNivel):
    cond_v = DatosNivel["cond_victoria"]
    match cond_v:
        case "MatarTodos":
            return MatarTodosEnemigos(DatosNivel)
        case "MiniBoss":
            return MiniBoss(DatosNivel)

#Es la escena que renderiza las habitaciones
class EscenaJuego(EscenaBase):
    def __init__(self, numeroNivel = 1,mundoActual =1, habitacion_id = None, vida =3,  x= None ,y= None, currentData = None ) :
        #Si el nivel esta en progreso, se carga el diccionario modificado, si es la primera vez se accede al diccionario del json
        self.mundoActual = mundoActual   # <- NUEVO
        self.numeroNivel = numeroNivel 
        self.nivel = currentData if currentData else CargarNivel(numeroNivel)
        #Si es un nivel con miniBoss
        if self.nivel["cond_victoria"] == "MiniBoss" and "miniboss_spawned" not in self.nivel:
            self.nivel["miniboss_spawned"] = False
            self.nivel["miniboss_muerto"] = False
        
        #Dependiendo de si esta en progreso o no se accede a determinada habitacion
        habitacion_ACT = habitacion_id if habitacion_id else self.nivel["habitacion_inicial"]
        self.habitacion = ManejoHabitaciones(self.nivel["habitaciones"][habitacion_ACT]["tipoHab"],self.nivel["habitaciones"][habitacion_ACT]) 
        self.numeroNivel = numeroNivel
        #Para que las transciciones entre habitaciones tengan logica dimensional( Si bajo aparezco en la parte de arriba y asi)
        if x is not None and y is not None:
            self.Jugador1 = Jugador(x,y)
        else:
            self.Jugador1 = Jugador(self.WIDTH//2,self.HEIGTH//2)
        self.Jugador1.vida = vida
        self.grupoJugador = pygame.sprite.GroupSingle(self.Jugador1) # type: ignore
        
        
    
    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                #Disparar proyectiles
                if event.key == pygame.K_x: 
                    self.habitacion.Proyectiles.add(Proyectil(self.Jugador1.x + self.Jugador1.direccion[0]*30, self.Jugador1.y + self.Jugador1.direccion[1]*30, self.Jugador1.direccion)) # type: ignore
                #Logica donde se deberia acceder al menu de pausa
                if event.key == pygame.K_RETURN:
                    from escenas.ES_estaticas import  MainMenu
                    return MainMenu()
        return self
    
    def Update(self, dt, keys):
        
        self.grupoJugador.update(dt,keys,self.WIDTH,self.HEIGTH)
        self.habitacion.update(dt,keys,self.grupoJugador, self.WIDTH, self.HEIGTH)      # type: ignore
        if(self.nivel["cond_victoria"] != "MiniBoss"):
            if ManejoCondicionVictoria(self.nivel):
                completarNivel(self.mundoActual, self.numeroNivel)
                from escenas.ES_estaticas import EndGame
                return EndGame()
        else: 
            if(self.nivel["miniboss_spawned"] == False):
                if (ManejoCondicionVictoria(self.nivel) == "spawnear" )and (type(self.habitacion) != HabitacionCura):
                    self.nivel["miniboss_spawned"] = True
                    self.habitacion.conexiones = {"arriba":None,"abajo":None,"izquierda":None,"derecha":None} # type: ignore
                    self.habitacion.SpawnMiniBoss(self.nivel["mundo"]) # type: ignore
            if ((self.nivel["miniboss_spawned"] == True)and (len(self.habitacion.miniBoss)==0)): # type: ignore
                completarNivel(self.mundoActual, self.numeroNivel)
                from escenas.ES_estaticas import EndGame
                return EndGame()
                
                    

        #Manejo de conexiones entre habitaciones, en el diccionario se establece hacia donde puede ir, y si esta en la puerta para ir hasta alla, se accede y ya
        conexiones = self.habitacion.conexiones # type: ignore
        if self.Jugador1.y <= 0 and conexiones["arriba"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x < 420):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaJuego(self.numeroNivel, self.mundoActual, conexiones["arriba"], self.Jugador1.vida, self.Jugador1.x, self.HEIGTH - 30, self.nivel)  # <- mundoActual
        if self.Jugador1.y >= (self.HEIGTH - 20) and conexiones["abajo"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x < 420):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaJuego(self.numeroNivel, self.mundoActual, conexiones["abajo"], self.Jugador1.vida, self.Jugador1.x, 30, self.nivel)  # <- mundoActual
        if self.Jugador1.x <= 0 and conexiones["izquierda"] is not None and (self.Jugador1.y > 280 and self.Jugador1.y < 320):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaJuego(self.numeroNivel, self.mundoActual, conexiones["izquierda"], self.Jugador1.vida, self.WIDTH - 30, self.Jugador1.y, self.nivel)  # <- mundoActual
        if self.Jugador1.x >= (self.WIDTH - 20) and conexiones["derecha"] is not None and (self.Jugador1.y > 280 and self.Jugador1.y < 320):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaJuego(self.numeroNivel, self.mundoActual, conexiones["derecha"], self.Jugador1.vida, 30, self.Jugador1.y, self.nivel)  # <- mundoActual
        #Si se muere da pantalla final
        if self.Jugador1.vida == 0:
            from escenas.ES_estaticas import DeadScreen
            return DeadScreen()
        
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        self.habitacion.draw(screen) # type: ignore
        #Dependiendo de cuantas vidas tenga, se renderizan corazones rojos
        for i in range(self.Jugador1.vida):
            pygame.draw.rect(screen,(255,0,0),(0+10*i, 10, 5,5))
        self.grupoJugador.draw(screen)
