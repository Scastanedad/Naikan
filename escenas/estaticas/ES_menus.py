import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.workModules.icono import Icono
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.filtros import Filtros


class MainMenu(EscenaBase):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 20)
        self.font_title = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 80)

        imagen_logo = pygame.image.load(
            "assets/menuImages/logoNaikanResize.png"
        ).convert_alpha()
        imagen_logo = pygame.transform.smoothscale(imagen_logo, (350, 182))
        self.titulo_icono = Icono(400, 60, image=imagen_logo, pos="midtop")

        imagen_boton = pygame.image.load(
            "assets/botones/botonrect1.png"
        ).convert_alpha()
        imagen_rueda = pygame.image.load("assets/botones/botonengr.png").convert_alpha()
        imagen_rueda = pygame.transform.scale(imagen_rueda, (50, 50))

        self.play_button = Boton(
            image=imagen_boton,
            pos=(650, 340),
            text_input="Iniciar Juego",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.config_button = Boton(
            image=imagen_rueda,
            pos=(50, 550),
            text_input="",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.tutorial_button = Boton(
            image=imagen_boton,
            pos=(650, 395),
            text_input="Tutorial",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.quit_button = Boton(
            image=imagen_boton,
            pos=(650, 450),
            text_input="Salir",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.quit_button,
            self.config_button,
            self.tutorial_button,
            self.play_button,
        )

        self.grupo_iconos = pygame.sprite.GroupSingle()
        self.grupo_iconos.add(self.titulo_icono)

        self.botones_navegables = [
            self.play_button,
            self.tutorial_button,
            self.quit_button,
            self.config_button,
        ]
        self.indice_seleccion = 0
        self.modo_teclado = False

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

    def ejecutar_accion_boton(self, boton_presionado):
        from escenas.workModules.audio_manager import AudioManager
        from escenas.estaticas.config.ES_config import Configuracion
        from escenas.estaticas.ES_menus import (
            MainMenu,
        )

        AudioManager.reproducir_sfx("click")

        if boton_presionado == self.play_button:
            Filtros.quitarse_lista(self)
            from escenas.ES_seleccion import SeleccionMundo

            return SeleccionMundo()
        elif boton_presionado == self.tutorial_button:
            pass
        elif boton_presionado == self.quit_button:
            pygame.quit()
            sys.exit()
        elif boton_presionado == self.config_button:
            return Configuracion(self)

        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
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
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_iconos.draw(screen)
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self


class Menu_Pausa(EscenaBase):
    def __init__(self, escena_juego):
        super().__init__()

        self.escena_juego = escena_juego

        self.font = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 20)
        self.font_title = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 50)

        imagen_boton = pygame.image.load(
            "assets/botones/botonrect1.png"
        ).convert_alpha()
        imagen_rueda = pygame.image.load("assets/botones/botonengr.png").convert_alpha()
        imagen_rueda = pygame.transform.scale(imagen_rueda, (50, 50))

        self.title_button = Boton(
            image=None,
            pos=(400, 100),
            text_input="MENÚ DE PAUSA",
            font=self.font_title,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.reanudar_button = Boton(
            image=imagen_boton,
            pos=(400, 220),
            text_input="Reanudar",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.config_button = Boton(
            image=imagen_rueda,
            pos=(50, 550),
            text_input="",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.tutorial_button = Boton(
            image=imagen_boton,
            pos=(400, 275),
            text_input="Tutorial",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.quitMenu_button = Boton(
            image=imagen_boton,
            pos=(400, 330),
            text_input="Volver al Menú",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.title_button,
            self.quitMenu_button,
            self.config_button,
            self.tutorial_button,
            self.reanudar_button,
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

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                from escenas.workModules.audio_manager import AudioManager

                if self.reanudar_button.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return self.escena_juego
                if self.config_button.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.config.ES_config import Configuracion

                    return Configuracion(self)
                if self.tutorial_button.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    pass
                if self.quitMenu_button.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return MainMenu()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self
