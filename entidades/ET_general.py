import pygame

class Entidad:
    def __init__(self, x, y, vida, velocidad, width, heigth):
        self.x = x
        self.y = y
        self.vida = vida
        self.velocidad = velocidad
        self.width = width
        self.heigth = heigth
        self.rect = pygame.Rect(self.x,self.y,self.width,self.heigth)
    
    def recibirDaño(self,Daño):
        self.vida -= Daño

    def update(self,dt,keys,width, height):
        pass

    def actualizarRect(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Proyectil:
  
    def __init__(self, x ,y,direccion):
        self.x = x
        self.y = y
        self.velocidad = 600
        self.direccion = direccion
        self.width = 5
        self.height = 5
        self.rect = pygame.Rect(self.x,self.y,self.width, self.height)

    def update (self,dt):
        self.x += dt * self.velocidad*self.direccion[0]
        self.y += dt *self.velocidad*self.direccion[1]
        self.rect.x = self.x
        self.rect.y = self.y
    def draw(self,screen):
        pygame.draw.rect(screen, (255,0,0), (self.x,self.y, self.width, self.height))   