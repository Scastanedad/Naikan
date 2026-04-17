from entidades.ET_general import Entidad
import pygame

class Jugador(Entidad):
    #Metodo constructor de la clase
    def __init__(self, x, y, vida= None, velocidad= None, width= None, heigth = None):
        super().__init__(x, y, vida= 3, velocidad=300, width=20, heigth=20)
        self.direccion= (1,0)
        self.dañoCooldown=1
        self.intervaloD = 1
        self.cooldown = 2
        self.intervalo = 2
    
    def update(self,dt,keys,width,height):
        self.mover(dt,keys,width,height)
    
    #El movimiento asociado a las teclas
    def mover(self,dt,keys, width, height):
        self.cooldown +=dt
        self.dañoCooldown += dt
        if (keys[pygame.K_w] or keys[pygame.K_UP])and (self.y >0):
            self.y -= self.velocidad * dt 
            self.direccion = (0,-1)
        if( keys[pygame.K_s]or keys[pygame.K_DOWN] )and (self.y < height-20):
            self.y += self.velocidad*dt
            self.direccion = (0,1)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (self.x < width-20):
            self.x += self.velocidad * dt
            self.direccion = (1,0)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (self.x >0) :
            self.x -= self.velocidad * dt
            self.direccion = (-1,0)
        #Dash funcional
        if(keys[pygame.K_c] and (self.cooldown>=self.intervalo)):
            self.cooldown = 0
            self.x +=100*self.direccion[0]
            self.y+=100*self.direccion[1]
        self.actualizarRect()
       
    def recibirDaño(self, Daño=None):
        return super().recibirDaño(Daño=1)
    
    def actualizarRect(self):
        return super().actualizarRect()




    