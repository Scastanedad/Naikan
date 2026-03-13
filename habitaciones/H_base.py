import pygame

class Habitacion():
    def __init__(self,datos):
        self.id = datos["id"]
        self.conexiones = datos["conexiones"]
        self.Proyectiles = []
        
    def update(self, dt, keys,Jugador1, WIDTH, HEIGTH):
        pass
    def draw(self, screen):
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