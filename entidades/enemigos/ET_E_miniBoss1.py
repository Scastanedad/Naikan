from entidades.enemigos.ET_E_base import Enemigos
import math,pygame
class MiniBoss1(Enemigos):
    def __init__(self, x, y):
        super().__init__(x, y, vida=10, velocidad=150, width=30, heigth=30)

    def update(self, dt, obstaculos, jugador):
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
    
    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)
    
    def draw(self, screen, color=(100,0,0)):
        for i in range(self.vida):
            pygame.draw.rect(screen,(0,255,0),(400+10*i, 10, 5,5))
        return super().draw(screen, color)