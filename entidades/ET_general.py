import pygame, math
from entidades.UT_spritesheet import SpriteSheet

# Clase base para todas las entidades
class Entidad(pygame.sprite.Sprite):
    def __init__(self, x, y, vida, velocidad, width, heigth, color,
                 sprite_path=None,
                 frame_config=None,
                 escala=1,
                 anim_speed=0.1):
        super().__init__()
        self.x = x
        self.y = y
        self.vida = vida
        self.velocidad = velocidad
        self.width = width
        self.height = heigth

        self.color_original = color
        self.color_actual = color

        # Spritesheet
        self.ss_objeto = None
        self.ss_original = None
        self.ss_filtrada = None
        self.frame_config = frame_config  # dict: {direccion: {"fila": y, "count": n}}
        self.escala = escala

        # Animación
        self.direccion = (1, 0)
        self.moviendo = False
        self.timer_anim = 0
        self.frame_index = 0
        self.anim_speed = anim_speed
        self.animaciones = {}

        if sprite_path:
            self.ss_objeto = SpriteSheet(sprite_path)
            self.ss_original = self.ss_objeto.sheet.copy()
            self.ss_filtrada = self.ss_original.copy()

        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)

        self.preparar_visuales()

    def preparar_visuales(self):
        # Si tiene spritesheet y config de frames, construye las animaciones
        if self.ss_objeto is not None and self.frame_config is not None and self.ss_filtrada is not None:
            self.ss_objeto.sheet = self.ss_filtrada
            self.animaciones = {
                dir: self.ss_objeto.get_fila(
                    y=cfg["fila"],
                    width=self.width,
                    height=self.height,
                    count=cfg["count"],
                    escala=self.escala
                )
                for dir, cfg in self.frame_config.items()
            }
            self.image = self.animaciones[self.direccion][self.frame_index]
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            # Fallback: rectángulo de color (mientras no tiene sprite)
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(self.color_actual)
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def animar(self, dt):
        if not self.animaciones:
            return
        frames = self.animaciones[self.direccion]
        if self.moviendo:
            self.timer_anim += dt
            if self.timer_anim >= self.anim_speed:
                self.timer_anim = 0
                self.frame_index = (self.frame_index + 1) % len(frames)
        else:
            self.frame_index = 0
            self.timer_anim = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros

        if self.ss_original is None and self.color_original is None:
            return

        if self.ss_original is not None:
            self.ss_filtrada = Filtros.aplicar_filtro(self.ss_original, nuevo_filtro)

        if self.color_original is not None:
            super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
            color_con_alpha = (self.color_original[0], self.color_original[1], self.color_original[2], 255)
            super_temp.fill(color_con_alpha)
            self.color_actual = Filtros.aplicar_filtro(super_temp, nuevo_filtro).get_at((0, 0))

        self.preparar_visuales()

    def recibirDaño(self, Daño):
        self.vida -= Daño

    def update(self, dt, keys, width, height):
        pass

    def actualizarRect(self):
        self.rect.center = (self.x, self.y)


class Proyectil(pygame.sprite.Sprite):

    def __init__(self, x, y, direccion, velocidad=600, modo=1, color=(0, 0, 200), dueño="enemigo"):
        super().__init__()
        self.dueño = dueño
        self.x = x
        self.y = y
        self.modo = modo
        self.velocidad = velocidad
        self.direccion = direccion
        self.width = 5
        self.height = 5

        self.color_original = color
        self.color_actual = color

        self.grace_period = 0.1
        self.t = 0

        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)

        self.preparar_visuales()

    def preparar_visuales(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color_actual)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros

        super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
        color_con_alpha = (self.color_original[0], self.color_original[1], self.color_original[2], 255)
        super_temp.fill(color_con_alpha)
        self.color_actual = Filtros.aplicar_filtro(super_temp, nuevo_filtro).get_at((0, 0))

        self.preparar_visuales()

    def update(self, dt):
        self.t += dt
        self.grace_period -= dt
        match self.modo:
            case 1:
                self.x += dt * self.velocidad * self.direccion[0]
                self.y += dt * self.velocidad * self.direccion[1]
            case 2:
                perp_x = -self.direccion[1]
                perp_y = self.direccion[0]
                amplitud = 20
                frecuencia = 200
                offset = math.sin(self.t * frecuencia) * amplitud
                self.x += dt * self.velocidad * self.direccion[0] + perp_x * offset
                self.y += dt * self.velocidad * self.direccion[1] + perp_y * offset
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
            from escenas.workModules.filtros import Filtros
            Filtros.quitarse_lista(self)

        self.rect.center = (self.x, self.y)
