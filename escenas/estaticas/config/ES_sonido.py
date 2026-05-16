import sys
import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.workModules import Slider
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.filtros import Filtros
from escenas.UT_guardado import cargarProgreso, cargarConfig, guardarConfig



class Sonido(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.config = cargarConfig()
        from escenas.workModules.audio_manager import AudioManager
        self.slider_musica = Slider(
            x=395,
            y=195,
            ancho=200,
            alto=10,
            valor_inicial=AudioManager.volumen_musica
        )

        self.slider_sfx = Slider(
            x=365,
            y=275,
            ancho=200,
            alto=10,
            valor_inicial=AudioManager.volumen_sfx
        )

        self.ultimo_volumen_musica = self.slider_musica.valor
        self.ultimo_volumen_sfx = self.slider_sfx.valor
        
        self.fuente = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 20)
        self.fuente_titulo = pygame.font.Font("assets/fonts/DotGothic16-Regular.ttf", 50)
        
        self.escena_anterior = escena_anterior

        self.boton_texto = Boton(
            image=None,
            pos=(400, 70),
            text_input="AJUSTE DE VOLUMEN",
            font=self.fuente_titulo,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225)
        )
        self.boton_musica = Boton(
            image=None,
            pos=(300, 200),
            text_input="Música:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225)
        )
        self.boton_sfx = Boton(
            image=None,
            pos=(300, 280),
            text_input="SFX:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225)
        )
        self.boton_regresar = Boton(
            image=None,
            pos=(400, 400),
            text_input="Regresar",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_texto,
            self.boton_regresar,
            self.boton_sfx,
            self.boton_musica
        )
        
        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]
        
        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1
            
        ruta_fondo = f'assets/menuImages/menu_principal{mundo_maximo}.png'
        
        self.fondo_original = pygame.image.load(ruta_fondo).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))
        
        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)
        
    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(self.fondo_original, nuevo_filtro)

    def HandleEvents(self, events):
        self.slider_musica.HandleEvents(events)
        self.slider_sfx.HandleEvents(events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_regresar.checkForInput(pygame.mouse.get_pos()):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    #from escenas.estaticas.config.ES_config import Configuracion
                    self.config["volumen_musica"] = self.slider_musica.valor
                    self.config["volumen_sfx"] = self.slider_sfx.valor
                    guardarConfig(self.config)
                    return self.escena_anterior
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        self.slider_musica.Update()
        self.slider_sfx.Update()

        from escenas.workModules.audio_manager import AudioManager

        if self.slider_musica.valor != self.ultimo_volumen_musica:
            AudioManager.cambiar_volumen_musica(self.slider_musica.valor)
            self.ultimo_volumen_musica = self.slider_musica.valor

        if self.slider_sfx.valor != self.ultimo_volumen_sfx:
            AudioManager.cambiar_volumen_sfx(self.slider_sfx.valor)
            self.ultimo_volumen_sfx = self.slider_sfx.valor

        return self

    def draw(self, screen):
        #screen.fill((0, 0, 0))
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)
        self.slider_musica.draw(screen)
        self.slider_sfx.draw(screen)
        pygame.display.flip()
        return self
