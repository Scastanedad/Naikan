import pygame

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

class Obstaculo:
    def __init__(self, x, y ):
        self.x = x
        self.y = y
        self.width = 10
        self.heigth = 10
        self.rect = pygame.Rect(self.x,self.y,self.width, self.heigth)
        
    
    def draw(self, screen):
        pygame.draw.rect(screen,(0,0,255), (self.x,self.y, self.width, self.heigth))