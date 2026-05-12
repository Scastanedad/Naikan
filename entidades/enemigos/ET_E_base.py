from entidades.ET_general import Entidad
import pygame

# Config estándar para enemigos: 4 direcciones x 2 frames
# Cada hijo puede sobreescribir esto si necesita algo distinto
FRAME_CONFIG_ENEMIGO = {
    (1,  0): {"fila": 0,  "count": 2},
    (-1, 0): {"fila": 32, "count": 2},
    (0, -1): {"fila": 64, "count": 2},
    (0,  1): {"fila": 96, "count": 2},
}

class Enemigos(Entidad):
    def __init__(self, x, y, vida, velocidad, width, heigth, color,
                 sprite_path=None,
                 frame_config=None,
                 escala=1):
        super().__init__(
            x, y, vida, velocidad, width, heigth, color,
            sprite_path=sprite_path,
            frame_config=frame_config,
            escala=escala
        )

    def update(self, dt, jugador):
        pass

    def recibirDaño(self, Danio):
        self.vida -= 1

    def actualizarRect(self):
        self.rect.center = (self.x, self.y)
