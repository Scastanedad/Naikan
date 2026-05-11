from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee, EnemigoDistancia
from entidades.ET_general import Proyectil
import math,pygame, random
class Boss1(Enemigos):
    def __init__(self, x, y,in_pos):
        super().__init__(x, y, vida=10, velocidad=50, width=30, heigth=30, color = (200,200,100))
        self.cooldownP = 0
        self.cooldownSP = 0
        self.intervaloP = 1.5
        self.intervaloSP = 4
        self.in_pos = in_pos
        
        
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
            
            spawn_x = self.x + 20 * dx
            spawn_y = self.y + 20 * dy
            # En ET_E_miniBoss1.py, justo antes de crear el proyectil:
            eventos.append(Proyectil(spawn_x, spawn_y, (dx, dy), 800, 2, dueño="Boss"))
        self.cooldownSP+= dt
        if self.cooldownSP >= self.intervaloSP:
            self.cooldownSP = 0
            if (random.randint(1,2) == 1):
                eventos.append(EnemigoMelee(self.x,self.y,[self.x,self.y]))
            else:
                eventos.append(EnemigoDistancia(self.x,self.y,[self.x,self.y]))
        return eventos
        
    
    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)
    
    def draw(self, screen, color=(100,0,0)):
        pygame.draw.rect(screen, color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
        for i in range(self.vida):
            pygame.draw.rect(screen, (0,255,0), (400 + 10*i, 10, 5, 5))
    def destruir(self,miniBossD):
        self.recibirDaño(1)
        if (self.vida <= 0):
            miniBossD.remove(self)
            self.kill()
        
        