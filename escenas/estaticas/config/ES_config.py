import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.filtros import Filtros


class Configuracion(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.font = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 20)
        self.title_font = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 50)
        
        self.escena_anterior = escena_anterior

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 70),
            text_input="CONFIGURACIÓN",
            font=self.title_font,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225)
        )
        self.boton_sonido = Boton(
            image=None,
            pos=(400, 170),
            text_input="Sonido",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170)
        )
        self.boton_accesibilidad = Boton(
            image=None,
            pos=(400, 240),
            text_input="Accesibilidad",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170)
        )
        self.boton_pantalla = Boton(
            image=None,
            pos=(400, 310),
            text_input="Pantalla",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170)
        )
        self.boton_teclas = Boton(
            image=None,
            pos=(410, 380),
            text_input="Asignación de Teclas",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170)
        )
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 450),
            text_input="Regresar",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170)
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
        
        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]
        
        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1
            
        ruta_fondo = f'assets/menuImages/menu_principal{mundo_maximo}.png'
        
        self.fondo_original = pygame.image.load(ruta_fondo).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))
        
        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)
        
    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(self.fondo_original, nuevo_filtro)

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)
        pygame.display.flip()
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
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.config.ES_sonido import Sonido
                    return Sonido(self)
                if self.boton_accesibilidad.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.config.ES_accesibilidad import Accesibilidad
                    return Accesibilidad(self)
                if self.boton_pantalla.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.config.ES_pantalla import Pantalla
                    return Pantalla(self)
                if self.boton_teclas.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.config.ES_teclas import Teclas
                    return Teclas(self)
                if self.boton_regresar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    if self.escena_anterior is not None:
                        return self.escena_anterior
                    else:
                        from escenas import MainMenu
                        return MainMenu()
                    """ from escenas.estaticas.ES_menus import MainMenu
                    return MainMenu() """
        return self
