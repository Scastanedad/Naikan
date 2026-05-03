from entidades.ET_general import Entidad
import pygame
#Clase base para todos los enemigos, que parte de la clase base Entidad
class Enemigos(Entidad):
    def __init__(self, x, y, vida, velocidad, width, heigth,color):
        super().__init__(x, y, vida, velocidad, width, heigth,color)
    
    def update(self,dt, obstaculos, jugador):
        pass

    def recibirDaño(self,Danio):
        self.vida -= 1

    def actualizarRect(self):
        self.rect.center = (self.x, self.y)