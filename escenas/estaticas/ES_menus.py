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

        self.font = pygame.font.Font(None, 50)
        self.font_title = pygame.font.Font(None, 80)
        
        imagen_logo = pygame.image.load("assets/menuImages/logoNaikan.png").convert_alpha()
        self.titulo_icono = Icono(600, 120, image=imagen_logo, pos="midtop")

        """ self.title_button = Boton(
            image=None,
            pos=(400, 100),
            text_input="NAIKAN",
            font=self.font_title,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        ) """
        
        self.play_button = Boton(
            image=None,
            pos=(600, 260),
            text_input="Iniciar Juego",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        
        self.config_button = Boton(
            image=None,
            pos=(50, 550),
            text_input="C",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.tutorial_button = Boton(
            image=None,
            pos=(600, 360),
            text_input="Tutorial",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.quit_button = Boton(
            image=None,
            pos=(600, 460),
            text_input="Salir",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            #self.title_button,
            self.quit_button,
            self.config_button,
            self.tutorial_button,
            self.play_button
        )
        
        self.grupo_iconos = pygame.sprite.GroupSingle()
        self.grupo_iconos.add(self.titulo_icono)
        
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
        
        """ self.fondo = pygame.image.load('assets/menuImages/menu_principal.png').convert()
        self.fondo = pygame.transform.scale(self.fondo, (800, 600)) """
        
    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(self.fondo_original, nuevo_filtro)
        
        
    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    Filtros.quitarse_lista(self)
                    from escenas.ES_seleccion import SeleccionMundo
                    return SeleccionMundo()
                if self.config_button.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.config.ES_config import Configuracion
                    return Configuracion(self)
                if self.tutorial_button.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    pass
                if self.quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        #screen.fill((0, 0, 0))
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_iconos.draw(screen)
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self


class Menu_Pausa(EscenaBase):
    def __init__(self, escena_juego):
        super().__init__()

        self.escena_juego = escena_juego

        self.font = pygame.font.Font(None, 60)
        self.font_title = pygame.font.Font(None, 80)

        self.title_button = Boton(
            image=None,
            pos=(400, 100),
            text_input="MENÚ DE PAUSA",
            font=self.font_title,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )
        self.reanudar_button = Boton(
            image=None,
            pos=(400, 220),
            text_input="Reanudar",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.config_button = Boton(
            image=None,
            pos=(640, 530),
            text_input="C",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.tutorial_button = Boton(
            image=None,
            pos=(400, 320),
            text_input="Tutorial",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.quitMenu_button = Boton(
            image=None,
            pos=(400, 420),
            text_input="Volver al Menú",
            font=self.font,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.title_button,
            self.quitMenu_button,
            self.config_button,
            self.tutorial_button,
            self.reanudar_button
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
        
        self.fondo_original = pygame.image.load(ruta_fondo).get_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))
        
        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)
        
    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(self.fondo_original, nuevo_filtro)

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reanudar_button.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return self.escena_juego
                if self.config_button.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.config.ES_config import Configuracion
                    return Configuracion(self)
                if self.tutorial_button.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    pass
                if self.quitMenu_button.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
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
