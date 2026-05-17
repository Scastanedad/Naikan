import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.workModules.filtros import Filtros
from escenas.UT_guardado import cargarConfig, guardarConfig, cargarProgreso


class Accesibilidad(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.font = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 20)
        self.font_title = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 50)

        self.escena_anterior = escena_anterior

        imagen_boton = pygame.image.load(
            "assets/botones/botonrect1.png"
        ).convert_alpha()

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 100),
            text_input="ACCESIBILIDAD",
            font=self.font_title,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_opcion_filtros = Boton(
            image=imagen_boton,
            pos=(400, 220),
            text_input="Filtros",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_regresar = Boton(
            image=imagen_boton,
            pos=(400, 275),
            text_input="Regresar",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_opcion_filtros, self.boton_regresar, self.boton_titulo
        )

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")

        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]

        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1

        ruta_fondo = f"assets/menuImages/menu_principal{mundo_maximo}.png"

        self.fondo_original = pygame.image.load(ruta_fondo).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))

        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
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
                from escenas.workModules.audio_manager import AudioManager

                if self.boton_opcion_filtros.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return Acc_FiltrosDaltonismo(self)
                if self.boton_regresar.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return self.escena_anterior
        return self


class Acc_FiltrosDaltonismo(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.font = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 20)
        self.font_title = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 50)

        self.escena_anterior = escena_anterior

        imagen_boton = pygame.image.load(
            "assets/botones/botonrect1.png"
        ).convert_alpha()

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 100),
            text_input="FILTROS",
            font=self.font_title,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_protanopia = Boton(
            image=imagen_boton,
            pos=(400, 220),
            text_input="Protanopia",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_deuteranopia = Boton(
            image=imagen_boton,
            pos=(400, 275),
            text_input="Deuteranopia",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_tritanopia = Boton(
            image=imagen_boton,
            pos=(400, 330),
            text_input="Tritanopia",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_ninguno = Boton(
            image=imagen_boton,
            pos=(400, 385),
            text_input="Ninguno",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_regresar = Boton(
            image=imagen_boton,
            pos=(400, 440),
            text_input="Regresar",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_titulo,
            self.boton_protanopia,
            self.boton_deuteranopia,
            self.boton_tritanopia,
            self.boton_ninguno,
            self.boton_regresar,
        )

        self.configuracion = cargarConfig()

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")

        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]

        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1

        ruta_fondo = f"assets/menuImages/menu_principal{mundo_maximo}.png"

        self.fondo_original = pygame.image.load(ruta_fondo).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))

        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))

        nombres = {
            "protanopia": "Protanopia",
            "deuteranopia": "Deuteranopia",
            "tritanopia": "Tritanopia",
            "ninguno": "Ninguno",
        }
        filtro = nombres.get(self.configuracion["filtro"], "Ninguno")
        texto_filtro = self.font.render(
            f"Filtro actual: {filtro}", True, (255, 255, 255)
        )
        screen.blit(texto_filtro, (300, 530))

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
                from escenas.workModules.audio_manager import AudioManager

                if self.boton_protanopia.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("protanopia")
                    self.configuracion["filtro"] = "protanopia"
                    guardarConfig(self.configuracion)
                if self.boton_deuteranopia.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("deuteranopia")
                    self.configuracion["filtro"] = "deuteranopia"
                    guardarConfig(self.configuracion)
                if self.boton_tritanopia.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("tritanopia")
                    self.configuracion["filtro"] = "tritanopia"
                    guardarConfig(self.configuracion)
                if self.boton_ninguno.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    Filtros.notificar_cambio("ninguno")
                    self.configuracion["filtro"] = "ninguno"
                    guardarConfig(self.configuracion)
                if self.boton_regresar.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    return self.escena_anterior
        return self
