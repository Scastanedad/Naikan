import pygame
from escenas.ES_base import EscenaBase
from G_utils import resource_path
from escenas.workModules.ME_boton import Boton
from escenas.workModules.asset_manager import AssetManager
from escenas.workModules.filtros import Filtros
from escenas.UT_guardado import cargarProgreso

DATOS_GALERIA = {
    "asami": [
        (
            "assets/sprites/jugador/spriteJugador.png",
            32,
            32,
            0,
            96,
            "Asami",
            "La valiente protagonista de nuestra historia.\nEquipada con su espada, está lista para\nenfrentar la oscuridad.",
            6,
        )
    ],
    "mundo1": [
        (
            "assets/sprites/enemigo_melee/melee_mundo1.png",
            32,
            32,
            0,
            96,
            "Stalker",
            "Una figura misteriosa que persigue a Asami sin descanso. \nRepresenta el acoso que recibe Asami digitalmente",
            5,
        ),
        (
            "assets/sprites/enemigo_distancia/distancia_mundo1.png",
            32,
            32,
            0,
            96,
            "Spammer",
            "Figura humanoide con cara de pantalla.\nDispara mensajes de odio a Asami \nSimboliza el acoso hacia Asami en redes sociales.",
            5,
        ),
        (
            "assets/sprites/bosses/boss_mundo1.png",
            64,
            64,
            0,
            192,
            "The Hater",
            "Es la cuspide del ciberacoso hacia Asami. \nEs un ser grotesco con una apariencia mounstrosa.\nSimboliza a todos aquellos que acosaban a Asami diariamente.",
            4,
        ),
    ],
    "mundo2": [
        (
            "assets/sprites/enemigo_melee/melee_mundo2.png",
            48,
            48,
            0,
            144,
            "Runner",
            "Es un fan obsesionado con Asami que la persigue a pedirle fotos.\nTiene una sonrisa macabra y ojos brillantes que reflejan su obsesión enfermiza.\nSimboliza a los acosadores que perseguían a Asami en la vida real.",
            5,
        ),
        (
            "assets/sprites/enemigo_distancia/distancia_mundo2.png",
            64,
            64,
            0,
            192,
            "Critic",
            "Es una critica de moda que dispara a Asami palabras de odio por su apariencia.\nTiene un aspecto elegante pero su rostro está distorsionado por la ira y el desprecio.",
            5,
        ),
        (
            "assets/sprites/minibosses/miniboss_mundo2.png",
            64,
            64,
            0,
            192,
            "The Crowd",
            "Es una multitud de personas que atacan a Asami en conjunto.\nSimboliza a la sociedad que juzgaba constantemente a Asami por su apariencia y personalidad.",
            4,
        ),
        (
            "assets/sprites/bosses/boss2/cuerpo_fisico.png",
            128,
            128,
            0,
            0,
            "The Stage",
            "Una pantalla gigante que no se mueve y que ataca a Asami a distancia.\nSimboliza el escenario donde Asami era juzgada y acosada por su apariencia",
            4,
        ),
    ],
    "mundo3": [
        (
            "assets/sprites/enemigo_melee/melee_mundo3.png",
            64,
            64,
            0,
            192,
            "Guard",
            "Un guardia que patrulla el área.\nRepresenta las figuras que intentan proteger a Asami.\nAunque su intención es protegerla, a veces pueden ser una molestia para Asami.",
            5,
        ),
        (
            "assets/sprites/enemigo_distancia/distancia_mundo3.png",
            48,
            48,
            0,
            144,
            "Controller",
            "Son camisas lujosas flotantes que disparan hilos a Asami para intentar controlarla.\nSimboliza a las personas que intentaban controlar la vida de Asami.",
            5,
        ),
        (
            "assets/sprites/minibosses/miniboss_mundo3.png",
            64,
            64,
            0,
            192,
            "The Dual",
            "Dos entidades unidas entre si que atacan a Asami en conjunto.\nSimboliza la dualidad de la vida de Asami, donde por un lado tenía que lidiar con el acoso\n Por otro lado tenía que lidiar con las personas que intentaban protegerla.",
            4,
        ),
        (
            "assets/sprites/bosses/boss_mundo3.png",
            64,
            64,
            0,
            192,
            "The Manager",
            "Es una figura autoritaria que controlaba todo lo que hace Asami.\nSimboliza al manager de Asami que controlaba su vida y su carrera.\n Explota a Asami y no le permite tomar sus propias decisiones.",
            4,
        ),
    ],
    "mundo4": [
        (
            "assets/sprites/enemigo_melee/melee_mundo4.png",
            32,
            32,
            0,
            96,
            "Shadow",
            "Es una version de Asami negativa con apariencia oscura.\nSimboliza los miedos y traumas internos de Asami que la acechan constantemente.\nAunque no es un enemigo real, puede ser una gran amenaza para Asami si no lo enfrenta.",
            5,
        ),
        (
            "assets/sprites/enemigo_distancia/distancia_mundo4.png",
            32,
            32,
            0,
            96,
            "Doubt",
            "Es una nube negra que representa la duda y la incertidumbre de Asami.\nSimboliza las inseguridades y dudas que Asami tenía sobre si misma y su vida.\nAunque no es un enemigo real, puede ser una gran amenaza para Asami si no lo enfrenta.",
            5,
        ),
        (
            "assets/sprites/minibosses/miniboss_mundo4.png",
            64,
            64,
            0,
            192,
            "The Voice",
            "Es una máscara que ataca en todas las direcciones.\nSimboliza la voz interior de Asami que a veces puede ser muy crítica y negativa.",
            4,
        ),
        (
            "assets/sprites/bosses/boss4/fase1.png",
            32,
            32,
            0,
            96,
            "Evil Asami",
            "Es una version corrupta de Asami con apariencia de Glitch.\nSimboliza la parte mas oscura de Asami, donde sus miedos, traumas e inseguridades se han manifestado en una entidad propia.\nEs el enemigo mas peligroso de Asami, ya que representa todo lo que Asami teme y odia de si misma.",
            4,
        ),
    ],
}


class MenuGaleria(EscenaBase):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font(resource_path("assets/fonts/fuente.ttf"), 20)
        self.font_title = pygame.font.Font(resource_path("assets/fonts/fuente.ttf"), 80)

        imagen_boton = AssetManager.get_image("assets/botones/botonrect1.png")

        progreso = cargarProgreso()
        lista_mundos = progreso["mundos_desbloqueados"]
        niveles_completado = progreso["niveles_completados"]

        if len(lista_mundos) > 0:
            mundo_maximo = max(lista_mundos)
        else:
            mundo_maximo = 1

        ruta_fondo = f"assets/menuImages/menus/menu_principal{mundo_maximo}.png"

        if 4 in lista_mundos:
            niveles_mundo4 = niveles_completado.get("4", [])
            if 4 in niveles_mundo4:
                ruta_fondo = f"assets/menuImages/menus/menu_principal5.png"

        self.fondo_original = AssetManager.get_image(ruta_fondo)
        self.fondo_original = pygame.transform.scale(self.fondo_original, (800, 600))
        self.fondo_filtrado = self.fondo_original.copy()
        Filtros.unirse_lista(self)

        self.boton_asami = Boton(
            image=imagen_boton,
            pos=(400, 180),
            text_input="Asami",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_m1 = Boton(
            image=imagen_boton,
            pos=(400, 240),
            text_input="Mundo 1",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_m2 = Boton(
            image=imagen_boton,
            pos=(400, 300),
            text_input="Mundo 2",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_m3 = Boton(
            image=imagen_boton,
            pos=(400, 360),
            text_input="Mundo 3",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_m4 = Boton(
            image=imagen_boton,
            pos=(400, 420),
            text_input="Mundo 4",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_volver = Boton(
            image=imagen_boton,
            pos=(400, 520),
            text_input="Volver al Menú",
            font=self.font,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(
            self.boton_asami,
            self.boton_m1,
            self.boton_m2,
            self.boton_m3,
            self.boton_m4,
            self.boton_volver,
        )

        self.botones_navegables = [
            self.boton_asami,
            self.boton_m1,
            self.boton_m2,
            self.boton_m3,
            self.boton_m4,
            self.boton_volver,
        ]
        self.indice_seleccion = 0
        self.modo_teclado = False

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def ejecutar_accion_boton(self, boton_presionado):
        from escenas.workModules.audio_manager import AudioManager
        from escenas.estaticas.ES_menus import MainMenu

        AudioManager.reproducir_sfx("click")

        if boton_presionado == self.boton_asami:
            return VisorGaleria("asami")
        elif boton_presionado == self.boton_m1:
            return VisorGaleria("mundo1")
        elif boton_presionado == self.boton_m2:
            return VisorGaleria("mundo2")
        elif boton_presionado == self.boton_m3:
            return VisorGaleria("mundo3")
        elif boton_presionado == self.boton_m4:
            return VisorGaleria("mundo4")
        elif boton_presionado == self.boton_volver:
            Filtros.quitarse_lista(self)
            return MainMenu()
        return self

    def Update(self, dt, keys):
        for boton in self.grupo_botones:
            boton.seleccionado_por_teclado = False
        if self.modo_teclado:
            self.botones_navegables[self.indice_seleccion].seleccionado_por_teclado = (
                True
            )
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                self.modo_teclado = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for boton in self.botones_navegables:
                    if boton.checkForInput(mouse_pos):
                        return self.ejecutar_accion_boton(boton)
            if event.type == pygame.KEYDOWN:
                self.modo_teclado = True
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.indice_seleccion = (self.indice_seleccion + 1) % len(
                        self.botones_navegables
                    )
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    self.indice_seleccion = (self.indice_seleccion - 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_RETURN:
                    return self.ejecutar_accion_boton(
                        self.botones_navegables[self.indice_seleccion]
                    )
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))
        titulo = self.font_title.render("Galería", True, (230, 150, 170))
        screen.blit(titulo, titulo.get_rect(center=(400, 80)))
        self.grupo_botones.draw(screen)
        pygame.display.flip()


class VisorGaleria(EscenaBase):
    def __init__(self, categoria):
        super().__init__()
        self.categoria = categoria
        self.elementos = DATOS_GALERIA.get(categoria, [])
        self.indice_actual = 0

        self.fuente_nombre = pygame.font.Font(
            resource_path("assets/fonts/fuente.ttf"), 50
        )
        self.fuente_desc = pygame.font.Font(
            resource_path("assets/fonts/fuente.ttf"), 18
        )
        self.fuente_boton = pygame.font.Font(
            resource_path("assets/fonts/fuente.ttf"), 20
        )

        self.fondo_original = pygame.Surface((800, 600))
        self.fondo_original.fill((255, 255, 255))
        self.fondo_filtrado = self.fondo_original.copy()
        Filtros.unirse_lista(self)

        imagen_boton = AssetManager.get_image("assets/botones/botonrect1.png")

        self.boton_ant = Boton(
            image=imagen_boton,
            pos=(200, 540),
            text_input="Anterior",
            font=self.fuente_boton,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_volver = Boton(
            image=imagen_boton,
            pos=(400, 540),
            text_input="Categorías",
            font=self.fuente_boton,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )
        self.boton_sig = Boton(
            image=imagen_boton,
            pos=(600, 540),
            text_input="Siguiente",
            font=self.fuente_boton,
            base_color=(245, 240, 225),
            hovering_color=(230, 150, 170),
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_ant, self.boton_volver, self.boton_sig)

        self.botones_navegables = [self.boton_ant, self.boton_volver, self.boton_sig]
        self.indice_seleccion = 1
        self.modo_teclado = False

    def configurar_filtro(self, nuevo_filtro):
        if self.fondo_original is not None:
            self.fondo_filtrado = Filtros.aplicar_filtro(
                self.fondo_original, nuevo_filtro
            )

    def ejecutar_accion_boton(self, boton):
        from escenas.workModules.audio_manager import AudioManager

        AudioManager.reproducir_sfx("click")

        if boton == self.boton_ant:
            self.indice_actual = (self.indice_actual - 1) % len(self.elementos)
        elif boton == self.boton_sig:
            self.indice_actual = (self.indice_actual + 1) % len(self.elementos)
        elif boton == self.boton_volver:
            Filtros.quitarse_lista(self)
            return MenuGaleria()
        return self

    def Update(self, dt, keys):
        for boton in self.botones_navegables:
            boton.seleccionado_por_teclado = False

        if self.modo_teclado:
            boton_actual = self.botones_navegables[self.indice_seleccion]
            boton_actual.seleccionado_por_teclado = True

        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def HandleEvents(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.modo_teclado = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for boton in self.botones_navegables:
                    if boton.checkForInput(mouse_pos):
                        return self.ejecutar_accion_boton(boton)
            if event.type == pygame.KEYDOWN:
                self.modo_teclado = True
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.indice_seleccion = (self.indice_seleccion + 1) % len(
                        self.botones_navegables
                    )
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.indice_seleccion = (self.indice_seleccion - 1) % len(
                        self.botones_navegables
                    )
                elif event.key == pygame.K_RETURN:
                    return self.ejecutar_accion_boton(
                        self.botones_navegables[self.indice_seleccion]
                    )
        return self

    def draw(self, screen):
        screen.blit(self.fondo_filtrado, (0, 0))

        if len(self.elementos) > 0:
            ruta, ancho, alto, cx, cy, nombre, desc, escala = self.elementos[
                self.indice_actual
            ]

            txt_nombre = self.fuente_nombre.render(nombre, True, (230, 150, 170))
            screen.blit(txt_nombre, txt_nombre.get_rect(center=(400, 70)))

            try:
                hoja = AssetManager.get_image(ruta)
                rect_recorte = pygame.Rect(cx, cy, ancho, alto)
                frame = hoja.subsurface(rect_recorte)
                frame = pygame.transform.scale(frame, (ancho * escala, alto * escala))
                screen.blit(frame, frame.get_rect(center=(400, 230)))
            except Exception:
                pass

            caja = pygame.Surface((650, 130), pygame.SRCALPHA)
            caja.fill((0, 0, 0, 200))
            screen.blit(caja, (75, 370))

            lineas = desc.split("\n")
            y_texto = 390
            for linea in lineas:
                txt_render = self.fuente_desc.render(linea, True, (255, 255, 255))
                screen.blit(txt_render, txt_render.get_rect(center=(400, y_texto)))
                y_texto += 30

        self.grupo_botones.draw(screen)
        pygame.display.flip()
