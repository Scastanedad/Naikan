from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee, EnemigoDistancia
from entidades.ET_general import Proyectil
import math, pygame, random

class Boss2(Enemigos):
    def __init__(self, x, y, in_pos):
        super().__init__(x, y, vida=15, velocidad=50, width=30, heigth=30, color=(200, 200, 100))
        self.cooldownP = 0
        self.cooldownSP = 0
        self.intervaloP = 1.5
        self.intervaloSP = 4

        self.coolDownR = 0
        self.intervaloR = 15   # tiempo fuera de pantalla
        self.coolDownD = 0
        self.intervaloD = 5    # tiempo dentro de pantalla

        self.estado = "fueraP"
        self.in_pos = in_pos
        self._fijar_posicion()  # posición fija al entrar, no cada frame

    def _fijar_posicion(self):
        match random.randint(1, 4):
            case 1: self.x, self.y = 200, 150
            case 2: self.x, self.y = 600, 150
            case 3: self.x, self.y = 200, 450
            case 4: self.x, self.y = 600, 450
        self.actualizarRect()

    def update(self, dt, jugador):
        eventos = []
        self.coolDownR += dt
        self.cooldownP += dt
        self.cooldownSP += dt

        # Dirección hacia el jugador (solo para proyectiles)
        dx = jugador.sprite.x - self.x
        dy = jugador.sprite.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)
        if distancia != 0:
            dx /= distancia
            dy /= distancia

        if self.coolDownR < self.intervaloR:
            # --- ESTADO: fuera de pantalla ---
            self.estado = "fueraP"

            # Proyectiles en posición aleatoria de la pantalla, sin depender del boss
            if self.cooldownP >= self.intervaloP:
                self.cooldownP = 0
                spawn_x = random.randint(50, 750)
                spawn_y = random.randint(50, 550)
                # Dirección desde el spawn hacia el jugador
                sdx = jugador.sprite.x - spawn_x
                sdy = jugador.sprite.y - spawn_y
                sdist = math.sqrt(sdx**2 + sdy**2)
                if sdist != 0:
                    sdx /= sdist
                    sdy /= sdist
                eventos.append(Proyectil(spawn_x, spawn_y, (sdx, sdy), 800, 2, dueño="Boss"))

            # Spawn de enemigos aleatorio
            if self.cooldownSP >= self.intervaloSP:
                self.cooldownSP = 0
                if random.randint(1, 2) == 1:
                    eventos.append(EnemigoMelee(self.x, self.y, 2, [self.x, self.y]))
                else:
                    eventos.append(EnemigoDistancia(self.x, self.y, 2, [self.x, self.y]))

        else:
            # --- ESTADO: dentro de pantalla ---
            if self.coolDownD < self.intervaloD:
                self.estado = "dentroP"
                self.coolDownD += dt
            else:
                # Termina el tiempo visible, resetea para volver a ocultarse
                self.estado = "fueraP"
                self.coolDownR = 0
                self.coolDownD = 0
                self._fijar_posicion()  # elige nueva esquina para la próxima aparición

        return eventos

    def draw(self, screen, color=(100, 0, 0)):
        if self.estado == "dentroP":
            pygame.draw.rect(
                screen, color,
                (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
            )
        elif self.estado == "fueraP":
            screen.fill((100, 100, 100))  # efecto visual de boss oculto

        for i in range(self.vida):
            pygame.draw.rect(screen, (0, 255, 0), (400 + 10 * i, 10, 5, 5))

    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)

    def destruir(self, BossD):
        self.recibirDaño(1)
        if self.vida <= 0:
            BossD.remove(self)
            self.kill()