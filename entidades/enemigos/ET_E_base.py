from entidades.ET_general import Entidad

class Enemigos(Entidad):
    def __init__(self, x, y, vida, velocidad, width, heigth):
        super().__init__(x, y, vida, velocidad, width, heigth)
    
    def update(self,dt, obstaculos, jugador):
        pass

    def recibirDaño(self,Danio):
        self.vida -= 1

    def actualizarRect(self):
        self.rect.x = self.x
        self.rect.y = self.y  