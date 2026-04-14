from habitaciones.H_base import Habitacion, Obstaculo
from entidades import EnemigoDistancia

class HabitacionEnemigos(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)
        self.obstaculos = [Obstaculo(x,y) for x,y in datos["obstaculos"]]
        self.enemigosM = [EnemigoDistancia(x,y)for x,y in datos["enemigosM"]]
    
    def update(self, dt, keys,Jugador1, WIDTH, HEIGTH):
        for e in self.enemigosM:
            if Jugador1.rect.colliderect(e.rect):
                Jugador1.x = WIDTH//2
                Jugador1.y = HEIGTH//2
                Jugador1.recibirDaño()
            for p in self.Proyectiles:
                if p.rect.colliderect(e.rect):
                    self.enemigosM.remove(e)
                    self.datos["enemigosM"] = self.enemigosM
        for o in self.obstaculos:
            if Jugador1.rect.colliderect(o.rect):
                Jugador1.x = WIDTH//2
                Jugador1.y = HEIGTH//2
                Jugador1.recibirDaño()
            for p in self.Proyectiles:
                    if p.rect.colliderect(o.rect):
                        self.obstaculos.remove(o)
                        self.datos["obstaculos"] = self.obstaculos
        for e in self.enemigosM:
            e.update(dt, Jugador1)
        for p in self.Proyectiles:
            p.update(dt)  

    def draw(self, screen):
        for o in self.obstaculos:
            o.draw(screen)
        for p in self.Proyectiles:
            p.draw(screen)
        for e in self.enemigosM: 
            e.draw(screen)