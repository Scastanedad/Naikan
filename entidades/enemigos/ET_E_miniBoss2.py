from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee
from G_utils import resource_path
import math, pygame, random
from escenas.workModules.asset_manager import AssetManager
from escenas.workModules.icono import Icono

FRAME_CONFIG_miniBOSS2 = {
    (1, 0): {"fila": 0, "count": 4},
    (-1, 0): {"fila": 64, "count": 4},
    (0, -1): {"fila": 128, "count": 4},
    (0, 1): {"fila": 192, "count": 4},
}


class miniBoss2(Enemigos):
    def __init__(self, x, y, in_pos):
        super().__init__(
            x,
            y,
            vida=15,
            velocidad=50,
            width=64,
            heigth=64,
            color=(200, 200, 100),
            sprite_path=resource_path("assets/sprites/minibosses/miniboss_mundo2.png"),
            frame_config=FRAME_CONFIG_miniBOSS2,
            escala=2,
        )
        self.in_pos = in_pos
        self.vidaInicial = 15

        imagen_corazon = AssetManager.get_image(
            "assets/sprites/bosses/corazon.png"
        ).convert_alpha()
        imagen_corazon = pygame.transform.smoothscale(imagen_corazon, (25, 25))
        self.icono_corazon = Icono(0, 0, imagen_corazon)

    def update(self, dt, jugador):
        eventos = []
        dx = jugador.sprite.x - self.x
        dy = jugador.sprite.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        # Obtenemos los vectores direccion en x y en y
        if distancia != 0:
            dx = dx / distancia
            dy = dy / distancia

        self.x += dx * dt * self.velocidad
        self.y += dy * dt * self.velocidad

        if abs(dx) > abs(dy):
            self.direccion = (1, 0) if dx > 0 else (-1, 0)
        else:
            self.direccion = (0, 1) if dy > 0 else (0, -1)

        self.moviendo = True
        self.animar(dt)

        self.actualizarRect()
        # Si le pegan spawnea a un enemigoMelee
        if self.vidaInicial > self.vida:
            self.vidaInicial = self.vida
            eventos.append(EnemigoMelee(self.x, self.y, 2, [self.x, self.y]))

    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)

    def draw(self, screen, color=(100, 0, 0)):
        # pygame.draw.rect(screen, color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
        screen.blit(self.image, self.rect)

        for i in range(self.vida):
            pos_x = 770
            pos_y = 100 + (30 * i)
            screen.blit(self.icono_corazon.image, (pos_x, pos_y))

    def destruir(self, miniBossD):
        self.recibirDaño(1)
        if self.vida <= 0:
            miniBossD.remove(self)
            from escenas.workModules.filtros import Filtros

            Filtros.quitarse_lista(self)
            self.kill()


