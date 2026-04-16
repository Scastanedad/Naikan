from escenas.ES_base import EscenaBase
import sys, pygame
from escenas.assets.workModules import Boton

#Clase que muestra el menu principal
class MainMenu(EscenaBase):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font(None, 60)

        self.play_button = Boton(
          image=None,
          pos=(400, 200),
          text_input="Iniciar Juego",
          font=self.font,
          base_color=(0,255,0),
          hovering_color=(255,255,255)
        )
        self.config_button = Boton(
              image=None,
              pos=(400, 300),
              text_input="Configuracion",
              font=self.font,
              base_color=(0,255,0),
              hovering_color=(255,255,255)
        )
        self.quit_button = Boton(
              image=None,
              pos=(400, 400),
              text_input="Salir",
              font=self.font,
              base_color=(0,255,0),
              hovering_color=(255,255,255)
        )



    def HandleEvents(self, events): # type: ignore
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    from escenas.ES_dinamicas import EscenaJuego
                    return EscenaJuego()

                if self.config_button.checkForInput(mouse_pos):
                    return Configuracion()

                if self.quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
        #Aqui empieza la flecha que se mueve por el menu
        #self.posFlecha = self.HEIGTH//2 - 190
        #super().__init__()
        return self

    
    #No necesariamente tiene que actualizarce nuestro menu
    def Update(self, dt, keys):
       
        return self
    def  draw(self, screen):
        screen.fill((0,0,0))

        mouse_pos = pygame.mouse.get_pos()

        # Hover effect
        self.play_button.changeColor(mouse_pos)
        self.config_button.changeColor(mouse_pos)
        self.quit_button.changeColor(mouse_pos)

        # Dibujar botones
        self.play_button.update(screen)
        self.config_button.update(screen)
        self.quit_button.update(screen)
        return self

#Escena utilizada tras Ganar
class EndGame(EscenaBase):
    def __init__(self):
        super().__init__()
    
    def Update(self, dt, keys):
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return MainMenu()
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        texto = self.fuente.render("Ganaste!", True, (0,255,0))
        screen.blit(texto,(200,300))
        return self

class DeadScreen(EscenaBase):
    def __init__(self):
        super().__init__()
    
    def Update(self, dt, keys):
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return MainMenu()
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        texto = self.fuente.render("Moriste! :((  Lol que mal jejejj", True, (0,255,0))
        screen.blit(texto,(200,300))
        return self

#Clase base para configuracion
class Configuracion(EscenaBase):
    def __init__(self):
        super().__init__()
    
    def draw(self, screen):
        return super().draw(screen)
    
    def Update(self, dt, keys):
        return super().Update(dt, keys)
    
    def HandleEvents(self, events):
        return super().HandleEvents(events)