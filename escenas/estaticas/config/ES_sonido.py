import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.workModules import Slider
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.filtros import Filtros
from escenas.UT_guardado import cargarProgreso, cargarConfig, guardarConfig
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager


class Sonido(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.config = cargarConfig()
        from escenas.workModules.audio_manager import AudioManager

        imagen_boton = AssetManager.get_image("assets/botones/botonrect1.png")
        imagen_boton = pygame.transform.scale(imagen_boton, (140, 48))

        self.slider_musica = Slider(
            x=370, y=215, ancho=200, alto=10, valor_inicial=AudioManager.volumen_musica
        )

        self.slider_sfx = Slider(
            x=370, y=270, ancho=200, alto=10, valor_inicial=AudioManager.volumen_sfx
        )

        self.ultimo_volumen_musica = self.slider_musica.valor
        self.ultimo_volumen_sfx = self.slider_sfx.valor

        self.fuente = pygame.font.Font(resource_path("assets/fonts/fuente.ttf"), 20)
        self.fuente_titulo = pygame.font.Font(
            resource_path("assets/fonts/fuente.ttf"), 50
        )

        self.escena_anterior = escena_anterior

        self.boton_texto = Boton(
            image=None,
            pos=(400, 100),
            text_input="AJUSTE DE VOLUMEN",
            font=self.fuente_titulo,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_musica = Boton(
            image=imagen_boton,
            pos=(290, 220),
            text_input="Música:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_sfx = Boton(
            image=imagen_boton,
            pos=(290, 275),
            text_input="SFX:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_regresar = Boton(
            image=imagen_boton,
            pos=(400, 350),
            text_input="Regresar",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_texto, self.boton_regresar, self.boton_sfx, self.boton_musica
        )

        self.botones_navegables = [
            self.boton_regresar,
        ]
        self.indice_seleccion = 0
        self.modo_teclado = False

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica(
            resource_path("assets/musica/naikan_main_theme.ogg")
        )

        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]

        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1

        ruta_fondo = f"assets/menuImages/menus/menu_principal{mundo_maximo}.png"

        self.fondo_original = AssetManager.get_image(ruta_fondo)
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))

        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def ejecutar_accion_boton(self, boton_presionado):
        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_sfx("click")

        if boton_presionado == self.boton_regresar:
            self.config["volumen_musica"] = self.slider_musica.valor
            self.config["volumen_sfx"] = self.slider_sfx.valor
            guardarConfig(self.config)
            return self.escena_anterior
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()

        self.slider_musica.HandleEvents(events)
        self.slider_sfx.HandleEvents(events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                self.modo_teclado = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for boton in self.botones_navegables:
                    if boton.checkForInput(mouse_pos):
                        return self.ejecutar_accion_boton(boton)

            if event.type == pygame.KEYDOWN:
                self.modo_teclado = True

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.indice_seleccion = (self.indice_seleccion + 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.indice_seleccion = (self.indice_seleccion - 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_RETURN:
                    boton_actual = self.botones_navegables[self.indice_seleccion]
                    return self.ejecutar_accion_boton(boton_actual)

        return self

    def Update(self, dt, keys):
        for boton in self.botones_navegables:
            boton.seleccionado_por_teclado = False

        if self.modo_teclado:
            boton_actual = self.botones_navegables[self.indice_seleccion]
            boton_actual.seleccionado_por_teclado = True

        self.grupo_botones.update(pygame.mouse.get_pos())
        self.slider_musica.Update()
        self.slider_sfx.Update()

        from escenas.workModules.audio_manager import AudioManager

        if self.slider_musica.valor != self.ultimo_volumen_musica:
            AudioManager.cambiar_volumen_musica(self.slider_musica.valor)
            self.ultimo_volumen_musica = self.slider_musica.valor

        if self.slider_sfx.valor != self.ultimo_volumen_sfx:
            AudioManager.cambiar_volumen_sfx(self.slider_sfx.valor)
            self.ultimo_volumen_sfx = self.slider_sfx.valor

        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)
        self.slider_musica.draw(screen)
        self.slider_sfx.draw(screen)
        pygame.display.flip()
        return self
