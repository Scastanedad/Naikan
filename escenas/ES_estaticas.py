from escenas.ES_base import EscenaBase

import sys
import pygame
class Boton:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        
        self.text = self.font.render(self.text_input, True, self.base_color)

        
        if self.image is None:
            self.image = self.text

        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))


    def update(self, screen):
        screen.blit(self.text, self.rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

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



    def HandleEvents(self, events):
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
        texto = self.fuente.render("Dale al enter para volver al menu", True, (0,255,0))
        screen.blit(texto,(200,300))
    

class Configuracion(EscenaBase):
    def __init__(self):
        super().__init__()
    
    def draw(self, screen):
        return super().draw(screen)
    
    def Update(self, dt, keys):
        return super().Update(dt, keys)
    
    def HandleEvents(self, events):
        return super().HandleEvents(events)