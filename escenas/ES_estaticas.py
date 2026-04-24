from escenas.ES_base import EscenaBase
import sys, pygame
from escenas.assets.workModules import Boton
from escenas.assets.workModules import Slider

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

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.quit_button, self.config_button, self.play_button)

    def HandleEvents(self, events): # type: ignore
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    from escenas.ES_seleccion import SeleccionMundo  
                    return SeleccionMundo()                           
                if self.config_button.checkForInput(mouse_pos):
                    return Configuracion()
                if self.quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
        return self

    
    #No necesariamente tiene que actualizarce nuestro menu
    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self
    
    def  draw(self, screen):
        screen.fill((0,0,0))

        self.grupo_botones.draw(screen)
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
                    from escenas.ES_seleccion import SeleccionMundo  # <- CAMBIO
                    return SeleccionMundo()   
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
        
        self.font = pygame.font.Font(None, 60)
        
        self.boton_sonido = Boton(image=None, pos=(400, 100), text_input="Sonido", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        self.boton_accesibilidad = Boton(image=None, pos=(400, 180), text_input="Accesibilidad", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        self.boton_resolucion = Boton(image=None, pos=(400, 260), text_input="Resolución", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        self.boton_teclas = Boton(image=None, pos=(400, 340), text_input="Asignación de Teclas", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        self.boton_regresar = Boton(image=None, pos=(400, 420), text_input="Regresar", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_sonido, self.boton_accesibilidad, self.boton_resolucion, self.boton_teclas, self.boton_regresar)
    
    def draw(self, screen):
        screen.fill((0,0,0))

        self.grupo_botones.draw(screen)
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
                    return Sonido()

                if self.boton_accesibilidad.checkForInput(mouse_pos):
                    return Accesibilidad()

                if self.boton_resolucion.checkForInput(mouse_pos):
                    pass
                    
                if self.boton_teclas.checkForInput(mouse_pos):
                    pass
                
                if self.boton_regresar.checkForInput(mouse_pos):
                    return MainMenu()
        return self
    
class Sonido(EscenaBase):
    def __init__(self):
        super().__init__()
        self.slider = Slider(x=300, y=200, ancho=200, alto=10, valor_inicial=0.5)
        self.fuente = pygame.font.Font(None, 60)

    def HandleEvents(self, events):
        self.slider.HandleEvents(events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        return self

    def Update(self, dt, keys):
        self.slider.Update(pygame.mouse.get_pos()) # type: ignore
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0)) 
        
        texto = self.fuente.render("Ajuste de Volumen", True, (0, 255, 0))
        screen.blit(texto, (220, 50))
        
        self.slider.draw(screen)
        return self

class Accesibilidad(EscenaBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.boton_opcion_filtros = Boton(image = None, pos = (400, 100), text_input = "Filtros", font = self.font, base_color = (0,255,0), hovering_color = (255,255,255))
        
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_opcion_filtros)
        
    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        
        self.grupo_botones.draw(screen)
        return self
    
    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_opcion_filtros.checkForInput(mouse_pos):
                    return Acc_FiltrosDaltonismo()
        return self
        
        
class Acc_FiltrosDaltonismo(EscenaBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.boton_protanopia = Boton(image=None, pos=(400, 150), text_input="Protanopia", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        self.boton_deuteranopia= Boton(image=None, pos=(400, 230), text_input="Deuteranopia", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        self.boton_tritanopia = Boton(image=None, pos=(400, 310), text_input="Tritanopia", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
        self.boton_regresar = Boton(image=None, pos=(400, 390), text_input="Regresar", font=self.font, base_color=(0,255,0), hovering_color=(255,255,255))
    
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_protanopia, self.boton_deuteranopia, self.boton_tritanopia, self.boton_regresar)
        
    def Update(self, dt,keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self
    
    def draw (self, screen):
        screen.fill((0,0,0))
        texto = self.font.render("Filtros de Daltonismo", True, (0, 255, 0))
        screen.blit(texto, (180, 50))
        
        self.grupo_botones.draw(screen)
        
        return self
    
    def HandleEvents(self, events):
        
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_protanopia.checkForInput(mouse_pos):
                    pass
                elif self.boton_deuteranopia.checkForInput(mouse_pos):
                    pass
                elif self.boton_tritanopia.checkForInput(mouse_pos):
                    pass
        return self
class Resolucion(EscenaBase):
    pass

class Teclas(EscenaBase):
    pass
    
class SeleccionMundo(EscenaBase):
    def __init__(self):
        super().__init__()
    
    def draw(self, screen):
        return super().draw(screen)
    
    def Update(self, dt, keys):
        return super().Update(dt, keys)
    
    def HandleEvents(self, events):
        return super().HandleEvents(events)

class SeleccionNivel(EscenaBase):
    pass
