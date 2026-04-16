import pygame

#Clase base para todas las escenas
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
