import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.UT_guardado import cargarConfig, guardarConfig


class Pantalla(EscenaBase):
    def __init__(self):
        super().__init__()
        self.configuracion = cargarConfig()
        self.fuente = pygame.font.Font(None, 60)
        self.fuente_titulo = pygame.font.Font(None, 80)

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 70),
            text_input="MODO PANTALLA",
            font=self.fuente_titulo,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )
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

        self.grupo_botones = pygame.sprite.Group(
            self.boton_titulo,
            self.boton_completa,
            self.boton_ventana,
            self.boton_regresar
        )
        
        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")

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
                    from escenas.estaticas.config.ES_config import Configuracion
                    return Configuracion()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))

        estado = "Completa" if self.configuracion["pantalla_completa"] else "Ventana"
        texto_estado = self.fuente.render(f"Modo actual: {estado}", True, (255, 255, 255))
        screen.blit(texto_estado, (180, 530))

        self.grupo_botones.draw(screen)
        return self  # ✅ FIXED: faltaba el return self
