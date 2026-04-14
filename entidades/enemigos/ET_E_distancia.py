from entidades.enemigos.ET_E_base import Enemigos
import math, pygame

class EnemigoDistancia(Enemigos):
    def __init__(self, x, y):
        super().__init__(x, y, vida= 2, velocidad=250, width=20,heigth=20)

    def update(self, dt, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        #Obtenemos los vectores direccion en x y en y
        if distancia !=0:
            dx = dx/ distancia
            dy = dy/distancia
        
        if (distancia <= 300):
            if ( self.x >20 and self.x<780):
                self.x -= dx * dt * self.velocidad
            if( self.y > 20 and self.y<580):
                self.y -= dy * dt * self.velocidad
        
        if ( distancia >= 301):
            self.x += dx * dt * self.velocidad
            self.y += dy * dt * self.velocidad

        self.actualizarRect()

        
    def draw(self,screen, ):
        pygame.draw.rect(screen, (100,100,0), (self.x,self.y,self.width, self.heigth))