from entidades.enemigos.ET_E_base import Enemigos
class MiniBoss1(Enemigos):
    def __init__(self, x, y, vida, velocidad, width, heigth):
        super().__init__(x, y, vida, velocidad, width, heigth)