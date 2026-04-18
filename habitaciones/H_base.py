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
    def __init__(self, x, y, listaO):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 10
        self.heigth = 10
        self.pos = [x,y]
        self.listaO = listaO
        #Sistema de colisiones para obstaculos
        self.image = pygame.Surface((self.width,self.heigth))
        self.image.fill((0,200,0))
        self.rect = pygame.Rect(self.x,self.y,self.width, self.heigth)
    
    def destruir(self):
        if self.pos in self.listaO:
            self.listaO.remove(self.pos)
        self.kill()    
        return self.listaO
