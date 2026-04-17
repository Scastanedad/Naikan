import pygame
#Clase abstracta que es base para todas las habitaciones
class Habitacion():
    def __init__(self,datos):
        #Los datos proviene del diccionario que utilizamos en escenas dinamicas
        self.id = datos["id"]
        self.datos = datos 
        self.conexiones = datos["conexiones"]
        #Para renderizar los proyectiles los cargamos todos en una lista
        self.Proyectiles = pygame.sprite.Group()
        
    def update(self, dt, keys,Jugador1, WIDTH, HEIGTH):
        pass
    def draw(self, screen):
        pass

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y ):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 10
        self.heigth = 10
        #Sistema de colisiones para obstaculos
        self.image = pygame.Surface((self.width,self.heigth))
        self.rect = pygame.Rect(self.x,self.y,self.width, self.heigth)
        
    
    def draw(self, screen):
        pygame.draw.rect(screen,(0,0,255), (self.x,self.y, self.width, self.heigth))