import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.UT_guardado import cargarConfig, guardarConfig


class Teclas(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.configuracion = cargarConfig()
        self.fuente = pygame.font.Font(None, 60)
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_pequeno = pygame.font.Font(None, 20)
        self.accion_editando = None
        teclas = self.configuracion["teclas"]
        
        self.escena_anterior = escena_anterior

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 70),
            text_input="ASIGNACION TECLAS",
            font=self.fuente_titulo,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )

        self.boton_arriba = Boton(
            image=None,
            pos=(550, 150),
            text_input=pygame.key.name(teclas["arriba"]).upper(),
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_abajo = Boton(
            image=None,
            pos=(550, 220),
            text_input=pygame.key.name(teclas["abajo"]).upper(),
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_izquierda = Boton(
            image=None,
            pos=(550, 290),
            text_input=pygame.key.name(teclas["izquierda"]).upper(),
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )
        self.boton_derecha = Boton(
            image=None,
            pos=(550, 360),
            text_input=pygame.key.name(teclas["derecha"]).upper(),
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        mostrar_disparo = "L-CLICK" if teclas["disparo"] == 430 else pygame.key.name(teclas["disparo"]).upper()
        self.boton_disparo = Boton(
            image=None,
            pos=(550, 430),
            text_input=mostrar_disparo,
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.boton_arriba_texto = Boton(image=None, pos=(250, 135), text_input="ARRIBA:", font=self.fuente, base_color=(0, 255, 0), hovering_color=(0, 255, 0))
        self.boton_abajo_texto = Boton(image=None, pos=(250, 205), text_input="ABAJO:", font=self.fuente, base_color=(0, 255, 0), hovering_color=(0, 255, 0))
        self.boton_izquierda_texto = Boton(image=None, pos=(250, 275), text_input="IZQUIERDA:", font=self.fuente, base_color=(0, 255, 0), hovering_color=(0, 255, 0))
        self.boton_derecha_texto = Boton(image=None, pos=(250, 345), text_input="DERECHA:", font=self.fuente, base_color=(0, 255, 0), hovering_color=(0, 255, 0))
        self.boton_disparo_texto = Boton(image=None, pos=(250, 415), text_input="DISPARO:", font=self.fuente, base_color=(0, 255, 0), hovering_color=(0, 255, 0))

        self.boton_regresar = Boton(
            image=None,
            pos=(400, 530),
            text_input="Regresar",
            font=self.fuente,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group(
            self.boton_disparo_texto,
            self.boton_arriba_texto,
            self.boton_abajo_texto,
            self.boton_derecha_texto,
            self.boton_izquierda_texto,
            self.boton_titulo,
            self.boton_arriba,
            self.boton_abajo,
            self.boton_izquierda,
            self.boton_derecha,
            self.boton_disparo,
            self.boton_regresar
        )
        
        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        self.fondo = pygame.image.load('assets/menuImages/menu_principal1.png').convert()
        self.fondo = pygame.transform.scale(self.fondo, (800, 600))

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if self.accion_editando is not None:
                if event.type == pygame.KEYDOWN:
                    self.configuracion["teclas"][self.accion_editando] = event.key
                    guardarConfig(self.configuracion)
                    return Teclas(self.escena_anterior)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.accion_editando == "disparo" and event.button == 1:
                        self.configuracion["teclas"]["disparo"] = 430
                        guardarConfig(self.configuracion)
                        return Teclas(self.escena_anterior)
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_arriba.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    self.accion_editando = "arriba"
                if self.boton_abajo.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    self.accion_editando = "abajo"
                if self.boton_izquierda.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    self.accion_editando = "izquierda"
                if self.boton_derecha.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    self.accion_editando = "derecha"
                if self.boton_disparo.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    self.accion_editando = "disparo"
                if self.boton_regresar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    #from escenas.estaticas.config.ES_config import Configuracion
                    return self.escena_anterior
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        #screen.fill((0, 0, 0))
        screen.blit(self.fondo, (0, 0))

        if self.accion_editando:
            mensaje = f"Presiona la nueva tecla para {self.accion_editando.upper()}"
            texto = self.fuente_pequeno.render(mensaje, True, (255, 255, 255))
            screen.blit(texto, (50, 580))

        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self
