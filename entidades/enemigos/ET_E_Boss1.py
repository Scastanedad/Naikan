from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee, EnemigoDistancia
from entidades.ET_general import Proyectil
from escenas.workModules.icono import Icono
from G_utils import resource_path
import math, pygame, random

FRAME_CONFIG_BOSS1 = {
    (1, 0): {"fila": 0, "count": 4},
    (-1, 0): {"fila": 64, "count": 4},
    (0, -1): {"fila": 128, "count": 4},
    (0, 1): {"fila": 192, "count": 4},
}


class Boss1(Enemigos):
    def __init__(self, x, y, in_pos):
        super().__init__(
            x,
            y,
            vida=10,
            velocidad=50,
            width=64,
            heigth=64,
            color=(200, 200, 100),
            sprite_path="assets/sprites/bosses/boss_mundo1.png",
            frame_config=FRAME_CONFIG_BOSS1,
            escala=2,
        )
        self.cooldownP = 0
        self.cooldownSP = 0
        self.intervaloP = 1.5
        self.intervaloSP = 4
        self.in_pos = in_pos

        imagen_corazon = pygame.image.load(
            resource_path("assets/sprites/bosses/corazon.png")
        ).convert_alpha()
        imagen_corazon = pygame.transform.smoothscale(imagen_corazon, (25, 25))
        self.icono_corazon = Icono(0, 0, imagen_corazon)
        
        self.sprite_bala = pygame.image.load(resource_path(
            "assets/sprites/bosses/proyectilCompleto.png")
        ).convert_alpha()
        
        self.sprite_bala = pygame.transform.scale(self.sprite_bala, (16, 16))

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

        self.cooldownP += dt
        self.actualizarRect()
        if self.cooldownP >= self.intervaloP:
            self.cooldownP = 0
            self.actualizarRect()

            spawn_x = self.x + 20 * dx
            spawn_y = self.y + 20 * dy
            # En ET_E_miniBoss1.py, justo antes de crear el proyectil:
            eventos.append(Proyectil(spawn_x, spawn_y, (dx, dy), 800, 2, (0, 0, 200),"Boss", self.sprite_bala))
        self.cooldownSP += dt
        if self.cooldownSP >= self.intervaloSP:
            self.cooldownSP = 0
            if random.randint(1, 2) == 1:
                eventos.append(EnemigoMelee(self.x, self.y, 1, [self.x, self.y]))
            else:
                eventos.append(EnemigoDistancia(self.x, self.y, 1, [self.x, self.y]))
        return eventos

    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)

    def draw(self, screen, color=(100, 0, 0)):
        screen.blit(self.image, self.rect)

        for i in range(self.vida):
            pos_x = 750
            pos_y = 150 + (30 * i)
            screen.blit(self.icono_corazon.image, (pos_x, pos_y))

    def destruir(self, miniBossD):
        self.recibirDaño(1)
        if self.vida <= 0:
            miniBossD.remove(self)
            from escenas.workModules.filtros import Filtros

            Filtros.quitarse_lista(self)
            self.kill()


# Esta clase al no tener sprite todavía usa la lógica más base de los filtros que es para los rectangulos, que está en la lógica
# de la clase Entidad
