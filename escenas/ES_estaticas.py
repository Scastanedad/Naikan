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
        self.font_title= pygame.font.Font(None, 80)

        self.title_button = Boton(
          image=None,
          pos=(400, 100),
          text_input="NAIKAN",
          font=self.font_title,
          base_color=(0,255,0),
          hovering_color=(0,255,0)
        )
        self.play_button = Boton(
          image=None,
          pos=(400, 220),
          text_input="Iniciar Juego",
          font=self.font,
          base_color=(0,255,0),
          hovering_color=(255,255,255)
        )
        self.config_button = Boton(
            image=None,
            pos=(640, 530),
            text_input="C",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
        self.tutorial_button = Boton(
            image=None,
            pos=(400, 320),
            text_input="Tutorial",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
        self.quit_button = Boton(
            image=None,
            pos=(400, 420),
            text_input="Salir",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.title_button, self.quit_button, self.config_button, self.tutorial_button, self.play_button)

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
                if self.tutorial_button.checkForInput(mouse_pos):
                    pass
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
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente = pygame.font.Font(None, 60)
        
        self.boton = Boton(
            image=None,
            pos=(400, 200),
            text_input="¡Ganaste!",
            font=self.fuente_titulo,
            base_color=(0,255,0),
            hovering_color=(0,255,0)
        )
        
        self.boton_reiniciar = Boton(
            image=None,
            pos=(400, 320),
            text_input="Volver a Jugar",
            font=self.fuente,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
        
        self.boton_volver_menu = Boton(
            image=None,
            pos=(400, 390),
            text_input="Volver al Menú Principal",
            font=self.fuente,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
    
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton, self.boton_reiniciar, self.boton_volver_menu)
        
    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from escenas.ES_seleccion import SeleccionMundo  # <- CAMBIO
                    return SeleccionMundo()   

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_reiniciar.checkForInput(pygame.mouse.get_pos()):
                        pass                          
                    if self.boton_volver_menu.checkForInput(pygame.mouse.get_pos()):
                        return MainMenu()
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        self.grupo_botones.draw(screen)
        return self

#Escena utilizada tras Morir
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
            base_color=(0,255,0),
            hovering_color=(0,255,0)
        )
        
        self.boton_reiniciar = Boton(
            image=None,
            pos=(400, 320),
            text_input="Volver a Jugar",
            font=self.fuente,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
        
        self.boton_volver_menu = Boton(
            image=None,
            pos=(400, 390),
            text_input="Volver al Menú Principal",
            font=self.fuente,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
    
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton, self.boton_reiniciar, self.boton_volver_menu)
    
    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return MainMenu()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_reiniciar.checkForInput(pygame.mouse.get_pos()):
                    pass                          
                if self.boton_volver_menu.checkForInput(pygame.mouse.get_pos()):
                    return MainMenu()
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))
        self.grupo_botones.draw(screen)
        return self

#Clase base para configuracion
class Configuracion(EscenaBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.title_font = pygame.font.Font(None, 80)
        
        self.boton_titulo = Boton(
            image=None,
            pos=(400, 70),
            text_input="CONFIGURACIÓN",
            font=self.title_font,
            base_color=(0,255,0),
            hovering_color=(0,255,0))
        
        self.boton_sonido = Boton(
            image=None,
            pos=(400, 170),
            text_input="Sonido",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_accesibilidad = Boton(
            image=None,
            pos=(400, 240),
            text_input="Accesibilidad",
            font=self.font, base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_pantalla = Boton(
            image=None,
            pos=(400, 310),
            text_input="Pantalla",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_teclas = Boton(
            image=None,
            pos=(410, 380),
            text_input="Asignación de Teclas",
            font=self.font, base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_regresar = Boton(image=None,
            pos=(400, 450),
            text_input="Regresar",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_titulo, self.boton_sonido, self.boton_accesibilidad, self.boton_pantalla, self.boton_teclas, self.boton_regresar)
    
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
        self.slider_musica = Slider(x=395, y=195, ancho=200, alto=10, valor_inicial=0.5)
        self.slider_sfx = Slider(x=365, y=275, ancho=200, alto=10, valor_inicial=0.5)
        self.fuente = pygame.font.Font(None, 60)
        self.fuente_titulo = pygame.font.Font(None, 80)
        
        self.boton_texto = Boton(image=None,
            pos=(400, 70),
            text_input="Ajuste de Volumen",
            font=self.fuente_titulo,
            base_color=(0,255,0),
            hovering_color=(0,255,0))
        
        self.boton_musica = Boton(image=None,
            pos=(300, 200),
            text_input="Música:",
            font=self.fuente,
            base_color=(0,255,0),
            hovering_color=(0,255,0))
        
        self.boton_sfx= Boton(image=None,
            pos=(300, 280),
            text_input="SFX:",
            font=self.fuente,
            base_color=(0,255,0),
            hovering_color=(0,255,0))
        
        self.boton_regresar = Boton(image=None,
            pos=(400, 400),
            text_input="Regresar",
            font=self.fuente,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_texto, self.boton_regresar, self.boton_sfx, self.boton_musica)

    def HandleEvents(self, events):
        self.slider_musica.HandleEvents(events)
        self.slider_sfx.HandleEvents(events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_regresar.checkForInput(pygame.mouse.get_pos()):
                    return MainMenu()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        self.slider_musica.Update() # type: ignore
        self.slider_sfx.Update()
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0)) 
        
        self.grupo_botones.draw(screen)
        self.slider_musica.draw(screen)
        self.slider_sfx.draw(screen)
        return self

#clase para las opciones de accesibilidad, se podría quitar si solamente se alcanza a implemetar uno
class Accesibilidad(EscenaBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.font_title = pygame.font.Font(None, 80)
        
        self.boton_titulo = Boton(
            image = None,
            pos = (400, 70),
            text_input = "ACCESIBILIDAD",
            font = self.font_title,
            base_color = (0,255,0),
            hovering_color = (0,255,0))
        
        self.boton_opcion_filtros = Boton(
            image = None,
            pos = (400, 170),
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
        self.grupo_botones.add(self.boton_opcion_filtros, self.boton_regresar, self.boton_titulo)
        
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
        self.font_title= pygame.font.Font(None, 80)
        
        self.boton_titulo = Boton(
            image = None,
            pos = (400, 70),
            text_input = "FILTROS",
            font = self.font_title,
            base_color = (0,255,0),
            hovering_color = (0,255,0))
        
        self.boton_protanopia = Boton(
            image=None, 
            pos=(400, 170),
            text_input="Protanopia",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_deuteranopia= Boton(
            image=None,
            pos=(400, 240),
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
        
        self.boton_ninguno = Boton(
            image=None,
            pos=(400, 380),
            text_input="Ninguno",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255))
        
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 450), 
            text_input="Regresar",
            font=self.font, 
            base_color=(0,255,0),
            hovering_color=(255,255,255))
    
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_titulo, self.boton_protanopia, self.boton_deuteranopia, self.boton_tritanopia, self.boton_ninguno, self.boton_regresar)
        
        self.configuracion = cargarConfig()
        
    def Update(self, dt,keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self
    
    def draw (self, screen):
        screen.fill((0,0,0))
        
        filtro = ""
        if self.configuracion["filtro"] == "protanopia":
            filtro = "Protanopia" 
        elif self.configuracion["filtro"] == "deuteranopia":
            filtro = "Deuteranopia"
        elif self.configuracion["filtro"] == "tritanopia":
            filtro = "Tritanopia"
        elif self.configuracion["filtro"] == "ninguno":
            filtro = "Ninguno"
            
        texto_filtro = self.font.render(f"Filtro actual: {filtro}", True, (255, 255, 255))
        screen.blit(texto_filtro, (180, 530))
        
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
                    Filtros.notificar_cambio("protanopia") #Se notifica del cambio a todos los objetos observadores y se hace el cambio
                    self.configuracion["filtro"] = "protanopia" #Se guarda la configuración
                    guardarConfig(self.configuracion)
                elif self.boton_deuteranopia.checkForInput(mouse_pos):
                    Filtros.notificar_cambio("deuteranopia")
                    self.configuracion["filtro"] = "deuteranopia"
                    guardarConfig(self.configuracion)
                elif self.boton_tritanopia.checkForInput(mouse_pos):
                    Filtros.notificar_cambio("tritanopia")
                    self.configuracion["filtro"] = "tritanopia"
                    guardarConfig(self.configuracion)
                elif self.boton_ninguno.checkForInput(mouse_pos):
                    Filtros.notificar_cambio("ninguno")
                    self.configuracion["filtro"] = "ninguno"
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
        self.fuente_titulo = pygame.font.Font(None, 80)
        
        self.boton_titulo = Boton(
            image = None,
            pos = (400, 70),
            text_input = "MODO PANTALLA",
            font = self.fuente_titulo,
            base_color = (0,255,0),
            hovering_color = (0,255,0))
        
        self.boton_completa = Boton(
            image=None,
            pos=(400, 180),
            text_input="Pantalla Completa",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        
        self.boton_ventana = Boton(
            image=None,
            pos=(400, 260),
            text_input="Modo Ventana",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 340),
            text_input="Regresar",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        
        self.grupo_botones = pygame.sprite.Group(self.boton_titulo, self.boton_completa, self.boton_ventana, self.boton_regresar)

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
        screen.blit(texto_estado, (180, 530))
        
        self.grupo_botones.draw(screen)

#Clase para asignar las teclas de movimiento y disparo
class Teclas(EscenaBase):
    def __init__(self):
        super().__init__()
        from escenas.workModules.filtros import Filtros
        self.configuracion = cargarConfig()
        self.fuente = pygame.font.Font(None, 60)
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_pequeno = pygame.font.Font(None, 20)
        self.accion_editando = None
        teclas = self.configuracion["teclas"]
        self.filtro = Filtros.filtro_actual
        
        self.boton_titulo = Boton(
            image = None,
            pos = (400, 70),
            text_input = "ASIGNACION TECLAS",
            font = self.fuente_titulo,
            base_color = (0,255,0),
            hovering_color = (0,255,0))
        
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
        
        self.boton_arriba_texto = Boton(
            image=None, 
            pos=(250, 135), 
            text_input="ARRIBA:", 
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0))
        
        self.boton_abajo_texto = Boton(
            image=None, 
            pos=(250, 205), 
            text_input="ABAJO:", 
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0))
        
        self.boton_izquierda_texto = Boton(
            image=None, 
            pos=(250, 275), 
            text_input="IZQUIERDA:", 
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0))
        
        self.boton_derecha_texto = Boton(
            image=None, 
            pos=(250, 345), 
            text_input="DERECHA:", 
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0))
        
        self.boton_disparo_texto = Boton(
            image=None, 
            pos=(250, 415), 
            text_input="DISPARO:", 
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0))
        
        self.boton_regresar = Boton(
            image=None, 
            pos=(400, 530), 
            text_input="Regresar",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255))

        self.grupo_botones = pygame.sprite.Group(self.boton_disparo_texto, self.boton_arriba_texto, self.boton_abajo_texto, self.boton_derecha_texto, self.boton_izquierda_texto, self.boton_titulo,self.boton_arriba, self.boton_abajo, self.boton_izquierda, self.boton_derecha, self.boton_disparo, self.boton_regresar)

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

        if self.accion_editando:
            from escenas.workModules.filtros import Filtros
            mensaje = f"Presiona la nueva tecla para {self.accion_editando.upper()}"
            self.fuente_pequeno = pygame.font.Font(None, 20)
            texto = self.fuente_pequeno.render(mensaje, True, (255, 255, 255))
            
            screen.blit(texto, (50, 580))
        
        self.grupo_botones.draw(screen)
        
        
class Menu_Pausa(EscenaBase):
    def __init__(self, escena_juego):
        super().__init__()
        
        self.escena_juego = escena_juego
        
        self.font = pygame.font.Font(None, 60)
        self.font_title= pygame.font.Font(None, 80)

        self.title_button = Boton(
          image=None,
          pos=(400, 100),
          text_input="MENÚ DE PAUSA",
          font=self.font_title,
          base_color=(0,255,0),
          hovering_color=(0,255,0)
        )
        self.reanudar_button = Boton(
          image=None,
          pos=(400, 220),
          text_input="Reanudar",
          font=self.font,
          base_color=(0,255,0),
          hovering_color=(255,255,255)
        )
        self.config_button = Boton(
            image=None,
            pos=(640, 530),
            text_input="C",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
        self.tutorial_button = Boton(
            image=None,
            pos=(400, 320),
            text_input="Tutorial",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )
        self.quitMenu_button = Boton(
            image=None,
            pos=(400, 420),
            text_input="Volver al Menú",
            font=self.font,
            base_color=(0,255,0),
            hovering_color=(255,255,255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.title_button, self.quitMenu_button, self.config_button, self.tutorial_button, self.reanudar_button)
        
    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reanudar_button.checkForInput(mouse_pos):
                    return self.escena_juego                           
                if self.config_button.checkForInput(mouse_pos):
                    return Configuracion()
                if self.tutorial_button.checkForInput(mouse_pos):
                    pass
                if self.quitMenu_button.checkForInput(mouse_pos):
                    return MainMenu()
        return self
        
    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self
    
    def draw(self, screen):
        screen.fill((0,0,0))

        self.grupo_botones.draw(screen)
        return self
    
class Tutorial(EscenaBase):
    def __init__(self):
        super().__init__()
        
    def HandleEvents(self, events):
        return super().HandleEvents(events)
    
    def Update(self, dt, keys):
        return super().Update(dt, keys)
    
    def draw(self, screen):
        return super().draw(screen)
