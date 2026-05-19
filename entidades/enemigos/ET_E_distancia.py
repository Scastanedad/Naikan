from entidades.enemigos.ET_E_base import Enemigos, FRAME_CONFIG_ENEMIGO
from entidades.ET_general import Proyectil
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager
import math
import pygame

FRAME_CONFIG_DISTANCIA_M2 = {
    (1, 0): {"fila": 0, "count": 4},
    (-1, 0): {"fila": 64, "count": 4},
    (0, -1): {"fila": 128, "count": 4},
    (0, 1): {"fila": 192, "count": 4},
}

FRAME_CONFIG_DISTANCIA_M3 = {
    (1, 0): {"fila": 0, "count": 4},
    (-1, 0): {"fila": 48, "count": 4},
    (0, -1): {"fila": 96, "count": 4},
    (0, 1): {"fila": 144, "count": 4},
}


class EnemigoDistancia(Enemigos):
    def __init__(self, x, y, mundo=1 ,in_pos=[], listaEM=[], iniciado = 1):
        self.in_pos = in_pos
        self.listaEM = listaEM
        self.cooldown = 0
        self.intervalo = 2
        self.mundo = mundo
        self.iniciado = iniciado

        self.sprite_bala = AssetManager.get_image(
            "assets/sprites/bosses/proyectilCompleto.png"
        )

        self.sprite_bala = pygame.transform.scale(self.sprite_bala, (16, 16))

        if self.mundo == 3:
            config_usar = FRAME_CONFIG_DISTANCIA_M3
            ancho_frame = 48
            alto_frame = 48
        elif mundo == 2:
            config_usar = FRAME_CONFIG_DISTANCIA_M2
            ancho_frame = 64
            alto_frame = 64
        else:
            config_usar = FRAME_CONFIG_ENEMIGO
            ancho_frame = 32
            alto_frame = 32

        super().__init__(
            x,
            y,
            vida=2,
            velocidad=250,
            width=ancho_frame,
            heigth=alto_frame,
            color=(100, 0, 0),
            sprite_path=resource_path(
                f"assets/sprites/enemigo_distancia/distancia_mundo{mundo}.png"
            ),
            frame_config=config_usar,
            escala=1,
        )

    def update(self, dt, jugador):
        if self.iniciado == 2:
            self.t_carga = self.intervaloCarga
        self.t_carga += dt
        if self.t_carga > self.intervaloCarga:
            dx = jugador.x - self.x
            dy = jugador.y - self.y
            distancia = math.sqrt(dx**2 + dy**2)

            if distancia != 0:
                dx = dx / distancia
                dy = dy / distancia

            # Se aleja si está muy cerca, se acerca si está lejos
            if distancia <= 300:
                if self.x > 60 and self.x < 740:
                    self.x -= dx * dt * self.velocidad
                if self.y > 60 and self.y < 540:
                    self.y -= dy * dt * self.velocidad
            elif distancia >= 350:
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
                from escenas.workModules.audio_manager import AudioManager

                AudioManager.reproducir_sfx(f"distancia_mundo{self.mundo}")
                offset_disparo = (self.width / 2) + 10
                return Proyectil(
                    # self.x + 20 * dx,
                    # self.y + 20 * dy,
                    self.x + (offset_disparo * dx),
                    self.y + (offset_disparo * dy),
                    (dx, dy),
                    800,
                    1,
                    (0, 0, 200),
                    "enemigo",
                    self.sprite_bala,
                )

            self.actualizarRect()

    def destruir(self):
        if self.in_pos in self.listaEM:
            self.listaEM.remove(self.in_pos)
            from escenas.workModules.filtros import Filtros

            Filtros.quitarse_lista(self)
        self.kill()
        return self.listaEM
