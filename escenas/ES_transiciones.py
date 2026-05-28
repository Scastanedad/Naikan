import pygame
from escenas.ES_base import EscenaBase
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager
from escenas.ES_dinamicas import CargarNivel
from escenas.workModules.filtros import Filtros
from escenas.workModules.audio_manager import AudioManager


class EscenaTransicion(EscenaBase):
    def __init__(self, mundo_id, nivel_id):
        super().__init__()
        self.mundo_id = mundo_id
        self.nivel_id = nivel_id

        if self.mundo_id == 5 and self.nivel_id == 1:
            self.modo = "cinematica"

            self.frames = [
                resource_path("assets/cinematicas/decoyf.jpeg"),
                resource_path("assets/cinematicas/decoyf.jpeg"),
                resource_path("assets/cinematicas/decoyf.jpeg"),
            ]
            self.indice_frame = 0
            self.cargar_frame_actual()
            Filtros.unirse_lista(self)

        else:
            self.datos_nivel = CargarNivel(self.nivel_id, self.mundo_id)
            self.condicion_victoria = self.datos_nivel["cond_victoria"]

            if self.nivel_id == 1:
                self.modo = "cinematica"
                self.frames = self.obtener_frames_cinematica(
                    self.mundo_id, self.nivel_id
                )
                self.indice_frame = 0
                self.cargar_frame_actual()
            else:
                self.modo = "carga"
                self.texto_objetivo = self.obtener_objetivo(self.condicion_victoria)
                self.tiempo_transcurrido = 0
                self.tiempo_espera = 4

                self.fuente_titulo = pygame.font.Font(
                    resource_path("assets/fonts/fuente.ttf"), 50
                )
                self.fuente_texto = pygame.font.Font(
                    resource_path("assets/fonts/fuente.ttf"), 30
                )

                self.fondo_carga_original = AssetManager.get_image(
                    f"assets/menuImages/menus/menu_principal{self.mundo_id}.png"
                )
                self.fondo_carga = pygame.transform.scale(
                    self.fondo_carga_original, (800, 600)
                )

            Filtros.unirse_lista(self)

            if self.modo == "cinematica":
                AudioManager.reproducir_musica(
                    resource_path("assets/musica/naikan_main_theme.ogg")
                )
            
    def configurar_filtro(self, nuevo_filtro):
        if self.modo == "carga":
            if hasattr(self, "fondo_carga_original"):
                fondo_filtrado = Filtros.aplicar_filtro(
                    self.fondo_carga_original, nuevo_filtro
                )
                self.fondo_carga = pygame.transform.scale(fondo_filtrado, (800, 600))

        elif self.modo == "cinematica":
            if hasattr(self, "imagen_actual_original"):
                imagen_filtrada = Filtros.aplicar_filtro(
                    self.imagen_actual_original, nuevo_filtro
                )
                self.imagen_actual = pygame.transform.scale(imagen_filtrada, (800, 600))

    def obtener_objetivo(self, condicion):
        if condicion == "MatarTodos":
            return "Elimina a todos los enemigos de la zona."

        elif condicion == "SobrevivirTiempo":
            return "Sobrevive hasta que el temporizador se agote."

        elif condicion == "Gema":
            return "Explora, encuentra y recoge la gema oculta."

        elif condicion == "MiniBoss":
            return "Enfréntate al poderoso Mini-Boss para avanzar."

        else:
            return "Prepárate para la batalla."

    def obtener_frames_cinematica(self, mundo_id, nivel_id):

        if mundo_id == 1 and nivel_id == 1:
            return [
                resource_path("assets/cinematicas/mundo1Inicio/1.png"),
                resource_path("assets/cinematicas/mundo1Inicio/2.png"),
                resource_path("assets/cinematicas/mundo1Inicio/3.png"),
                resource_path("assets/cinematicas/mundo1Inicio/4.png"),
                resource_path("assets/cinematicas/mundo1Inicio/5.png"),
                resource_path("assets/cinematicas/mundo1Inicio/6.png"),
                resource_path("assets/cinematicas/mundo1Inicio/7.png"),
                resource_path("assets/cinematicas/mundo1Inicio/8.png"),
                resource_path("assets/cinematicas/mundo1Inicio/9.png"),
                resource_path("assets/cinematicas/mundo1Inicio/10.png"),
                resource_path("assets/cinematicas/mundo1Inicio/11.png"),
                resource_path("assets/cinematicas/mundo1Inicio/12.png"),
                resource_path("assets/cinematicas/mundo1Inicio/13.png"),
                #resource_path("assets/cinematicas/mundo1Inicio/4.png"),
            ]

        elif mundo_id == 2 and nivel_id == 1:
            return [
                resource_path("assets/cinematicas/mundo1Final/1.png"),
                resource_path("assets/cinematicas/mundo1Final/2.png"),
                resource_path("assets/cinematicas/mundo1Final/3.png"),
                resource_path("assets/cinematicas/mundo1Final/4.png"),
                resource_path("assets/cinematicas/mundo2Inicio/1.png"),
                resource_path("assets/cinematicas/mundo2Inicio/2.png"),
                resource_path("assets/cinematicas/mundo2Inicio/3.png"),
                resource_path("assets/cinematicas/mundo2Inicio/4.jpeg"),
            ]

        elif mundo_id == 3 and nivel_id == 1:
            return [
                resource_path("assets/cinematicas/mundo2Final/1.jpeg"),
                resource_path("assets/cinematicas/mundo2Final/2.png"),
                resource_path("assets/cinematicas/mundo2Final/3.png"),
                resource_path("assets/cinematicas/mundo2Final/4.png"),
                resource_path("assets/cinematicas/mundo3Inicio/1.png"),
                resource_path("assets/cinematicas/mundo3Inicio/2.png"),
                resource_path("assets/cinematicas/mundo3Inicio/3.png"),
                resource_path("assets/cinematicas/mundo3Inicio/4.png"),
                resource_path("assets/cinematicas/mundo3Inicio/5.png"),
            ]

        elif mundo_id == 4 and nivel_id == 1:
            return [
                resource_path("assets/cinematicas/mundo3Final/1.png"),
                resource_path("assets/cinematicas/mundo3Final/2.png"),
                resource_path("assets/cinematicas/mundo3Final/3.png"),
                resource_path("assets/cinematicas/mundo4Inicio/1.png"),
                resource_path("assets/cinematicas/mundo4Inicio/2.png"),
                resource_path("assets/cinematicas/mundo4Inicio/3.png"),
                resource_path("assets/cinematicas/mundo4Inicio/4.png"),
                resource_path("assets/cinematicas/mundo4Inicio/5.png"),
            ]

        return [resource_path("assets/cinematicas/decoyf.jpeg")]

    def cargar_frame_actual(self):
        ruta_img = self.frames[self.indice_frame]

        self.imagen_actual_original = AssetManager.get_image(ruta_img)
        self.imagen_actual = pygame.transform.scale(
            self.imagen_actual_original, (800, 600)
        )

    def HandleEvents(self, events):
        for event in events:
            if self.modo == "cinematica":
                if event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN
                    and event.key in [pygame.K_RETURN, pygame.K_SPACE]
                ):

                    self.indice_frame += 1

                    if self.indice_frame >= len(self.frames):
                        Filtros.quitarse_lista(self)

                        if self.mundo_id == 5 and self.nivel_id == 1:
                            from escenas.estaticas.ES_menus import MainMenu

                            return MainMenu()

                        from escenas.ES_dinamicas import EscenaJuego

                        return EscenaJuego(
                            numeroNivel=self.nivel_id,
                            mundoActual=self.mundo_id,
                            currentData=self.datos_nivel,
                        )
                    else:
                        self.cargar_frame_actual()

        return self

    def Update(self, dt, keys):
        if self.modo == "carga":
            self.tiempo_transcurrido += dt

            if self.tiempo_transcurrido >= self.tiempo_espera:
                Filtros.quitarse_lista(self)
                from escenas.ES_dinamicas import EscenaJuego

                return EscenaJuego(
                    numeroNivel=self.nivel_id,
                    mundoActual=self.mundo_id,
                    currentData=self.datos_nivel,
                )
        return self

    def draw(self, screen):

        if self.modo == "carga":
            screen.blit(self.fondo_carga, (0, 0))

            titulo = self.fuente_titulo.render(
                f"Mundo {self.mundo_id} - Nivel {self.nivel_id}", True, (255, 255, 255)
            )
            rect_titulo = titulo.get_rect(center=(400, 200))
            screen.blit(titulo, rect_titulo)

            obj_render = self.fuente_texto.render(
                f"Objetivo: {self.texto_objetivo}", True, (255, 255, 255)
            )
            rect_obj = obj_render.get_rect(center=(400, 300))
            screen.blit(obj_render, rect_obj)

            if int(self.tiempo_transcurrido * 2) % 2 == 0:
                cargando = self.fuente_texto.render(
                    "Cargando...", True, (255, 255, 255)
                )
                screen.blit(cargando, cargando.get_rect(center=(400, 500)))

        elif self.modo == "cinematica":
            screen.blit(self.imagen_actual, (0, 0))

            # 230, 150, 170

        pygame.display.flip()
