import pygame
from escenas.ES_base import EscenaBase
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.ME_boton import Boton
from escenas.workModules.filtros import Filtros
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager


class SeleccionMundo(EscenaBase):
    def __init__(self):
        super().__init__()
        self.progreso = cargarProgreso()
        self.mundos_desbloqueados = self.progreso["mundos_desbloqueados"]

        self.fuente = pygame.font.Font(resource_path("assets/fonts/fuente.ttf"), 25)

        self.fuente_pequeña = pygame.font.Font(
            resource_path("assets/fonts/fuente.ttf"), 15
        )

        m1Normal = AssetManager.get_image(
            "assets/menuImages/seleccion_mundo/1_norm.png"
        )

        m1Normal = pygame.transform.scale(m1Normal, (120, 120))
        m1Bloq = AssetManager.get_image("assets/menuImages/seleccion_mundo/1_bloq.png")

        m1Bloq = pygame.transform.scale(m1Bloq, (120, 120))

        m2Normal = AssetManager.get_image(
            "assets/menuImages/seleccion_mundo/2_norm.png"
        )

        m2Normal = pygame.transform.scale(m2Normal, (120, 120))
        m2Bloq = AssetManager.get_image("assets/menuImages/seleccion_mundo/2_bloq.png")

        m2Bloq = pygame.transform.scale(m2Bloq, (120, 120))

        m3Normal = AssetManager.get_image(
            "assets/menuImages/seleccion_mundo/3_norm.png"
        )

        m3Normal = pygame.transform.scale(m3Normal, (120, 120))
        m3Bloq = AssetManager.get_image("assets/menuImages/seleccion_mundo/3_bloq.png")

        m3Bloq = pygame.transform.scale(m3Bloq, (120, 120))

        m4Normal = AssetManager.get_image(
            "assets/menuImages/seleccion_mundo/4_norm.png"
        )

        m4Normal = pygame.transform.scale(m4Normal, (120, 120))
        m4Bloq = AssetManager.get_image("assets/menuImages/seleccion_mundo/4_bloq.png")
        m4Bloq = pygame.transform.scale(m4Bloq, (120, 120))

        if 1 in self.mundos_desbloqueados:
            self.boton_mundo_1 = Boton(
                image=m1Normal,
                pos=(270, 215),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_mundo_1 = Boton(
                image=m1Bloq,
                pos=(270, 215),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        if 2 in self.mundos_desbloqueados:
            self.boton_mundo_2 = Boton(
                image=m2Normal,
                pos=(270, 385),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_mundo_2 = Boton(
                image=m2Bloq,
                pos=(270, 385),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        if 3 in self.mundos_desbloqueados:
            self.boton_mundo_3 = Boton(
                image=m3Normal,
                pos=(510, 215),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_mundo_3 = Boton(
                image=m3Bloq,
                pos=(510, 215),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        if 4 in self.mundos_desbloqueados:
            self.boton_mundo_4 = Boton(
                image=m4Normal,
                pos=(510, 385),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_mundo_4 = Boton(
                image=m4Bloq,
                pos=(510, 385),
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        imagen_regresar = pygame.Surface((100, 100)).convert()
        imagen_regresar.fill((255, 255, 255))
        imagen_regresar.set_alpha(0)

        self.boton_regresar = Boton(
            image=imagen_regresar,
            pos=(400, 525),
            text_input="",
            font=self.fuente,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            # self.boton_titulo,
            self.boton_mundo_1,
            self.boton_mundo_2,
            self.boton_mundo_3,
            self.boton_mundo_4,
            self.boton_regresar,
        )

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica(
            resource_path("assets/musica/naikan_main_theme.ogg")
        )

        ruta_fondo = "assets/menuImages/seleccion_mundo/cielo_estrellado.jpeg"
        self.fondo_original = AssetManager.get_image(ruta_fondo)
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))
        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def seleccionar(self, mundo_id):
        if mundo_id in self.progreso["mundos_desbloqueados"]:
            return SeleccionNivel(mundo_id)
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.boton_mundo_1.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager

                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(1)

                if self.boton_mundo_2.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager

                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(2)

                if self.boton_mundo_3.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager

                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(3)

                if self.boton_mundo_4.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager

                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(4)

                if self.boton_regresar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager

                    AudioManager.reproducir_sfx("click")
                    Filtros.quitarse_lista(self)
                    from escenas.estaticas import MainMenu

                    return MainMenu()

        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)

        texto_m1 = self.fuente.render("Mundo 1", True, (245, 240, 225))
        rect_m1 = texto_m1.get_rect(center=(270, 295))
        screen.blit(texto_m1, rect_m1)

        texto_m2 = self.fuente.render("Mundo 2", True, (245, 240, 225))
        rect_m2 = texto_m2.get_rect(center=(270, 465))
        screen.blit(texto_m2, rect_m2)

        texto_m3 = self.fuente.render("Mundo 3", True, (245, 240, 225))
        rect_m3 = texto_m3.get_rect(center=(510, 295))
        screen.blit(texto_m3, rect_m3)

        texto_m4 = self.fuente.render("Mundo 4", True, (245, 240, 225))
        rect_m4 = texto_m4.get_rect(center=(510, 465))
        screen.blit(texto_m4, rect_m4)

        mensaje_asami = self.fuente_pequeña.render(
            "Selecciona un mundo para seguir la aventura de Asami",
            True,
            (200, 200, 200),
        )
        rect_5 = mensaje_asami.get_rect(center=(400, 580))
        screen.blit(mensaje_asami, rect_5)

        pygame.display.flip()


class SeleccionNivel(EscenaBase):
    def __init__(self, mundo_id):
        super().__init__()
        self.mundo_id = mundo_id

        self.progreso = cargarProgreso()
        self.desbloqueados = self.progreso["niveles_desbloqueados"][str(self.mundo_id)]
        self.completados = self.progreso["niveles_completados"][str(self.mundo_id)]

        self.fuente_titulo = pygame.font.Font(
            resource_path("assets/fonts/fuente.ttf"), 60
        )
        self.fuente_regresar = pygame.font.Font(
            resource_path("assets/fonts/fuente.ttf"), 30
        )
        self.fuente = pygame.font.Font(None, 30)

        img_n1 = AssetManager.get_image("assets/menuImages/seleccion_nivel/nivel1.png")

        img_n1 = pygame.transform.scale(img_n1, (80, 80))
        img_n1_bloq = img_n1.copy()
        img_n1_bloq.fill((80, 80, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)

        img_n2 = AssetManager.get_image("assets/menuImages/seleccion_nivel/nivel2.png")

        img_n2 = pygame.transform.scale(img_n2, (80, 80))
        img_n2_bloq = img_n2.copy()
        img_n2_bloq.fill((80, 80, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)

        img_n3 = AssetManager.get_image("assets/menuImages/seleccion_nivel/nivel3.png")

        img_n3 = pygame.transform.scale(img_n3, (80, 80))
        img_n3_bloq = img_n3.copy()
        img_n3_bloq.fill((80, 80, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)

        img_n4 = AssetManager.get_image("assets/menuImages/seleccion_nivel/nivel4.png")

        img_n4 = pygame.transform.scale(img_n4, (80, 80))
        img_n4_bloq = img_n4.copy()
        img_n4_bloq.fill((80, 80, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)

        posiciones_mundos = {
            1: [(345, 295), (185, 420), (500, 415), (630, 245)],
            2: [(310, 260), (170, 330), (460, 460), (580, 300)],
            3: [(380, 240), (185, 310), (380, 445), (630, 355)],
            4: [(330, 160), (130, 340), (320, 420), (600, 420)],
        }

        posiciones_actuales = posiciones_mundos[self.mundo_id]

        self.pos_n1 = posiciones_actuales[0]
        self.pos_n2 = posiciones_actuales[1]
        self.pos_n3 = posiciones_actuales[2]
        self.pos_n4 = posiciones_actuales[3]

        if 1 in self.desbloqueados:
            self.boton_nivel_1 = Boton(
                image=img_n1,
                pos=self.pos_n1,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_nivel_1 = Boton(
                image=img_n1_bloq,
                pos=self.pos_n1,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        if 2 in self.desbloqueados:
            self.boton_nivel_2 = Boton(
                image=img_n2,
                pos=self.pos_n2,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_nivel_2 = Boton(
                image=img_n2_bloq,
                pos=self.pos_n2,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        if 3 in self.desbloqueados:
            self.boton_nivel_3 = Boton(
                image=img_n3,
                pos=self.pos_n3,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_nivel_3 = Boton(
                image=img_n3_bloq,
                pos=self.pos_n3,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        if 4 in self.desbloqueados:
            self.boton_nivel_4 = Boton(
                image=img_n4,
                pos=self.pos_n4,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )
        else:
            self.boton_nivel_4 = Boton(
                image=img_n4_bloq,
                pos=self.pos_n4,
                text_input="",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(0, 0, 0),
            )

        imagen_regresar = AssetManager.get_image(
            "assets/menuImages/seleccion_nivel/boton_regresar.png"
        )
        imagen_regresar = pygame.transform.scale(imagen_regresar, (140, 48))

        self.boton_regresar = Boton(
            image=imagen_regresar,
            pos=(400, 560),
            text_input="Regresar",
            font=self.fuente_regresar,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_nivel_1,
            self.boton_nivel_2,
            self.boton_nivel_3,
            self.boton_nivel_4,
            self.boton_regresar,
        )

        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")

        ruta_fondo = f"assets/menuImages/seleccion_nivel/mundo{self.mundo_id}.png"
        self.fondo_original = AssetManager.get_image(ruta_fondo)
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))
        self.fondo_filtrado = self.fondo_original.copy()

        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def seleccionar(self, nivel_id):
        if nivel_id in self.desbloqueados:
            from escenas.ES_dinamicas import EscenaJuego

            return EscenaJuego(numeroNivel=nivel_id, mundoActual=self.mundo_id)
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                from escenas.workModules.audio_manager import AudioManager

                mouse_pos = pygame.mouse.get_pos()
                if self.boton_nivel_1.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(1)
                if self.boton_nivel_2.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(2)
                if self.boton_nivel_3.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(3)
                if self.boton_nivel_4.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(4)
                if self.boton_regresar.checkForInput(mouse_pos):
                    AudioManager.reproducir_sfx("click")
                    Filtros.quitarse_lista(self)
                    return SeleccionMundo()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        self.grupo_botones.draw(screen)

        titulo = self.fuente_titulo.render(
            f"Mundo {self.mundo_id}", True, (245, 240, 225)
        )
        rect_titulo = titulo.get_rect(center=(400, 60))
        screen.blit(titulo, rect_titulo)

        pygame.display.flip()
