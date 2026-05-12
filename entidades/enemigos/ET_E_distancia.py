from entidades.enemigos.ET_E_base import Enemigos, FRAME_CONFIG_ENEMIGO
from entidades.ET_general import Proyectil
import math

class EnemigoDistancia(Enemigos):
    def __init__(self, x, y, mundo=1, in_pos=[], listaEM=[]):
        self.in_pos = in_pos
        self.listaEM = listaEM
        self.cooldown = 0
        self.intervalo = 2

        super().__init__(
            x, y,
            vida=2,
            velocidad=250,
            width=20,
            heigth=20,
            color=(100, 0, 0),
            sprite_path=f"assets/sprites/enemigo_distancia/sprite{mundo}.png",
            frame_config=FRAME_CONFIG_ENEMIGO,
        )

    def update(self, dt, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        if distancia != 0:
            dx = dx / distancia
            dy = dy / distancia

        # Se aleja si está muy cerca, se acerca si está lejos
        if distancia <= 300:
            if self.x > 20 and self.x < 780:
                self.x -= dx * dt * self.velocidad
            if self.y > 20 and self.y < 580:
                self.y -= dy * dt * self.velocidad
        elif distancia >= 310:
            self.x += dx * dt * self.velocidad
            self.y += dy * dt * self.velocidad

        # Actualiza dirección para la animación
        if abs(dx) > abs(dy):
            self.direccion = (1, 0) if dx > 0 else (-1, 0)
        else:
            self.direccion = (0, 1) if dy > 0 else (0, -1)

        self.moviendo = True
        self.animar(dt)  # ← heredado de Entidad

        self.cooldown += dt
        if self.cooldown >= self.intervalo:
            self.cooldown = 0
            self.actualizarRect()
            return Proyectil(self.x + 20 * dx, self.y + 20 * dy, (dx, dy), 800)

        self.actualizarRect()

    def destruir(self):
        if self.in_pos in self.listaEM:
            self.listaEM.remove(self.in_pos)
            from escenas.workModules.filtros import Filtros
            Filtros.quitarse_lista(self)
        self.kill()
        return self.listaEM
