from entidades.enemigos.ET_E_base import Enemigos, FRAME_CONFIG_ENEMIGO
import math

class EnemigoMelee(Enemigos):
    def __init__(self, x, y, mundo=1, in_pos=[], listaEM=[]):
        self.in_pos = in_pos
        self.listaEM = listaEM

        super().__init__(
            x, y,
            vida=2,
            velocidad=150,
            width=20,
            heigth=20,
            color=(0, 100, 0),
            sprite_path=f"assets/sprites/enemigo_melee/sprite{mundo}.png",
            frame_config=FRAME_CONFIG_ENEMIGO,
        )

    def update(self, dt, jugador):
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
