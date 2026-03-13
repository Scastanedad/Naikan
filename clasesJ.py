import pygame
import math

#Clase abstracta para todas las entidades
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

class Jugador(Entidad):
    #Metodo constructor de la clase
    def __init__(self, x, y, vida= None, velocidad= None, width= None, heigth = None):
        super().__init__(x, y, vida= 3, velocidad=300, width=20, heigth=20)
    
    def mover(self,dt,keys, width, height):
        
        if keys[pygame.K_w] and (self.y >0):
            self.y -= self.velocidad * dt 
            self.direccion = (0,-1)
        if keys[pygame.K_s] and (self.y < height-20):
            self.y += self.velocidad*dt
            self.direccion = (0,1)
        if keys[pygame.K_d] and (self.x < width-20):
            self.x += self.velocidad * dt
            self.direccion = (1,0)
        if keys[pygame.K_a] and (self.x >0) :
            self.x -= self.velocidad * dt
            self.direccion = (-1,0)
        self.actualizarRect()
       
    def recibirDaño(self, Daño=None):
        return super().recibirDaño(Daño=1)
    
    def actualizarRect(self):
        return super().actualizarRect()

    def draw(self,screen):
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y, 20,20))

class Proyectil:
  
    def __init__(self, x ,y,direccion):
        self.x = x
        self.y = y+9
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

        
class Enemigos(Entidad):
    def __init__(self, x, y, vida, velocidad, width, heigth):
        super().__init__(x, y, vida, velocidad, width, heigth)
    
    def update(self,dt, obstaculos, jugador):
        pass

    def recibirDaño(self,Danio):
        self.vida -= 1

    def actualizarRect(self):
        self.rect.x = self.x
        self.rect.y = self.y    

class EnemigoMelee(Enemigos):
    def __init__(self, x, y):
        super().__init__(x, y, vida= 2, velocidad=150, width=20,heigth=20)

    def update(self, dt, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        #Obtenemos los vectores direccion en x y en y
        if distancia !=0:
            dx = dx/ distancia
            dy = dy/distancia
        
        self.x += dx * dt * self.velocidad
        self.y += dy * dt * self.velocidad

        self.actualizarRect()

        
    def draw(self,screen, ):
        pygame.draw.rect(screen, (100,100,0), (self.x,self.y,self.width, self.heigth))
        
