from entidades.enemigos.ET_E_base import Enemigos
from entidades.ET_general import Proyectil
import math, pygame

#Clase que describe los enemigos que disparan a la distancia

class EnemigoDistancia(Enemigos):
    def __init__(self, x, y):
        super().__init__(x, y, vida= 2, velocidad=250, width=20,heigth=20)
        #Cada cuanto dispara
        self.cooldown = 0
        self.intervalo = 2

    def update(self, dt, jugador):
        #Obtenemos la distancia en x y en y del jugador
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        #Distancia real ( pitagoras )
        distancia = math.sqrt(dx**2 + dy**2)

        #Obtenemos los vectores direccion en x y en y
        if distancia !=0:
            dx = dx/ distancia
            dy = dy/distancia
        
        #Si esta muy cerca, se aleja, si esta cerca, se aleja
        if (distancia <= 300):
            if ( self.x >20 and self.x<780):
                self.x -= dx * dt * self.velocidad
            if( self.y > 20 and self.y<580):
                self.y -= dy * dt * self.velocidad
        
        if ( distancia >= 310):
            self.x += dx * dt * self.velocidad
            self.y += dy * dt * self.velocidad

        self.cooldown += dt
        if self.cooldown >= self.intervalo:
            self.cooldown = 0
            self.actualizarRect()
            return Proyectil(self.x+ 20*dx, self.y+ 20* dy,  (dx,dy), 800)

        self.actualizarRect()

        
    def draw(self, screen, color = (200,200,0)):
        return super().draw(screen, color)