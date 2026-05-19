from entidades.enemigos.ET_E_base import Enemigos, FRAME_CONFIG_ENEMIGO
from G_utils import resource_path
import math

FRAME_CONFIG_ENEMIGO_M2 = {
    (1, 0): {"fila": 0, "count": 4},  
    (-1, 0): {"fila": 48, "count": 4}, 
    (0, -1): {"fila": 96, "count": 4},  
    (0, 1): {"fila": 144, "count": 4}   
}

FRAME_CONFIG_ENEMIGO_M3 = {
    (1, 0): {"fila": 192, "count": 4},  
    (-1, 0): {"fila": 192, "count": 4}, 
    (0, 1): {"fila": 192, "count": 4},   
    (0, -1): {"fila": 0, "count": 4}
}

class EnemigoMelee(Enemigos):
    def __init__(self, x, y, mundo=1, in_pos=[], listaEM=[]):
        self.in_pos = in_pos
        self.listaEM = listaEM
        
        if mundo == 3:
            config_usar = FRAME_CONFIG_ENEMIGO_M3
            ancho_frame = 64 
            alto_frame = 64
        elif mundo == 2:
            config_usar = FRAME_CONFIG_ENEMIGO_M2
            ancho_frame = 48 
            alto_frame = 48
        else:
            config_usar = FRAME_CONFIG_ENEMIGO
            ancho_frame = 32
            alto_frame = 32

        super().__init__(
            x, y,
            vida=2,
            velocidad=150,
            width=ancho_frame,
            heigth=alto_frame,
            color=(0, 100, 0),
            sprite_path=resource_path(f"assets/sprites/enemigo_melee/melee_mundo{mundo}.png"),
            frame_config=config_usar, escala = 1.5
        )

    def update(self, dt, jugador):
        self.t_carga += dt
        if self.t_carga > self.intervaloCarga:
            dx = jugador.x - self.x
            dy = jugador.y - self.y
            distancia = math.sqrt(dx**2 + dy**2)

            if distancia != 0:
                dx = dx / distancia
                dy = dy / distancia

            self.x += dx * dt * self.velocidad
            self.y += dy * dt * self.velocidad

            # Actualiza dirección para la animación
            if abs(dx) > abs(dy):
                self.direccion = (1, 0) if dx > 0 else (-1, 0)
            else:
                self.direccion = (0, 1) if dy > 0 else (0, -1)

            self.moviendo = True
            self.animar(dt)  # ← heredado de Entidad
            self.actualizarRect()

    def destruir(self):
        if self.in_pos in self.listaEM:
            self.listaEM.remove(self.in_pos)
            from escenas.workModules.filtros import Filtros
            Filtros.quitarse_lista(self)
        self.kill()
        return self.listaEM
