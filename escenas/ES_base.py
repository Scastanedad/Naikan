import pygame

#Clase base para todas las escenas
class EscenaBase ():
    WIDTH = 800
    HEIGTH = 600
    def __init__(self):    
        self.fuente = pygame.font.Font(None, 28)
    def HandleEvents (self, events):
        return self
    def Update(self,dt,keys):
        return self
    def draw(self,screen):
        return self