import pygame
import math

#Clase abstracta para todas las entidades





#Como agregamos diseño de nivel, ya la generacion no sera aleatoria, entonces el obstaculo no requiere saber donde esta el jugador
class Obstaculo:
    def __init__(self, x, y ):
        self.x = x
        self.y = y
        self.width = 10
        self.heigth = 10
        self.rect = pygame.Rect(self.x,self.y,self.width, self.heigth)
        
    
    def draw(self, screen):
        pygame.draw.rect(screen,(0,0,255), (self.x,self.y, self.width, self.heigth))

        


        
