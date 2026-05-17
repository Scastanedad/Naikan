from habitaciones.H_base import Habitacion, Obstaculo,Gema
from habitaciones.H_colManager import ManejoColisiones
from entidades import Proyectil
from escenas.UT_guardado import cargarConfig
import pygame


class HabitacionMecanicas(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json

        
    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        self.Proyectiles.update(dt)
        configuracion = cargarConfig()
        teclas = configuracion["teclas"]
        if (keys[pygame.K_c])and len(self.datos["TeclasOprimidas"][0]) == 0:
            self.datos["TeclasOprimidas"][0].append(1)
        if (keys[pygame.K_x])and len(self.datos["TeclasOprimidas"][1]) == 0:
            self.datos["TeclasOprimidas"][1].append(1)
        
        

        if (self.datos["TeclasOprimidas"][0] == [1] )and (self.datos["TeclasOprimidas"][1] == [1] ):
            self.conexiones["derecha"] = 3
        #Para el miniBoss

    def draw(self, screen):
        self.Proyectiles.draw(screen)