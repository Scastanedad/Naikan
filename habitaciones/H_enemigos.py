from habitaciones.H_base import Habitacion, Obstaculo,Gema
from habitaciones.H_colManager import ManejoColisiones
from entidades import EnemigoDistancia, EnemigoMelee, MiniBoss1,Proyectil
import pygame

class HabitacionEnemigos(Habitacion):
    def __init__(self, datos,mundo):
        super().__init__(datos)
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json
        self.obstaculos = pygame.sprite.Group(*[Obstaculo(x,y,datos["obstaculos"]) for x,y in datos["obstaculos"]]) # type: ignore
        self.enemigosM = pygame.sprite.Group(*[EnemigoMelee(x,y,mundo,[x,y],datos["enemigosM"]) for x,y in datos["enemigosM"]]) # type: ignore
        self.enemigosD = pygame.sprite.Group(*[EnemigoDistancia(x,y,mundo,[x,y],datos["enemigosD"]) for x,y in datos["enemigosD"]]) # type: ignore
        self.miniBoss = pygame.sprite.Group()
    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        eventos =[]

        ManejoColisiones(self,Jugador1)
        self.enemigosM.update(dt,Jugador1.sprite)
        for e in self.enemigosD:
            proyectil = e.update(dt, Jugador1.sprite)
            if proyectil:
                self.Proyectiles.add(proyectil)
    
        for b in self.miniBoss:
            eventos = b.update(dt,Jugador1)          
        if eventos: 
            for e in eventos:
                if isinstance(e,Proyectil):
                    proyectil = e
                    if proyectil:
                        self.Proyectiles.add(proyectil)
                if isinstance(e,EnemigoMelee):
                    enemigo = e
                    if enemigo:
                        self.enemigosM.add(e)
        self.Proyectiles.update(dt)

        #Para el miniBoss

    def draw(self, screen):
        self.Proyectiles.draw(screen)
        self.obstaculos.draw(screen)
        self.enemigosM.draw(screen)
        self.enemigosD.draw(screen)
        for m in self.miniBoss:
            m.draw(screen)

    def SpawnMiniBoss(self,mundo):
        if ( mundo == 1):
            self.miniBoss.add(MiniBoss1(400,300,(400,300)))
        

    
