from habitaciones.H_base import Habitacion, Obstaculo, Gema
from habitaciones.H_colManager import ManejoColisiones
from entidades import Proyectil
from escenas.UT_guardado import cargarConfig
import pygame


class HabitacionMecanicas(Habitacion):
    def __init__(self, datos,mundo,iniciado):
        super().__init__(datos,mundo,iniciado)
        self.configuracion = cargarConfig()
        # Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json

    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        self.Proyectiles.update(dt)

        tecla_disparo = self.configuracion["teclas"]["disparo"]

        # teclas = self.configuracion["teclas"]

        if (keys[pygame.K_c]) and len(self.datos["TeclasOprimidas"][0]) == 0:
            self.datos["TeclasOprimidas"][0].append(1)

        """ if (keys[pygame.K_x])and len(self.datos["TeclasOprimidas"][1]) == 0:
            self.datos["TeclasOprimidas"][1].append(1) """

        disparo_activado = False

        if tecla_disparo == 430:
            mouse_botones = pygame.mouse.get_pressed()
            if mouse_botones[0]:
                disparo_activado = True
        else:
            if keys[tecla_disparo]:
                disparo_activado = True

        if disparo_activado and len(self.datos["TeclasOprimidas"][1]) == 0:
            self.datos["TeclasOprimidas"][1].append(1)

        if (self.datos["TeclasOprimidas"][0] == [1]) and (
            self.datos["TeclasOprimidas"][1] == [1]
        ):
            self.conexiones["derecha"] = 3
        # Para el miniBoss

    def draw(self, screen):
        self.Proyectiles.draw(screen)
