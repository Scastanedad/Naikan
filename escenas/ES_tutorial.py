
from escenas.ES_base import EscenaBase
import os,json,pygame
from habitaciones import HabitacionEnemigos, HabitacionWasd, HabitacionMecanicas # type: ignore
from entidades import Jugador, Proyectil
from escenas.CO_victoria import MatarTodosEnemigos, Tuto
from escenas.UT_guardado import completarNivel
from escenas.UT_guardado import cargarConfig
#Esta clase es la que trae el json a un diccionario de python
#El que carga el nivel es el hub
def CargarNivel(NumeroNivel, MundoActual ):
    base = os.path.dirname(__file__)
    ruta = os.path.join(base,"..","mundos","tutorial","tutorial.json")
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
def ManejoHabitaciones(TipoHab,DatosHabitacion,mundo):
    match TipoHab:
        case "HabitacionEnemigo":
            return HabitacionEnemigos(DatosHabitacion,mundo)
        case "HabitacionWasd":
            return HabitacionWasd(DatosHabitacion)
        case "HabitacionMecanicas":
            return HabitacionMecanicas(DatosHabitacion)
        case _:
            return print("Tipo de habitacion no valida")

#Que condicion de victoria vamos a utilizar
def ManejoCondicionVictoria(DatosNivel, t=None):
    cond_v = DatosNivel["cond_victoria"]
    match cond_v:
        case "MatarTodos":
            return MatarTodosEnemigos(DatosNivel)
        case "Tuto":
            return Tuto(DatosNivel)



class EscenaTutorial(EscenaBase):
    def __init__(self, numeroNivel = 1,mundoActual =1, habitacion_id = None, vida =3,  x= None ,y= None, currentData = None ) :
        #Si el nivel esta en progreso, se carga el diccionario modificado, si es la primera vez se accede al diccionario del json
        self.mundoActual = mundoActual   
        self.numeroNivel = numeroNivel 
        self.nivel = currentData if currentData else CargarNivel(numeroNivel,mundoActual)
        #Si es un nivel con miniBoss
        #Dependiendo de si esta en progreso o no se accede a determinada habitacion
        habitacion_ACT = habitacion_id if habitacion_id else self.nivel["habitacion_inicial"]
        self.habitacion = ManejoHabitaciones(self.nivel["habitaciones"][habitacion_ACT]["tipoHab"],self.nivel["habitaciones"][habitacion_ACT],self.mundoActual) 
        self.numeroNivel = numeroNivel
        
        from escenas.workModules.audio_manager import AudioManager
        ruta_musica = f"assets/musica/mundo{self.mundoActual}/habitacion_mundo{self.mundoActual}.ogg"
            
        AudioManager.reproducir_musica(ruta_musica)
        #Para que las transciciones entre habitaciones tengan logica dimensional( Si bajo aparezco en la parte de arriba y asi)
        if x is not None and y is not None:
            self.Jugador1 = Jugador(x,y)
        else:
            self.Jugador1 = Jugador(self.WIDTH//2,self.HEIGTH//2)
        self.Jugador1.vida = vida
        self.grupoJugador = pygame.sprite.GroupSingle(self.Jugador1) # type: ignore
        
    def HandleEvents(self, events):
        configuracion = cargarConfig()
        tecla_disparo = configuracion["teclas"]["disparo"]

        for event in events:
            if tecla_disparo == 430:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("bala")
                    self.habitacion.Proyectiles.add(Proyectil(self.Jugador1.x + self.Jugador1.direccion[0]*30, self.Jugador1.y + self.Jugador1.direccion[1]*30, self.Jugador1.direccion,600,1,(0,0,200),"jugador",self.Jugador1.sprite_bala)) # type: ignore
                    
            else:
                if event.type == pygame.KEYDOWN and event.key == tecla_disparo: 
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("bala")
                    self.habitacion.Proyectiles.add(Proyectil(self.Jugador1.x + self.Jugador1.direccion[0]*30, self.Jugador1.y + self.Jugador1.direccion[1]*30, self.Jugador1.direccion,600,1,(0,0,200),"jugador",self.Jugador1.sprite_bala)) # type: ignore

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #from escenas.ES_estaticas import MainMenu
                    from escenas.estaticas import Menu_Pausa
                    return Menu_Pausa(self) 
        return self
    
    def Update(self, dt, keys):
        
        self.grupoJugador.update(dt,keys,self.WIDTH,self.HEIGTH)
        self.habitacion.update(dt,keys,self.grupoJugador, self.WIDTH, self.HEIGTH)      # type: ignore
        match self.nivel["cond_victoria"]:
            case "MatarTodos":
                if ManejoCondicionVictoria(self.nivel):
                    completarNivel(self.mundoActual, self.numeroNivel)
                    from escenas.estaticas import EndGame
                    return EndGame(self.numeroNivel, self.mundoActual)
            case _:
                if ManejoCondicionVictoria(self.nivel):
                    completarNivel(self.mundoActual, self.numeroNivel)
                    from escenas.estaticas import EndGame
                    return EndGame(self.numeroNivel, self.mundoActual)
                
                    

        #Manejo de conexiones entre habitaciones, en el diccionario se establece hacia donde puede ir, y si esta en la puerta para ir hasta alla, se accede y ya
        conexiones = self.habitacion.conexiones # type: ignore
        if self.Jugador1.y <= 40 and conexiones["arriba"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x < 420):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaTutorial(self.numeroNivel, self.mundoActual, conexiones["arriba"], self.Jugador1.vida, self.Jugador1.x, self.HEIGTH -50, self.nivel)  # <- mundoActual
        if self.Jugador1.y >= (self.HEIGTH - 40) and conexiones["abajo"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x < 420):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaTutorial(self.numeroNivel, self.mundoActual, conexiones["abajo"], self.Jugador1.vida, self.Jugador1.x, 50, self.nivel)  # <- mundoActual
        if self.Jugador1.x <= 40 and conexiones["izquierda"] is not None and (self.Jugador1.y > 280 and self.Jugador1.y < 320):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaTutorial(self.numeroNivel, self.mundoActual, conexiones["izquierda"], self.Jugador1.vida, self.WIDTH - 50, self.Jugador1.y, self.nivel)  # <- mundoActual
        if self.Jugador1.x >= (self.WIDTH - 40) and conexiones["derecha"] is not None and (self.Jugador1.y > 280 and self.Jugador1.y < 320):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos # type: ignore
            return EscenaTutorial(self.numeroNivel, self.mundoActual, conexiones["derecha"], self.Jugador1.vida, 50, self.Jugador1.y, self.nivel)  # <- mundoActual
        #Si se muere da pantalla final
        if self.Jugador1.vida == 0:
            from escenas.estaticas import DeadScreen
            return DeadScreen(self.numeroNivel, self.mundoActual)
        
        return self
    
    def draw(self, screen):
        screen.fill((255,255,255))
        color_vida = (255, 0, 0)
        
        from escenas.workModules.filtros import Filtros
        filtro_actual = Filtros.filtro_actual
        
        if filtro_actual != "ninguno" and filtro_actual in Filtros.MATRICES:
            super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
            super_temp.fill(color_vida)
            super_filtrada = Filtros.aplicar_filtro(super_temp, filtro_actual)
            color_vida = super_filtrada.get_at((0, 0))  # type: ignore
        
        #Dependiendo de cuantas vidas tenga, se renderizan corazones rojos
        self.habitacion.draw(screen) # type: ignore
        self.grupoJugador.draw(screen)
        for i in range(self.Jugador1.vida):
            pygame.draw.rect(screen, color_vida, (0+10*i, 10, 5, 5))
