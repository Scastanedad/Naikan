from escenas.ES_base import EscenaBase
import sys, pygame

from escenas.workModules import Boton #type: ignore
from escenas.workModules import Slider
from escenas.UT_guardado import cargarConfig, guardarConfig
from escenas.workModules.filtros import Filtros

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

#Escena utilizada tras Morir
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
        
        self.boton_sonido = Boton(
            image=None,
            pos=(400, 100),
            text_input="Sonido",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_accesibilidad = Boton(
            image=None,
            pos=(400, 180),
            text_input="Accesibilidad",
            font=self.font, base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_pantalla = Boton(
            image=None,
            pos=(400, 260),
            text_input="Pantalla",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_teclas = Boton(
            image=None,
            pos=(400, 340),
            text_input="Asignación de Teclas",
            font=self.font, base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_regresar = Boton(image=None,
            pos=(400, 420),
            text_input="Regresar",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_sonido, self.boton_accesibilidad, self.boton_pantalla, self.boton_teclas, self.boton_regresar)
    
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

                if self.boton_pantalla.checkForInput(mouse_pos):
                    return Pantalla()
                    
                if self.boton_teclas.checkForInput(mouse_pos):
                    return Teclas()
                
                if self.boton_regresar.checkForInput(mouse_pos):
                    return MainMenu()
        return self
    
#Clase donde se accede al control del volumen del juego
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
        self.slider.Update() # type: ignore
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0)) 
        
        texto = self.fuente.render("Ajuste de Volumen", True, (0, 255, 0))
        screen.blit(texto, (220, 50))
        
        self.slider.draw(screen)
        return self

#clase para las opciones de accesibilidad, se podría quitar si solamente se alcanza a implemetar uno
class Accesibilidad(EscenaBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.boton_opcion_filtros = Boton(
            image = None,
            pos = (400, 100),
            text_input = "Filtros",
            font = self.font,
            base_color = (0,255,0),
            hovering_color = (255,255,255))
        
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 390), 
            text_input="Regresar",
            font=self.font, 
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_opcion_filtros, self.boton_regresar)
        
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
                elif self.boton_regresar.checkForInput(mouse_pos):
                    return Configuracion()
        return self
        
#clase para seleccionar los filtros de daltonismo
class Acc_FiltrosDaltonismo(EscenaBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.boton_protanopia = Boton(
            image=None, 
            pos=(400, 150),
            text_input="Protanopia",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_deuteranopia= Boton(
            image=None,
            pos=(400, 230),
            text_input="Deuteranopia",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_tritanopia = Boton(
            image=None,
            pos=(400, 310),
            text_input="Tritanopia",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 390), 
            text_input="Regresar",
            font=self.font, 
            base_color=(0,255,0),
            hovering_color=(255,255,255))
    
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_protanopia, self.boton_deuteranopia, self.boton_tritanopia, self.boton_regresar)
        
        self.configuracion = cargarConfig()
        
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
                    Filtros.notificar_cambio("protanopia")
                    self.configuracion["filtro"] = "protanopia"
                    guardarConfig(self.configuracion)
                elif self.boton_deuteranopia.checkForInput(mouse_pos):
                    Filtros.notificar_cambio("deuteranopia")
                    self.configuracion["filtro"] = "deuteranopia"
                    guardarConfig(self.configuracion)
                elif self.boton_tritanopia.checkForInput(mouse_pos):
                    Filtros.notificar_cambio("tritanopia")
                    self.configuracion["filtro"] = "tritanopia"
                    guardarConfig(self.configuracion)
                elif self.boton_regresar.checkForInput(mouse_pos):
                    return Accesibilidad()
        return self
    
#Clase para seleccionar el modo de presentación del juego
class Pantalla(EscenaBase):
    def __init__(self):
        super().__init__()
        self.configuracion = cargarConfig()
        self.fuente = pygame.font.Font(None, 60)
        
        self.boton_completa = Boton(
            image=None,
            pos=(400, 230),
            text_input="Pantalla Completa",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        
        self.boton_ventana = Boton(
            image=None,
            pos=(400, 330),
            text_input="Modo Ventana",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 500),
            text_input="Regresar",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        
        self.grupo_botones = pygame.sprite.Group(self.boton_completa, self.boton_ventana, self.boton_regresar)

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_completa.checkForInput(mouse_pos):
                    self.configuracion["pantalla_completa"] = True
                    guardarConfig(self.configuracion)
                
                elif self.boton_ventana.checkForInput(mouse_pos):
                    self.configuracion["pantalla_completa"] = False
                    guardarConfig(self.configuracion)
                
                elif self.boton_regresar.checkForInput(mouse_pos):
                    return Configuracion()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.configuracion["pantalla_completa"]:
            estado = "Completa" 
        else:
            estado = "Ventana"
            
        texto_estado = self.fuente.render(f"Modo actual: {estado}", True, (255, 255, 255))
        screen.blit(texto_estado, (180, 100))
        
        self.grupo_botones.draw(screen)

#Clase para asignar las teclas de movimiento y disparo
class Teclas(EscenaBase):
    def __init__(self):
        super().__init__()
        self.configuracion = cargarConfig()
        self.fuente = pygame.font.Font(None, 60)
        self.fuente_pequeno = pygame.font.Font(None, 20)
        self.accion_editando = None
        teclas = self.configuracion["teclas"]
        
        self.boton_arriba = Boton(
            image=None,
            pos =(550, 150), 
            text_input= pygame.key.name(teclas["arriba"]).upper(),
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255))
        
        self.boton_abajo = Boton(
            image=None,
            pos=(550, 220),
            text_input=pygame.key.name(teclas["abajo"]).upper(),
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255))
        
        self.boton_izquierda = Boton(
            image=None,
            pos=(550, 290),
            text_input=pygame.key.name(teclas["izquierda"]).upper(),
            font=self.fuente,
            base_color=(0, 255, 0), 
            hovering_color=(255, 255, 255))
        
        self.boton_derecha = Boton(
            image=None,
            pos=(550, 360),
            text_input=pygame.key.name(teclas["derecha"]).upper(), 
            font=self.fuente, 
            base_color=(0, 255, 0), 
            hovering_color=(255, 255, 255))
        
        if teclas["disparo"] == 430:
            mostrar_disparo = "L-CLICK"
        else:
            mostrar_disparo = pygame.key.name(teclas["disparo"]).upper()
            
        self.boton_disparo = Boton(
            image=None, 
            pos=(550, 430), 
            text_input=mostrar_disparo, 
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255))
        
        self.boton_regresar = Boton(
            image=None, 
            pos=(400, 530), 
            text_input="Regresar",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255))

        self.grupo_botones = pygame.sprite.Group(self.boton_arriba, self.boton_abajo, self.boton_izquierda, self.boton_derecha, self.boton_disparo, self.boton_regresar)

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if self.accion_editando is not None:
                if event.type == pygame.KEYDOWN:
                    self.configuracion["teclas"][self.accion_editando] = event.key
                    guardarConfig(self.configuracion)
                    return Teclas()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.accion_editando == "disparo" and event.button == 1:
                        self.configuracion["teclas"]["disparo"] = 430
                        guardarConfig(self.configuracion)
                        return Teclas()
                continue 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_arriba.checkForInput(mouse_pos):
                    self.accion_editando = "arriba"
                elif self.boton_abajo.checkForInput(mouse_pos):
                    self.accion_editando = "abajo"
                elif self.boton_izquierda.checkForInput(mouse_pos):
                    self.accion_editando = "izquierda"
                elif self.boton_derecha.checkForInput(mouse_pos):
                    self.accion_editando = "derecha"
                elif self.boton_disparo.checkForInput(mouse_pos):
                    self.accion_editando = "disparo"
                elif self.boton_regresar.checkForInput(mouse_pos):
                    return Configuracion()
                    
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))
        arriba = self.fuente.render("ARRIBA:", True, (0, 255, 0))
        screen.blit(arriba, (250, 135))
        abajo = self.fuente.render("ABAJO:", True, (0, 255, 0))
        screen.blit(abajo, (250, 205))
        izquierda = self.fuente.render("IZQUIERDA:", True, (0, 255, 0))
        screen.blit(izquierda, (250,275))
        derecha = self.fuente.render("DERECHA:", True, (0, 255, 0))
        screen.blit(derecha, (250, 345))
        disparo = self.fuente.render("DISPARO:", True, (0, 255, 0))
        screen.blit(disparo, (250, 415))

        if self.accion_editando:
            mensaje = f"Presiona la nueva tecla para {self.accion_editando.upper()}"
            fuente_pequeño = pygame.font.Font(None, 20)
            texto = self.fuente_pequeno.render(mensaje, True, (255, 255, 255))
            screen.blit(texto, (50, 50))
        
        self.grupo_botones.draw(screen)
    
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
