import pygame

from escenas.ES_base import EscenaBase
from escenas.workModules import Boton
from escenas.UT_guardado import cargarConfig, guardarConfig, cargarProgreso
from escenas.workModules.filtros import Filtros


class Teclas(EscenaBase):
    def __init__(self, escena_anterior=None):
        super().__init__()
        self.configuracion = cargarConfig()
        self.fuente = pygame.font.Font("assets/fonts/fuente.ttf", 20)
        self.fuente_titulo = pygame.font.Font(
            "assets/fonts/fuente.ttf", 50
        )
        self.fuente_pequeno = pygame.font.Font(
            "assets/fonts/fuente.ttf", 10
        )
        self.accion_editando = None
        teclas = self.configuracion["teclas"]

        self.escena_anterior = escena_anterior

        imagen_boton = pygame.image.load(
            "assets/botones/botonrect1.png"
        ).convert_alpha()

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 100),
            text_input="ASIGNACION TECLAS",
            font=self.fuente_titulo,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )

        self.boton_arriba = Boton(
            image=None,
            pos=(510, 200),
            text_input=pygame.key.name(teclas["arriba"]).upper(),
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_abajo = Boton(
            image=None,
            pos=(510, 310),
            text_input=pygame.key.name(teclas["abajo"]).upper(),
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_izquierda = Boton(
            image=None,
            pos=(510, 255),
            text_input=pygame.key.name(teclas["izquierda"]).upper(),
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_derecha = Boton(
            image=None,
            pos=(510, 365),
            text_input=pygame.key.name(teclas["derecha"]).upper(),
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        mostrar_disparo = (
            "L-CLICK"
            if teclas["disparo"] == 430
            else pygame.key.name(teclas["disparo"]).upper()
        )
        self.boton_disparo = Boton(
            image=None,
            pos=(510, 420),
            text_input=mostrar_disparo,
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.boton_arriba_texto = Boton(
            image=imagen_boton,
            pos=(350, 200),
            text_input="ARRIBA:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_abajo_texto = Boton(
            image=imagen_boton,
            pos=(350, 310),
            text_input="ABAJO:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_izquierda_texto = Boton(
            image=imagen_boton,
            pos=(350, 255),
            text_input="IZQUIERDA:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_derecha_texto = Boton(
            image=imagen_boton,
            pos=(350, 365),
            text_input="DERECHA:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )
        self.boton_disparo_texto = Boton(
            image=imagen_boton,
            pos=(350, 420),
            text_input="DISPARO:",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(245, 240, 225),
        )

        self.boton_regresar = Boton(
            image=imagen_boton,
            pos=(400, 505),
            text_input="Regresar",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
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
            self.boton_regresar,
        )

        self.botones_navegables = [
            self.boton_arriba,
            self.boton_izquierda,
            self.boton_abajo,
            self.boton_derecha,
            self.boton_disparo,
            self.boton_regresar,
        ]
        self.indice_seleccion = 0
        self.modo_teclado = False

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")

        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]

        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1

        ruta_fondo = f"assets/menuImages/menus/menu_principal{mundo_maximo}.png"

        self.fondo_original = pygame.image.load(ruta_fondo).convert_alpha()
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))

        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def ejecutar_accion_boton(self, boton_presionado):
        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_sfx("click")

        if boton_presionado == self.boton_arriba:
            self.accion_editando = "arriba"
        elif boton_presionado == self.boton_izquierda:
            self.accion_editando = "izquierda"
        elif boton_presionado == self.boton_abajo:
            self.accion_editando = "abajo"
        elif boton_presionado == self.boton_derecha:
            self.accion_editando = "derecha"
        elif boton_presionado == self.boton_disparo:
            self.accion_editando = "disparo"
        elif boton_presionado == self.boton_regresar:
            return self.escena_anterior

        return self

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

            if event.type == pygame.MOUSEMOTION:
                self.modo_teclado = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for boton in self.botones_navegables:
                    if boton.checkForInput(mouse_pos):
                        return self.ejecutar_accion_boton(boton)

            if event.type == pygame.KEYDOWN:
                self.modo_teclado = True

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.indice_seleccion = (self.indice_seleccion + 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.indice_seleccion = (self.indice_seleccion - 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_RETURN:
                    boton_actual = self.botones_navegables[self.indice_seleccion]
                    return self.ejecutar_accion_boton(boton_actual)

        return self

    def Update(self, dt, keys):
        for boton in self.grupo_botones:
            boton.seleccionado_por_teclado = False

        if self.modo_teclado:
            boton_actual = self.botones_navegables[self.indice_seleccion]
            boton_actual.seleccionado_por_teclado = True

        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))

        if self.accion_editando:
            mensaje = f"Presiona la nueva tecla para {self.accion_editando.upper()}"
            texto = self.fuente_pequeno.render(mensaje, True, (255, 255, 255))
            screen.blit(texto, (50, 580))

        self.grupo_botones.draw(screen)
        pygame.display.flip()
        return self
