from entidades.enemigos.ET_E_base import Enemigos
import math, pygame
#Clase base para los enemigos cuerpo
class EnemigoMelee(Enemigos):
    def __init__(self, x, y,in_pos,listaEM = []):
        super().__init__(x, y, vida= 2, velocidad=150, width=20,heigth=20,color = (0,100,0))
        self.in_pos = in_pos
        self.listaEM = listaEM

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

    def destruir(self):
        if self.in_pos in self.listaEM:
            self.listaEM.remove(self.in_pos)
        self.kill()
        return self.listaEM

    