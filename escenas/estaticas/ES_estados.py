import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton


class EndGame(EscenaBase):
    def __init__(self):
        super().__init__()
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente = pygame.font.Font(None, 60)

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

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from escenas.ES_seleccion import SeleccionMundo
                    return SeleccionMundo()

            # ✅ FIXED: estaba anidado dentro del KEYDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_reiniciar.checkForInput(mouse_pos):
                    pass
                if self.boton_volver_menu.checkForInput(mouse_pos):
                    from escenas.estaticas.ES_menus import MainMenu
                    return MainMenu()
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.grupo_botones.draw(screen)
        return self


class DeadScreen(EscenaBase):
    def __init__(self):
        super().__init__()
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente = pygame.font.Font(None, 60)

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

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from escenas.estaticas.ES_menus import MainMenu
                    return MainMenu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_reiniciar.checkForInput(mouse_pos):
                    pass
                if self.boton_volver_menu.checkForInput(mouse_pos):
                    from escenas.estaticas.ES_menus import MainMenu
                    return MainMenu()
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.grupo_botones.draw(screen)
        return self
