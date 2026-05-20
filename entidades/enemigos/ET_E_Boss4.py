from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee, EnemigoDistancia
from entidades.ET_general import Proyectil
from escenas.workModules.icono import Icono
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager
import math, pygame, random

FRAME_CONFIG_F1 = {
    (1, 0):  {"fila": 0,   "count": 4},
    (-1, 0): {"fila": 64,  "count": 4},
    (0, -1): {"fila": 128, "count": 4},
    (0, 1):  {"fila": 192, "count": 4},
}
FRAME_CONFIG_F2 = {
    (1, 0):  {"fila": 0,   "count": 4},
    (-1, 0): {"fila": 64,  "count": 4},
    (0, -1): {"fila": 128, "count": 4},
    (0, 1):  {"fila": 192, "count": 4},
}
FRAME_CONFIG_F3 = {
    (1, 0):  {"fila": 0,   "count": 4},
    (-1, 0): {"fila": 64,  "count": 4},
    (0, -1): {"fila": 128, "count": 4},
    (0, 1):  {"fila": 192, "count": 4},
}


class Boss4(Enemigos):
    def __init__(self, x, y, in_pos):
        super().__init__(
            x, y,
            vida=50,
            velocidad=50,
            width=64,
            heigth=64,
            color=(200, 200, 100),
            sprite_path=resource_path("assets/sprites/bosses/boss_mundo4_f1.png"),
            frame_config=FRAME_CONFIG_F1,
            escala=2,
        )
        self.in_pos = in_pos
        self.vidaInicial = 50

        imagen_corazon = AssetManager.get_image(
            "assets/sprites/bosses/corazon.png"
        ).convert_alpha()
        imagen_corazon = pygame.transform.smoothscale(imagen_corazon, (18, 18))
        self.icono_corazon = Icono(0, 0, imagen_corazon)

        self.sprite_bala = AssetManager.get_image(
            "assets/sprites/bosses/proyectilCompleto.png"
        )
        self.sprite_bala = pygame.transform.scale(self.sprite_bala, (20, 20))

        self.fase = 1

        #  Fase 2 
        self.cooldown_disparo = 0
        self.intervalo_disparo = 1.5
        self.hits_fase2 = 0

        #  Fase 3
        self.cooldown_spawn = 0
        self.intervalo_spawn = 2.0
        self.timer_fase3 = 0
        self.duracion_fase3 = 15.0
        self.escudo_activo = True


    def _cambiar_fase(self, nueva_fase):
        self.fase = nueva_fase
        self._cambiar_posicion_aleatoria()

        sprite_por_fase = {
            1: "assets/sprites/bosses/boss_mundo4_f1.png",
            2: "assets/sprites/bosses/boss_mundo4_f2.png",
            3: "assets/sprites/bosses/boss_mundo4_f3.png",
        }
        config_por_fase = {
            1: FRAME_CONFIG_F1,
            2: FRAME_CONFIG_F2,
            3: FRAME_CONFIG_F3,
        }

        nueva_sheet = AssetManager.get_image(
            sprite_por_fase[nueva_fase]
        ).convert_alpha()
        self.cargar_sprite(nueva_sheet, config_por_fase[nueva_fase])

    def _cambiar_posicion_aleatoria(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)


    def update(self, dt, jugador):
        eventos = []
        dx = jugador.sprite.x - self.x
        dy = jugador.sprite.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)
        if distancia != 0:
            dx /= distancia
            dy /= distancia


        if self.fase == 1 and self.vida <= 35:
            self._cambiar_fase(2)

        elif self.fase == 2 and self.vida <= 15:
            self._cambiar_fase(3)
            self.escudo_activo = True


        if self.fase == 1:
            self.x += dx * dt * self.velocidad
            self.y += dy * dt * self.velocidad


        elif self.fase == 2:
            if distancia < 300:
                self.x -= dx * dt * self.velocidad
                self.y -= dy * dt * self.velocidad

            self.cooldown_disparo += dt
            if self.cooldown_disparo >= self.intervalo_disparo:
                self.cooldown_disparo = 0
                self.actualizarRect()
                offset = (self.ancho_real / 2) + 10
                eventos.append(Proyectil(
                    self.x + offset * dx,
                    self.y + offset * dy,
                    (dx, dy),
                    800, 2,
                    (0, 0, 200),
                    "Boss",
                    self.sprite_bala,
                ))

        elif self.fase == 3:
            self.timer_fase3 += dt
            if self.timer_fase3 >= self.duracion_fase3:
                self.vida = 0
                return eventos

            self.cooldown_spawn += dt
            if self.cooldown_spawn >= self.intervalo_spawn:
                self.cooldown_spawn = 0
                if random.randint(1, 2) == 1:
                    eventos.append(EnemigoMelee(self.x, self.y, 4, [self.x, self.y]))
                else:
                    eventos.append(EnemigoDistancia(self.x, self.y, 4, [self.x, self.y]))

        if abs(dx) > abs(dy):
            self.direccion = (1, 0) if dx > 0 else (-1, 0)
        else:
            self.direccion = (0, 1) if dy > 0 else (0, -1)
        self.moviendo = True
        self.animar(dt)
        return eventos

    def recibirDaño(self, danio):
        if self.fase == 3 and self.escudo_activo:
            return

        super().recibirDaño(danio)

        if self.fase == 2:
            self.hits_fase2 += 1
            if self.hits_fase2 >= 2:
                self.hits_fase2 = 0
                self._cambiar_posicion_aleatoria()

    def draw(self, screen, color=(100, 0, 0)):
        screen.blit(self.image, self.rect)

        if self.fase == 3 and self.escudo_activo:
            pygame.draw.circle(
                screen, (100, 180, 255),
                (int(self.x), int(self.y)),
                self.ancho_real // 2 + 20,
                3,
            )

        for i in range(self.vida):
            pos_x = 765
            pos_y = 40 + (21 * i)
            screen.blit(self.icono_corazon.image, (pos_x, pos_y))

    def destruir(self, grupo):
        self.recibirDaño(1)
        if self.vida <= 0:
            grupo.remove(self)
            from escenas.workModules.filtros import Filtros
            Filtros.quitarse_lista(self)
            self.kill()