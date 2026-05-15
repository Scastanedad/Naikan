import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.workModules.filtros import Filtros
from escenas.UT_guardado import cargarConfig, guardarConfig


class Accesibilidad(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.font_title = pygame.font.Font(None, 80)

        self.escena_anterior = escena_anterior
        
        self.boton_titulo = Boton(
            image=None,
            pos=(400, 70),
            text_input="ACCESIBILIDAD",
            font=self.font_title,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )
        self.boton_opcion_filtros = Boton(
            image=None,
            pos=(400, 170),
            text_input="Filtros",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 390),
            text_input="Regresar",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_opcion_filtros,
            self.boton_regresar,
            self.boton_titulo
        )
        
        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        self.fondo = pygame.image.load('assets/menuImages/menu_principal1.png').convert()
        self.fondo = pygame.transform.scale(self.fondo, (800, 600))

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        #screen.fill((0, 0, 0))
        screen.blit(self.fondo, (0, 0))
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_opcion_filtros.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return Acc_FiltrosDaltonismo(self)
                if self.boton_regresar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    #from escenas.estaticas.config.ES_config import Configuracion
                    return self.escena_anterior
        return self


class Acc_FiltrosDaltonismo(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.font_title = pygame.font.Font(None, 80)
        
        self.escena_anterior = escena_anterior

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 70),
            text_input="FILTROS",
            font=self.font_title,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )
        self.boton_protanopia = Boton(
            image=None,
            pos=(400, 170),
            text_input="Protanopia",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_deuteranopia = Boton(
            image=None,
            pos=(400, 240),
            text_input="Deuteranopia",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_tritanopia = Boton(
            image=None,
            pos=(400, 310),
            text_input="Tritanopia",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_ninguno = Boton(
            image=None,
            pos=(400, 380),
            text_input="Ninguno",
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
            self.boton_protanopia,
            self.boton_deuteranopia,
            self.boton_tritanopia,
            self.boton_ninguno,
            self.boton_regresar
        )

        self.configuracion = cargarConfig()
        
        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        self.fondo = pygame.image.load('assets/menuImages/menu_principal1.png').convert()
        self.fondo = pygame.transform.scale(self.fondo, (800, 600))

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        #screen.fill((0, 0, 0))
        screen.blit(self.fondo, (0, 0))

        nombres = {
            "protanopia": "Protanopia",
            "deuteranopia": "Deuteranopia",
            "tritanopia": "Tritanopia",
            "ninguno": "Ninguno"
        }
        filtro = nombres.get(self.configuracion["filtro"], "Ninguno")
        texto_filtro = self.font.render(f"Filtro actual: {filtro}", True, (255, 255, 255))
        screen.blit(texto_filtro, (180, 530))

        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_protanopia.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("protanopia")
                    self.configuracion["filtro"] = "protanopia"
                    guardarConfig(self.configuracion)
                if self.boton_deuteranopia.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("deuteranopia")
                    self.configuracion["filtro"] = "deuteranopia"
                    guardarConfig(self.configuracion)
                if self.boton_tritanopia.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("tritanopia")
                    self.configuracion["filtro"] = "tritanopia"
                    guardarConfig(self.configuracion)
                if self.boton_ninguno.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("ninguno")
                    self.configuracion["filtro"] = "ninguno"
                    guardarConfig(self.configuracion)
                if self.boton_regresar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return self.escena_anterior
        return self
