import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.UT_guardado import cargarConfig, guardarConfig, cargarProgreso
from escenas.workModules.filtros import Filtros


class Pantalla(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.configuracion = cargarConfig()
        self.fuente = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 20)
        self.fuente_titulo = pygame.font.Font(
            "assets/fonts/DotGothic16-Regular.ttf", 50
        )

        self.escena_anterior = escena_anterior

        imagen_boton = pygame.image.load(
            "assets/botones/botonrect1.png"
        ).convert_alpha()

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 100),
            text_input="MODO PANTALLA",
            font=self.fuente_titulo,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_completa = Boton(
            image=imagen_boton,
            pos=(400, 220),
            text_input="Fullscreen",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_ventana = Boton(
            image=imagen_boton,
            pos=(400, 275),
            text_input="Modo Ventana",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_regresar = Boton(
            image=imagen_boton,
            pos=(400, 330),
            text_input="Regresar",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group(
            self.boton_titulo,
            self.boton_completa,
            self.boton_ventana,
            self.boton_regresar,
        )

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")

        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]

        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1

        ruta_fondo = f"assets/menuImages/menu_principal{mundo_maximo}.png"

        self.fondo_original = pygame.image.load(ruta_fondo).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))

        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                from escenas.workModules.audio_manager import AudioManager

                if self.boton_completa.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    self.configuracion["pantalla_completa"] = True
                    guardarConfig(self.configuracion)
                if self.boton_ventana.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    self.configuracion["pantalla_completa"] = False
                    guardarConfig(self.configuracion)
                if self.boton_regresar.checkForInput(mouse_pos):

                    AudioManager.reproducir_sfx("click")
                    return self.escena_anterior
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))

        estado = "Completa" if self.configuracion["pantalla_completa"] else "Ventana"
        texto_estado = self.fuente.render(
            f"Modo actual: {estado}", True, (255, 255, 255)
        )
        screen.blit(texto_estado, (300, 530))

        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self
