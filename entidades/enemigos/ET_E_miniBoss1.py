from entidades.enemigos.ET_E_base import Enemigos
class MiniBoss1(Enemigos):
    def __init__(self, x, y, vida, velocidad, width, heigth):
        super().__init__(x, y, vida, velocidad, width, heigth)

    def update(self, dt, obstaculos, jugador):
        return super().update(dt, obstaculos, jugador)
    
    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)
    
    def draw(self, screen, color):
        return super().draw(screen, color)