from habitaciones.H_base import Habitacion, Obstaculo,Gema
from habitaciones.H_colManager import ManejoColisiones
from entidades import EnemigoDistancia, EnemigoMelee,Proyectil
import pygame,random

class HabitacionSobrevivir(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json
        self.obstaculos = pygame.sprite.Group(*[Obstaculo(x,y,datos["obstaculos"]) for x,y in datos["obstaculos"]]) # type: ignore
        self.enemigosM = pygame.sprite.Group(*[EnemigoMelee(x,y,[x,y],datos["enemigosM"]) for x,y in datos["enemigosM"]]) # type: ignore
        self.enemigosD = pygame.sprite.Group(*[EnemigoDistancia(x,y,[x,y],datos["enemigosD"]) for x,y in datos["enemigosD"]]) # type: ignore
        self.timer = 0 
        self.timer_melee = 0
        self.timer_distancia = 0

    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        self.timer += dt
        # En update:
        self.timer_melee += dt
        self.timer_distancia += dt

        if self.timer_melee >= 3.0:  
            x = random.randint(100, 700)
            y = random.randint(200, 500)
            self.enemigosM.add(EnemigoMelee(x, y))
            self.timer_melee = 0  
        if self.timer_distancia >= 2.0:  
            x = random.randint(100, 700)
            y = random.randint(200, 500)
            self.enemigosD.add(EnemigoDistancia(x, y)) 
            self.timer_distancia = 0
        ManejoColisiones(self,Jugador1)
        self.enemigosM.update(dt,Jugador1.sprite)
        for e in self.enemigosD:
            proyectil = e.update(dt, Jugador1.sprite)
            if proyectil:
                self.Proyectiles.add(proyectil)
        self.Proyectiles.update(dt)

        #Para el miniBoss

    def draw(self, screen):
        self.Proyectiles.draw(screen)
        self.obstaculos.draw(screen)
        self.enemigosM.draw(screen)
        self.enemigosD.draw(screen)


        
