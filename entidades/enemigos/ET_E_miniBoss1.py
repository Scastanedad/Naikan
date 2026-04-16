from entidades.enemigos.ET_E_base import Enemigos
from entidades.ET_general import Proyectil
import math,pygame
class MiniBoss1(Enemigos):
    def __init__(self, x, y):
        self.cooldown = 0
        self.intervalo = 1
        super().__init__(x, y, vida=10, velocidad=50, width=30, heigth=30)

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
        self.cooldown += dt
        if self.cooldown >= self.intervalo:
            self.cooldown = 0
            self.actualizarRect()
            return Proyectil(self.x+ 30*dx, self.y+ 30* dy,  (dx,dy), 800,2)

        self.actualizarRect()
    
    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)
    
    def draw(self, screen, color=(100,0,0)):
        for i in range(self.vida):
            pygame.draw.rect(screen,(0,255,0),(400+10*i, 10, 5,5))
        return super().draw(screen, color)