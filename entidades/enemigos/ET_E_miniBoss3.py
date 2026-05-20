from entidades.enemigos.ET_E_base import Enemigos, FRAME_CONFIG_ENEMIGO
from entidades.ET_general import Proyectil
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager
from escenas.workModules.icono import Icono
import math
import pygame

FRAME_CONFIG_miniBOSS3 = {
    (1, 0): {"fila": 0, "count": 4},
    (-1, 0): {"fila": 64, "count": 4},
    (0, -1): {"fila": 128, "count": 4},
    (0, 1): {"fila": 192, "count": 4},
}


class miniBoss3(Enemigos):
    def __init__(self, x, y, in_pos):
            super().__init__(
                x,
                y,
                vida=20,
                velocidad=50,
                width=64,
                heigth=64,
                color=(200, 200, 100),
                sprite_path=resource_path("assets/sprites/minibosses/miniboss_mundo3.png"),
                frame_config=FRAME_CONFIG_miniBOSS3,
                escala=2,
            )
            self.in_pos = in_pos
            self.vidaInicial = 15
            self.cooldown = 0
            self.intervalo = 2
            self.sprite_bala = AssetManager.get_image(
            "assets/sprites/bosses/proyectilCompleto.png"
        )
            imagen_corazon = AssetManager.get_image(
                "assets/sprites/bosses/corazon.png"
            ).convert_alpha()
            imagen_corazon = pygame.transform.smoothscale(imagen_corazon, (25, 25))
            self.icono_corazon = Icono(0, 0, imagen_corazon)


    def update(self, dt, jugador):

        dx = jugador.sprite.x - self.x
        dy = jugador.sprite.y - self.y
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
        self.animar(dt)  

        self.cooldown += dt
        if self.cooldown >= self.intervalo:
            self.cooldown = 0
            self.actualizarRect()
            from escenas.workModules.audio_manager import AudioManager
            offset_disparo = (self.width / 2) + 10
            return Proyectil(
                # self.x + 20 * dx,
                # self.y + 20 * dy,
                self.x + (offset_disparo * dx),
                self.y + (offset_disparo * dy),
                (dx, dy),
                800,
                2,
                (0, 0, 200),
                "enemigo",
                self.sprite_bala,
            )
        
    def draw(self, screen, color=(100, 0, 0)):
        # pygame.draw.rect(screen, color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
        screen.blit(self.image, self.rect)

        for i in range(self.vida):
            pos_x = 770
            pos_y = 100 + (30 * i)
            screen.blit(self.icono_corazon.image, (pos_x, pos_y))

        self.actualizarRect()

    def destruir(self,miniBossD):
        self.recibirDaño(1)
        if self.vida <= 0:
            miniBossD.remove(self)
            from escenas.workModules.filtros import Filtros

            Filtros.quitarse_lista(self)
            self.kill()
