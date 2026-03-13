from escenas.ES_base import EscenaBase

import sys
import pygame

class MainMenu(EscenaBase):
    def __init__(self):
        self.posFlecha = self.HEIGTH//2 - 190
        super().__init__()

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.posFlecha == self.HEIGTH//2 - 190: 
                        from escenas.ES_dinamicas import EscenaJuego
                        return EscenaJuego()
                    if self.posFlecha == self.HEIGTH//2 - 90:
                        return self
                    if self.posFlecha == self.HEIGTH//2 +10:
                        pygame.quit()
                        sys.exit()

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if (self.posFlecha < self.HEIGTH//2 + 10):
                        self.posFlecha += 100
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.posFlecha > self.HEIGTH//2 - 190:
                        self.posFlecha -= 100

        return self
    #No necesariamente tiene que actualizarce nuestro menu
    def Update(self, dt, keys):
       
        return self
    def  draw(self, screen):
        #Menu principal
        screen.fill((0,0,0))
        texto = self.fuente.render("Iniciar Juego", True, (0,255,0))
        screen.blit(texto,(50,100))
        texto = self.fuente.render("Configuracion", True, (0,255,0))
        screen.blit(texto,(50,200))
        texto = self.fuente.render("Salir", True, (0,255,0))
        screen.blit(texto,(50,300))
        pygame.draw.rect(screen, ( 0,255,0), (200, self.posFlecha, 10, 2))

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