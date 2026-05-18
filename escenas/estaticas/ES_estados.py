import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.ES_dinamicas import EscenaJuego
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.filtros import Filtros
from escenas.workModules.icono import Icono
from G_utils import resource_path

class EndGame(EscenaBase):
    def __init__(self, numeroNivel, mundoActual):
        super().__init__()
        self.fuente_titulo = pygame.font.Font(
            resource_path("assets/fonts/DotGothic16-Regular.ttf"), 80
        )
        self.fuente = pygame.font.Font("assets/fonts/fuente.ttf", 20)

        self.numeroNivel = numeroNivel
        self.mundoActual = mundoActual

        if self.numeroNivel < 4:
            self.siguiente_nivel = self.numeroNivel + 1
            self.siguiente_mundo = self.mundoActual
        else:
            self.siguiente_nivel = 1
            self.siguiente_mundo = self.mundoActual + 1

        if self.mundoActual == 4 and self.numeroNivel == 4:
            self.endgame = True
        else:
            self.endgame = False

        self.boton_reiniciar = Boton(
            image=None,
            pos=(200, 570),
            text_input="Volver a Jugar",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_volver_menu = Boton(
            image=None,
            pos=(400, 570),
            text_input="Menú Principal",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.boton_siguiente = Boton(
            image=None,
            pos=(600, 570),
            text_input="Siguiente",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()

        if not self.endgame:
            self.grupo_botones.add(
                self.boton_reiniciar, self.boton_siguiente, self.boton_volver_menu
            )
            self.botones_navegables = [
                self.boton_reiniciar,
                self.boton_siguiente,
                self.boton_volver_menu,
            ]
        else:
            self.boton_reiniciar.rect.center = (280, 570)
            self.boton_volver_menu.rect.center = (480, 570)
            self.grupo_botones.add(self.boton_reiniciar, self.boton_volver_menu)
            self.botones_navegables = [self.boton_reiniciar, self.boton_volver_menu]

        self.indice_seleccion = 0
        self.modo_teclado = False

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica(resource_path("assets/musica/naikan_main_theme.ogg"))

        ruta_fondo = f"assets/menuImages/menus_estados/WinScreen.png"

        self.fondo_original = pygame.image.load(resource_path(ruta_fondo)).convert_alpha()
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
        from escenas.estaticas.ES_menus import MainMenu
        from escenas.ES_dinamicas import EscenaJuego
        from escenas.ES_tutorial import EscenaTutorial

        AudioManager.reproducir_sfx("click")

        if boton_presionado == self.boton_reiniciar:
            if self.numeroNivel == 0:
                return EscenaTutorial(numeroNivel=0, mundoActual=1)
            else:
                return EscenaJuego(self.numeroNivel, self.mundoActual)
        elif boton_presionado == self.boton_volver_menu:
            return MainMenu()
        elif boton_presionado == self.boton_siguiente:
            return EscenaJuego(self.siguiente_nivel, self.siguiente_mundo)
        return self

    def Update(self, dt, keys):
        for boton in self.grupo_botones:
            boton.seleccionado_por_teclado = False

        if self.modo_teclado:
            boton_actual = self.botones_navegables[self.indice_seleccion]
            boton_actual.seleccionado_por_teclado = True

        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.modo_teclado = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for boton in self.botones_navegables:
                    if boton.checkForInput(mouse_pos):
                        return self.ejecutar_accion_boton(boton)

            if event.type == pygame.KEYDOWN:
                self.modo_teclado = True

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.indice_seleccion = (self.indice_seleccion + 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.indice_seleccion = (self.indice_seleccion - 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_RETURN:
                    boton_actual = self.botones_navegables[self.indice_seleccion]
                    return self.ejecutar_accion_boton(boton_actual)

        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self


class DeadScreen(EscenaBase):
    def __init__(self, numeroNivel, mundoActual):
        super().__init__()
        self.fuente_titulo = pygame.font.Font(
           resource_path( "assets/fonts/DotGothic16-Regular.ttf"), 80
        )
        self.fuente = pygame.font.Font(resource_path("assets/fonts/DotGothic16-Regular.ttf"), 20)

        self.numeroNivel = numeroNivel
        self.mundoActual = mundoActual

        self.boton_reiniciar = Boton(
            image=None,
            pos=(280, 570),
            text_input="Volver a Jugar",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_volver_menu = Boton(
            image=None,
            pos=(480, 570),
            text_input="Menú Principal",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(  # self.boton
            self.boton_reiniciar, self.boton_volver_menu
        )

        self.botones_navegables = [self.boton_reiniciar, self.boton_volver_menu]
        self.indice_seleccion = 0
        self.modo_teclado = False

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica(resource_path("assets/musica/naikan_main_theme.ogg"))

        ruta_fondo = f"assets/menuImages/menus_estados/deadScreen.png"

        self.fondo_original = pygame.image.load(resource_path(ruta_fondo)).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))

        self.fondo_filtrado = self.fondo_original.copy()

        ruta_mensaje = "assets/menuImages/menus_estados/mensaje_moriste.png"
        imagen_mensaje = pygame.image.load(resource_path(ruta_mensaje)).convert_alpha()
        imagen_mensaje = pygame.transform.smoothscale(imagen_mensaje, (350, 182))
        self.icono_moriste = Icono(x=400, y=100, image=imagen_mensaje, pos="midtop")

        self.grupo_iconos = pygame.sprite.GroupSingle()
        self.grupo_iconos.add(self.icono_moriste)

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def ejecutar_accion_boton(self, boton_presionado):
        from escenas.workModules.audio_manager import AudioManager
        from escenas.estaticas.ES_menus import MainMenu
        from escenas.ES_tutorial import EscenaTutorial

        AudioManager.reproducir_sfx("click")

        if boton_presionado == self.boton_reiniciar:
            if self.numeroNivel == 0:
                return EscenaTutorial(numeroNivel=0, mundoActual=1)
            else:
                return EscenaJuego(self.numeroNivel, self.mundoActual)
        elif boton_presionado == self.boton_volver_menu:
            return MainMenu()
        return self

    def Update(self, dt, keys):
        for boton in self.grupo_botones:
            boton.seleccionado_por_teclado = False

        if self.modo_teclado:
            boton_actual = self.botones_navegables[self.indice_seleccion]
            boton_actual.seleccionado_por_teclado = True

        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.modo_teclado = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for boton in self.botones_navegables:
                    if boton.checkForInput(mouse_pos):
                        return self.ejecutar_accion_boton(boton)

            if event.type == pygame.KEYDOWN:
                self.modo_teclado = True

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.indice_seleccion = (self.indice_seleccion + 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.indice_seleccion = (self.indice_seleccion - 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_RETURN:
                    boton_actual = self.botones_navegables[self.indice_seleccion]
                    return self.ejecutar_accion_boton(boton_actual)

        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_iconos.draw(screen)
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self
