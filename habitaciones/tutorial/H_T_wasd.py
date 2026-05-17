
from habitaciones.H_base import Habitacion, Obstaculo,Gema
from habitaciones.H_colManager import ManejoColisiones
from entidades import Proyectil
from escenas.UT_guardado import cargarConfig
import pygame

class HabitacionWasd(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json
        
    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        self.Proyectiles.update(dt)
        configuracion = cargarConfig()
        teclas = configuracion["teclas"]
        if (keys[teclas["arriba"]] or keys[pygame.K_UP]) and len(self.datos["TeclasOprimidas"][0]) == 0 :
            self.datos["TeclasOprimidas"][0].append(1)
        if (keys[teclas["abajo"]] or keys[pygame.K_DOWN])and len(self.datos["TeclasOprimidas"][1]) == 0:
            self.datos["TeclasOprimidas"][1].append(1)
        if (keys[teclas["derecha"]] or keys[pygame.K_RIGHT])and len(self.datos["TeclasOprimidas"][2]) == 0 :
            self.datos["TeclasOprimidas"][2].append(1)
        if (keys[teclas["izquierda"]] or keys[pygame.K_LEFT])and len(self.datos["TeclasOprimidas"][3]) == 0 :
            self.datos["TeclasOprimidas"][3].append(1)
        
        if (self.datos["TeclasOprimidas"][0] == [1] )and (self.datos["TeclasOprimidas"][1] == [1] ) and (self.datos["TeclasOprimidas"][2] == [1] ) and (self.datos["TeclasOprimidas"][3] == [1] ):
            self.conexiones["abajo"] = 2
        #Para el miniBoss

    def draw(self, screen):
        self.Proyectiles.draw(screen)

        

    
