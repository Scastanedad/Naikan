from habitaciones.H_base import Habitacion, Obstaculo,Gema
from habitaciones.H_colManager import ManejoColisiones
from entidades import Proyectil
import pygame

class HabitacionGema(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json
        self.gema = pygame.sprite.Group(*[Gema(x,y) for x,y in datos["enemigosD"]]) # type: ignore
    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        ColJugadorGema(self, Jugador1)
        self.Proyectiles.update(dt)

        #Para el miniBoss

    def draw(self, screen):
        self.gema.draw(screen)

def ColJugadorGema(hab,Jugador1):
    colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , hab.gema, False) # type: ignore
    if colisiones:
        for gema in colisiones:
            hab.datos["obstaculos"] = gema.destruir()
            # type: ignore

        

    
