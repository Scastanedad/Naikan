import pygame,math
#Clase base para todas las entidades
class Entidad(pygame.sprite.Sprite):
    def __init__(self, x, y, vida, velocidad, width, heigth,color):
        super().__init__()
        self.x = x
        self.y = y
        self.vida = vida
        self.velocidad = velocidad
        self.width = width
        self.height = heigth
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill((color))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        #self.rect.center=((self.x,self.y))
    
    def recibirDaño(self,Daño):
        self.vida -= Daño

    def update(self,dt,keys,width, height):
        pass

    def actualizarRect(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Proyectil(pygame.sprite.Sprite):
  
    def __init__(self, x ,y,direccion, velocidad = 600, modo = 1, color = (0,0,200)):
        super().__init__()
        self.x = x
        self.y = y
        self.modo = modo
        self.velocidad = velocidad
        self.direccion = direccion
        self.width = 5
        self.height = 5
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill((color))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.t = 0

    def update (self,dt):
        self.t += dt
        match self.modo:
            case 1:
                self.x += dt * self.velocidad*self.direccion[0]
                self.y += dt *self.velocidad*self.direccion[1]
            case 2:
                perp_x = -self.direccion[1]
                perp_y = self.direccion[0]

                amplitud = 20
                frecuencia = 200

                offset = math.sin(self.t * frecuencia) * amplitud

                self.x += dt * self.velocidad * self.direccion[0] + perp_x * offset
                self.y += dt * self.velocidad * self.direccion[1] + perp_y * offset
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
        self.rect.x = self.x
        self.rect.y = self.y
