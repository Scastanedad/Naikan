from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee
from entidades.ET_general import Proyectil
import math,pygame
class MiniBoss1(Enemigos):
    def __init__(self, x, y):
        super().__init__(x, y, vida=10, velocidad=50, width=30, heigth=30, color = (200,200,100))
        self.cooldownP = 0
        self.cooldownSP = 0
        self.intervaloP = 1.5
        self.intervaloSP = 4
        
        

    def update(self, dt, jugador):
        eventos = []
        dx = jugador.sprite.x - self.x
        dy = jugador.sprite.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        #Obtenemos los vectores direccion en x y en y
        if distancia !=0:
            dx = dx/ distancia
            dy = dy/distancia
        
        self.x += dx * dt * self.velocidad
        self.y += dy * dt * self.velocidad
        self.cooldownP += dt
        self.actualizarRect()
        if self.cooldownP >= self.intervaloP:
            self.cooldownP = 0
            self.actualizarRect()
            eventos.append( Proyectil(self.x+ 30*dx, self.y+ 30* dy,  (dx,dy), 800,2))
        self.cooldownSP+= dt
        if self.cooldownSP >= self.intervaloSP:
            self.cooldownSP = 0
            eventos.append(EnemigoMelee(self.x,self.y,[self.x,self.y]))
        return eventos
        
    
    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)
    
    def draw(self, screen, color=(100,0,0)):
        pygame.draw.rect(screen, color, (self.x,self.y,self.width, self.height))
        for i in range(self.vida):
            pygame.draw.rect(screen,(0,255,0),(400+10*i, 10, 5,5))
        