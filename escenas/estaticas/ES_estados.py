import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.ES_dinamicas import EscenaJuego
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.filtros import Filtros

class EndGame(EscenaBase):
    def __init__(self, numeroNivel, mundoActual):
        super().__init__()
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente = pygame.font.Font(None, 60)
        
        self.numeroNivel = numeroNivel
        self.mundoActual = mundoActual

        self.boton = Boton(
            image=None,
            pos=(400, 200),
            text_input="¡Ganaste!",
            font=self.fuente_titulo,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )
        self.boton_reiniciar = Boton(
            image=None,
            pos=(400, 320),
            text_input="Volver a Jugar",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_volver_menu = Boton(
            image=None,
            pos=(400, 390),
            text_input="Volver al Menú Principal",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton, self.boton_reiniciar, self.boton_volver_menu)
        
        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        """ progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]
        
        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1 """
            
        ruta_fondo = f'assets/menuImages/deadScreen.png'
        
        self.fondo_original = pygame.image.load(ruta_fondo).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))
        
        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)
        
    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(self.fondo_original, nuevo_filtro)

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_reiniciar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return EscenaJuego(self.numeroNivel, self.mundoActual)
                if self.boton_volver_menu.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.ES_menus import MainMenu
                    return MainMenu()
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self


class DeadScreen(EscenaBase):
    def __init__(self, numeroNivel, mundoActual):
        super().__init__()
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente = pygame.font.Font(None, 60)
        
        self.numeroNivel = numeroNivel
        self.mundoActual = mundoActual

        self.boton = Boton(
            image=None,
            pos=(400, 200),
            text_input="¡Moriste! GIT GUD",
            font=self.fuente_titulo,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )
        self.boton_reiniciar = Boton(
            image=None,
            pos=(400, 320),
            text_input="Volver a Jugar",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_volver_menu = Boton(
            image=None,
            pos=(400, 390),
            text_input="Volver al Menú Principal",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton, self.boton_reiniciar, self.boton_volver_menu)
        
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

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_reiniciar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return EscenaJuego(self.numeroNivel, self.mundoActual)
                if self.boton_volver_menu.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    from escenas.estaticas.ES_menus import MainMenu
                    return MainMenu()
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0,0))
        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self
