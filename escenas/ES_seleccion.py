import pygame
from escenas.ES_base import EscenaBase
from escenas.UT_guardado import cargarProgreso
from escenas.workModules.ME_boton import Boton


class SeleccionMundo(EscenaBase):
    def __init__(self):
        super().__init__()
        self.progreso = cargarProgreso()
        self.mundos_desbloqueados = self.progreso["mundos_desbloqueados"]

        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_regreasr = pygame.font.Font(None, 60)
        self.fuente = pygame.font.Font(None, 30)
        
        self.boton_titulo = Boton(
                image=None,
                pos=(400, 100),
                text_input="Selecciona un Mundo",
                font=self.fuente_titulo,
                base_color=(0, 255, 0),
                hovering_color=(0, 255, 0))
        
        fondo_1 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 1 in self.mundos_desbloqueados:
            fondo_1.fill((0, 200, 0))
            self.boton_mundo_1 = Boton(
                image=fondo_1,
                pos=(400, 175),
                text_input="Mundo 1",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))
        else:
            fondo_1.fill((80, 80, 80))
            self.boton_mundo_1 = Boton(
                image=fondo_1,
                pos=(400, 175),
                text_input="Mundo 1 - BLOQUEADO",
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))

        fondo_2 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 2 in self.mundos_desbloqueados:
            fondo_2.fill((0, 200, 0))
            self.boton_mundo_2 = Boton(
                image=fondo_2,
                pos=(400, 255),
                text_input="Mundo 2",
                font=self.fuente, 
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))
        else:
            fondo_2.fill((80, 80, 80))
            self.boton_mundo_2 = Boton(
                image=fondo_2, 
                pos=(400, 255),
                text_input="Mundo 2 - BLOQUEADO",
                font=self.fuente, 
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))

        fondo_3 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 3 in self.mundos_desbloqueados:
            fondo_3.fill((0, 200, 0))
            self.boton_mundo_3 = Boton(
                image=fondo_3,
                pos=(400, 335), 
                text_input="Mundo 3", 
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))
        else:
            fondo_3.fill((80, 80, 80))
            self.boton_mundo_3 = Boton(
                image=fondo_3, 
                pos=(400, 335), 
                text_input="Mundo 3 - BLOQUEADO", 
                font=self.fuente,
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))

        fondo_4 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 4 in self.mundos_desbloqueados:
            fondo_4.fill((0, 200, 0))
            self.boton_mundo_4 = Boton(
                image=fondo_4, 
                pos=(400, 415),
                text_input="Mundo 4", 
                font=self.fuente, 
                base_color=(0, 0, 0), 
                hovering_color=(255, 255, 255))
        else:
            fondo_4.fill((80, 80, 80))
            self.boton_mundo_4 = Boton(
                image=fondo_4, 
                pos=(400, 415), 
                text_input="Mundo 4 - BLOQUEADO", 
                font=self.fuente, 
                base_color=(0, 0, 0), 
                hovering_color=(255, 255, 255))

        self.boton_regresar = Boton(
            image=None, 
            pos=(400, 520), 
            text_input="Regresar", 
            font=self.fuente_regreasr,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255))
        
        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_titulo, self.boton_mundo_1, self.boton_mundo_2, self.boton_mundo_3, self.boton_mundo_4, self.boton_regresar)

        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        self.fondo = pygame.image.load('assets/menuImages/menu_principal.png').convert()
        self.fondo = pygame.transform.scale(self.fondo, (800, 600))
        
    """ def mundos_disponibles(self):
        return self.progreso["mundos_desbloqueados"] """

    def seleccionar(self, mundo_id):
        if mundo_id in self.progreso["mundos_desbloqueados"]:
            return SeleccionNivel(mundo_id)
        return self

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from escenas.estaticas import MainMenu
                    return MainMenu()
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
                    from escenas.estaticas import MainMenu
                    return MainMenu()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        #screen.fill((0, 0, 0))
        screen.blit(self.fondo, (0, 0))
        self.grupo_botones.draw(screen)
        pygame.display.flip()

class SeleccionNivel(EscenaBase):
    def __init__(self, mundo_id):
        super().__init__()
        self.mundo_id = mundo_id
        self.progreso = cargarProgreso()
        
        self.desbloqueados = self.niveles_desbloqueados()
        self.completados = self.niveles_completados()

        self.fuente_titulo = pygame.font.Font(None, 60) 
        self.fuente_regresar = pygame.font.Font(None, 60)
        self.fuente = pygame.font.Font(None, 30)

        self.boton_titulo = Boton(
            image=None,
            pos=(400, 100),
            text_input=f"Mundo {self.mundo_id} - Selecciona un Nivel",
            font=self.fuente_titulo,
            base_color=(0, 255, 0),
            hovering_color=(0, 255, 0)
        )

        fondo_1 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 1 in self.desbloqueados:
            if 1 in self.completados:
                fondo_1.fill((0, 100, 200)) 
                self.boton_nivel_1 = Boton(
                    image=fondo_1,
                    pos=(400, 175), 
                    text_input="Nivel 1 - OK", 
                    font=self.fuente,
                    base_color=(255, 255, 255), 
                    hovering_color=(255, 255, 255))
            else:
                fondo_1.fill((0, 200, 0)) 
                self.boton_nivel_1 = Boton(
                    image=fondo_1,
                    pos=(400, 175),
                    text_input="Nivel 1",
                    font=self.fuente, 
                    base_color=(0, 0, 0),
                    hovering_color=(255, 255, 255))
        else:
            fondo_1.fill((80, 80, 80))  
            self.boton_nivel_1 = Boton(
                image=fondo_1,
                pos=(400, 175),
                text_input="Nivel 1 - BLOQUEADO", 
                font=self.fuente,
                base_color=(0, 0, 0), 
                hovering_color=(255, 255, 255))

        fondo_2 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 2 in self.desbloqueados:
            if 2 in self.completados:
                fondo_2.fill((0, 100, 200))
                self.boton_nivel_2 = Boton(
                    image=fondo_2, 
                    pos=(400, 255), 
                    text_input="Nivel 2 - OK", 
                    font=self.fuente, 
                    base_color=(255, 255, 255),
                    hovering_color=(255, 255, 255))
            else:
                fondo_2.fill((0, 200, 0))
                self.boton_nivel_2 = Boton(
                    image=fondo_2, 
                    pos=(400, 255), 
                    text_input="Nivel 2",
                    font=self.fuente,
                    base_color=(0, 0, 0), 
                    hovering_color=(255, 255, 255))
        else:
            fondo_2.fill((80, 80, 80))
            self.boton_nivel_2 = Boton(
                image=fondo_2, 
                pos=(400, 255), 
                text_input="Nivel 2 - BLOQUEADO",
                font=self.fuente, 
                base_color=(0, 0, 0), 
                hovering_color=(255, 255, 255))

        fondo_3 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 3 in self.desbloqueados:
            if 3 in self.completados:
                fondo_3.fill((0, 100, 200))
                self.boton_nivel_3 = Boton(
                    image=fondo_3,
                    pos=(400, 335), 
                    text_input="Nivel 3 - OK", 
                    font=self.fuente, 
                    base_color=(255, 255, 255),
                    hovering_color=(255, 255, 255))
            else:
                fondo_3.fill((0, 200, 0))
                self.boton_nivel_3 = Boton(
                    image=fondo_3,
                    pos=(400, 335), 
                    text_input="Nivel 3",
                    font=self.fuente,
                    base_color=(0, 0, 0), 
                    hovering_color=(255, 255, 255))
        else:
            fondo_3.fill((80, 80, 80))
            self.boton_nivel_3 = Boton(
                image=fondo_3,
                pos=(400, 335), 
                text_input="Nivel 3 - BLOQUEADO",
                font=self.fuente, 
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))

        fondo_4 = pygame.Surface((300, 50), pygame.SRCALPHA)
        if 4 in self.desbloqueados:
            if 4 in self.completados:
                fondo_4.fill((0, 100, 200))
                self.boton_nivel_4 = Boton(
                    image=fondo_4,
                    pos=(400, 415), 
                    text_input="Nivel 4 - OK", 
                    font=self.fuente,
                    base_color=(255, 255, 255),
                    hovering_color=(255, 255, 255))
            else:
                fondo_4.fill((0, 200, 0))
                self.boton_nivel_4 = Boton(
                    image=fondo_4,
                    pos=(400, 415),
                    text_input="Nivel 4",
                    font=self.fuente, 
                    base_color=(0, 0, 0),
                    hovering_color=(255, 255, 255))
        else:
            fondo_4.fill((80, 80, 80))
            self.boton_nivel_4 = Boton(
                image=fondo_4, 
                pos=(400, 415),
                text_input="Nivel 4 - BLOQUEADO",
                font=self.fuente, 
                base_color=(0, 0, 0),
                hovering_color=(255, 255, 255))

        self.boton_regresar = Boton(
            image=None, 
            pos=(400, 520), 
            text_input="Regresar", 
            font=self.fuente_regresar,
            base_color=(0, 255, 0),
            hovering_color=(255, 255, 255)
        )

        self.grupo_botones = pygame.sprite.Group()
        self.grupo_botones.add(self.boton_titulo, self.boton_nivel_1, self.boton_nivel_2, self.boton_nivel_3, self.boton_nivel_4, self.boton_regresar)

        from escenas.workModules.audio_manager import AudioManager
        AudioManager.reproducir_musica("assets/musica/naikan_main_theme.ogg")
        
        self.fondo = pygame.image.load('assets/menuImages/menu_principal.png').convert()
        self.fondo = pygame.transform.scale(self.fondo, (800, 600))
        
    def niveles_desbloqueados(self):
        return self.progreso["niveles_desbloqueados"][str(self.mundo_id)]

    def niveles_completados(self):
        return self.progreso["niveles_completados"][str(self.mundo_id)]

    def seleccionar(self, nivel_id):
        if nivel_id in self.niveles_desbloqueados():
            from escenas.ES_dinamicas import EscenaJuego
            return EscenaJuego(numeroNivel=nivel_id, mundoActual=self.mundo_id)
        return self

    def HandleEvents(self, events):
        for event in events:      
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.boton_nivel_1.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(1)
                if self.boton_nivel_2.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(2)
                if self.boton_nivel_3.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(3)
                if self.boton_nivel_4.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return self.seleccionar(4)
                if self.boton_regresar.checkForInput(mouse_pos):
                    from escenas.workModules.audio_manager import AudioManager
                    AudioManager.reproducir_sfx("click")
                    return SeleccionMundo()
        return self

    def Update(self, dt, keys):
        self.grupo_botones.update(pygame.mouse.get_pos())
        return self

    def draw(self, screen):
        #screen.fill((0, 0, 0))
        screen.blit(self.fondo, (0, 0))
        self.grupo_botones.draw(screen)
        pygame.display.flip