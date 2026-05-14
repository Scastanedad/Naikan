import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton


class Configuracion(EscenaBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.title_font = pygame.font.Font(None, 80)

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 70),
            text_input="CONFIGURACIÓN",
            font=self.title_font,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )
        self.boton_sonido = Boton(
            image=None,
            pos=(400, 170),
            text_input="Sonido",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_accesibilidad = Boton(
            image=None,
            pos=(400, 240),
            text_input="Accesibilidad",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_pantalla = Boton(
            image=None,
            pos=(400, 310),
            text_input="Pantalla",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_teclas = Boton(
            image=None,
            pos=(410, 380),
            text_input="Asignación de Teclas",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 450),
            text_input="Regresar",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_titulo,
            self.boton_sonido,
            self.boton_accesibilidad,
            self.boton_pantalla,
            self.boton_teclas,
            self.boton_regresar
        )
        
        """ from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("ruta") """

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.grupo_botones.draw(screen)
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_sonido.checkForInput(mouse_pos):
                    from escenas.estaticas.config.ES_sonido import Sonido
                    return Sonido()
                if self.boton_accesibilidad.checkForInput(mouse_pos):
                    from escenas.estaticas.config.ES_accesibilidad import Accesibilidad
                    return Accesibilidad()
                if self.boton_pantalla.checkForInput(mouse_pos):
                    from escenas.estaticas.config.ES_pantalla import Pantalla
                    return Pantalla()
                if self.boton_teclas.checkForInput(mouse_pos):
                    from escenas.estaticas.config.ES_teclas import Teclas
                    return Teclas()
                if self.boton_regresar.checkForInput(mouse_pos):
                    from escenas.estaticas.ES_menus import MainMenu
                    return MainMenu()
        return self
