from clasesJ import Jugador, Proyectil
from clasesHab import HabitacionEnemigos
import pygame
import json
#Importamos os por que queremos interactuar con archivos
import os 
import sys

def CargarNivel(NumeroNivel):
    base = os.path.dirname(__file__)
    ruta = os.path.join(base, "niveles", f"nivel{NumeroNivel}.json")
    with open(ruta,"r") as archivo:
        raw = json.load(archivo)
    return {
        "habitacion_inicial":raw["habitacion_inicial"],
        #Cargamos las caracteristicas de las habitaciones en un diccionario que tiene como clave el id
        "habitaciones":{h["id"]:h for h in raw["habitaciones"]}
    }


def ManejoHabitaciones(TipoHab,DatosHabitacion):
    match TipoHab:
        case "HabitacionEnemigo":
            return HabitacionEnemigos(DatosHabitacion)
        case _:
            return print("Tipo de habitacion no valida")
    

class EscenaBase ():
    WIDTH = 800
    HEIGTH = 600
    def __init__(self):    
        self.fuente = pygame.font.Font(None, 28)
    def HandleEvents (self, events):
        pass
    def Update(self,dt,keys):
        pass
    def draw(self,screen):

        pass


class MainMenu(EscenaBase):
    def __init__(self):
        self.posFlecha = self.HEIGTH//2 - 190
        super().__init__()

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.posFlecha == self.HEIGTH//2 - 190: 
                        return EscenaJuego()
                    if self.posFlecha == self.HEIGTH//2 - 90:
                        return EscenaJuego()
                    if self.posFlecha == self.HEIGTH//2 +10:
                        pygame.quit()
                        sys.exit()

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if (self.posFlecha < self.HEIGTH//2 + 10):
                        self.posFlecha += 100
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.posFlecha > self.HEIGTH//2 - 190:
                        self.posFlecha -= 100

        return self
    #No necesariamente tiene que actualizarce nuestro menu
    def Update(self, dt, keys):
       
        return self
    def  draw(self, screen):
        #Menu principal
        screen.fill((0,0,0))
        texto = self.fuente.render("Iniciar Juego", True, (0,255,0))
        screen.blit(texto,(50,100))
        texto = self.fuente.render("Configuracion", True, (0,255,0))
        screen.blit(texto,(50,200))
        texto = self.fuente.render("Salir", True, (0,255,0))
        screen.blit(texto,(50,300))
        pygame.draw.rect(screen, ( 0,255,0), (200, self.posFlecha, 10, 2))


class EscenaJuego(EscenaBase):
    def __init__(self, numeroNivel = 1, habitacion_id = None, vida =3,  x= None ,y= None ) :
        self.nivel = CargarNivel(numeroNivel)
        inicio = habitacion_id if habitacion_id else self.nivel["habitacion_inicial"]
<<<<<<< HEAD
<<<<<<< Updated upstream
        self.habitacion = Habitacion(self.nivel["habitaciones"][inicio])
=======
        self.habitacion = ManejoHabitaciones(self.nivel["habitaciones"][inicio]["tipoHab"],self.nivel["habitaciones"][inicio]) 
>>>>>>> Stashed changes
=======
        self.habitacion = HabitacionEnemigos(self.nivel["habitaciones"][inicio])
>>>>>>> main
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
                    self.habitacion.Proyectiles.append(Proyectil(self.Jugador1.x, self.Jugador1.y, self.Jugador1.direccion))
                if event.key == pygame.K_RETURN:
                    return MainMenu()
        return self
    
    def Update(self, dt, keys):
        self.Jugador1.mover(dt,keys,self.WIDTH,self.HEIGTH)
        self.habitacion.update(dt,keys,self.Jugador1, self.WIDTH, self.HEIGTH)     
        
        conexiones = self.habitacion.conexiones
        if self.Jugador1.y <= 0 and conexiones["arriba"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x <420):
            return EscenaJuego(self.numeroNivel,conexiones["arriba"],self.Jugador1.vida, self.Jugador1.x, self.HEIGTH- 30)
        if self.Jugador1.y >= (self.HEIGTH -20)and conexiones["abajo"] is not None and (self.Jugador1.x > 380 and self.Jugador1.x <420):
            return EscenaJuego(self.numeroNivel, conexiones["abajo"],self.Jugador1.vida, self.Jugador1.x, 30)
        if self.Jugador1.x <= 0 and conexiones["izquierda"] is not None and (self.Jugador1.y >280 and self.Jugador1.y < 320):
            return EscenaJuego(self.numeroNivel, conexiones["izquierda"],self.Jugador1.vida, self.WIDTH - 30, self.Jugador1.y)
        if self.Jugador1.x >= (self.WIDTH-20) and conexiones["derecha"] is not None and (self.Jugador1.y >280 and self.Jugador1.y < 320):
            return EscenaJuego(self.numeroNivel, conexiones["derecha"],self.Jugador1.vida, 30, self.Jugador1.y)
        if self.Jugador1.vida == 0:
            return EndGame()
        
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        for i in range(self.Jugador1.vida):
            pygame.draw.rect(screen,(255,0,0),(0+10*i, 10, 5,5))
        self.habitacion.draw(screen)
        self.Jugador1.draw(screen)


class EndGame(EscenaBase):
    def __init__(self):
        super().__init__()
    
    def Update(self, dt, keys):
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return MainMenu()
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        texto = self.fuente.render("Dale al enter para volver al menu", True, (0,255,0))
        screen.blit(texto,(200,300))
    

class Configuracion(EscenaBase):
    def __init__(self):
        super().__init__()
    
    def draw(self, screen):
        return super().draw(screen)
    
    def Update(self, dt, keys):
        return super().Update(dt, keys)
    
    def HandleEvents(self, events):
        return super().HandleEvents(events)