from entidades.ET_general import Entidad
from escenas.UT_guardado import cargarConfig
import pygame

class Jugador(Entidad):


    def __init__(self, x, y):
        # Config de animación: 4 direcciones x 4 frames, cada fila de 32px de alto
        self.sprite_bala = pygame.image.load("assets/sprites/jugador/spriteDisparoJ.png")
        frame_config = {
            (1,  0): {"fila": 0,   "count": 4},
            (-1, 0): {"fila": 32,  "count": 4},
            (0, -1): {"fila": 64,  "count": 4},
            (0,  1): {"fila": 96,  "count": 4},
        }

        self.ss_objeto = None  # Evita error en el super antes de que se asigne

        super().__init__(
            x, y,
            vida=3,
            velocidad=300,
            width=32,
            heigth=32,
            color=(0, 0, 100),
            sprite_path="assets/sprites/jugador/spriteJugador.png",
            frame_config=frame_config,
            escala=2,
            anim_speed=0.1
        )

        self.dañoCooldown = 1
        self.intervaloD = 1
        self.cooldown = 2
        self.intervalo = 2

        from escenas.workModules.filtros import Filtros
        self.configurar_filtro(Filtros.filtro_actual)

    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros
        if self.ss_original is not None:
            self.ss_filtrada = Filtros.aplicar_filtro(self.ss_original, nuevo_filtro)
        super().configurar_filtro(nuevo_filtro)

    def update(self, dt, keys, width, height):
        self.mover(dt, keys, width, height)
        self.animar(dt)  # ← heredado de Entidad

    def mover(self, dt, keys, width, height):
        configuracion = cargarConfig()
        teclas = configuracion["teclas"]
        self.cooldown += dt
        self.dañoCooldown += dt
        self.moviendo = False

        if (keys[teclas["arriba"]] or keys[pygame.K_UP]) and (self.y > 40):
            self.y -= self.velocidad * dt
            self.direccion = (0, -1)
            self.moviendo = True
        if (keys[teclas["abajo"]] or keys[pygame.K_DOWN]) and (self.y < height - 40):
            self.y += self.velocidad * dt
            self.direccion = (0, 1)
            self.moviendo = True
        if (keys[teclas["derecha"]] or keys[pygame.K_RIGHT]) and (self.x < width - 40):
            self.x += self.velocidad * dt
            self.direccion = (1, 0)
            self.moviendo = True
        if (keys[teclas["izquierda"]] or keys[pygame.K_LEFT]) and (self.x > 40):
            self.x -= self.velocidad * dt
            self.direccion = (-1, 0)
            self.moviendo = True

        if keys[pygame.K_c] and (self.cooldown >= self.intervalo):
            self.cooldown = 0
            if (self.x < 680) and (self.x > 120):
                self.x += 100 * self.direccion[0]
            if (self.y < 480) and (self.y > 120):
                self.y += 100 * self.direccion[1]
            self.moviendo = True

        self.actualizarRect()

    def recibirDaño(self, Daño=None):
        return super().recibirDaño(Daño=1)

    def actualizarRect(self):
        return super().actualizarRect()
