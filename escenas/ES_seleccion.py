import pygame
from escenas.ES_base import EscenaBase
from escenas.UT_guardado import cargarProgreso


class SeleccionMundo(EscenaBase):
    def __init__(self):
        super().__init__()
        self.progreso = cargarProgreso()

    def mundos_disponibles(self):
        return self.progreso["mundos_desbloqueados"]

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
                mouse = pygame.mouse.get_pos()
                for mundo_id in range(1, 5):
                    y = 150 + (mundo_id - 1) * 80
                    rect = pygame.Rect(300, y, 200, 50)
                    if rect.collidepoint(mouse):
                        return self.seleccionar(mundo_id)
        return self

    def Update(self, dt, keys):
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))

        fuente = pygame.font.Font(None, 40)
        titulo = fuente.render("Selecciona un Mundo", True, (255, 255, 255))
        screen.blit(titulo, (250, 50))

        fuente_btn = pygame.font.Font(None, 32)
        for mundo_id in range(1, 5):
            y = 150 + (mundo_id - 1) * 80
            rect = pygame.Rect(300, y, 200, 50)

            if mundo_id in self.progreso["mundos_desbloqueados"]:
                pygame.draw.rect(screen, (0, 200, 0), rect)
                texto = fuente_btn.render(f"Mundo {mundo_id}", True, (0, 0, 0))
            else:
                pygame.draw.rect(screen, (80, 80, 80), rect)
                texto = fuente_btn.render(f"Mundo {mundo_id} - BLOQUEADO", True, (150, 150, 150))

            screen.blit(texto, (rect.x + 10, rect.y + 12))


class SeleccionNivel(EscenaBase):
    def __init__(self, mundo_id):
        super().__init__()
        self.mundo_id = mundo_id
        self.progreso = cargarProgreso()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return SeleccionMundo()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for nivel_id in range(1, 5):
                    y = 150 + (nivel_id - 1) * 80
                    rect = pygame.Rect(300, y, 200, 50)
                    if rect.collidepoint(mouse):
                        return self.seleccionar(nivel_id)
        return self

    def Update(self, dt, keys):
        return self

    def draw(self, screen):
        screen.fill((0, 0, 0))

        fuente = pygame.font.Font(None, 40)
        titulo = fuente.render(f"Mundo {self.mundo_id} - Selecciona un Nivel", True, (255, 255, 255))
        screen.blit(titulo, (150, 50))

        fuente_btn = pygame.font.Font(None, 32)
        desbloqueados = self.niveles_desbloqueados()
        completados   = self.niveles_completados()

        for nivel_id in range(1, 5):
            y = 150 + (nivel_id - 1) * 80
            rect = pygame.Rect(300, y, 200, 50)

            if nivel_id in desbloqueados:
                if nivel_id in completados:
                    pygame.draw.rect(screen, (0, 100, 200), rect)
                    texto = fuente_btn.render(f"Nivel {nivel_id} - OK", True, (255, 255, 255))
                else:
                    pygame.draw.rect(screen, (0, 200, 0), rect)
                    texto = fuente_btn.render(f"Nivel {nivel_id}", True, (0, 0, 0))
            else:
                pygame.draw.rect(screen, (80, 80, 80), rect)
                texto = fuente_btn.render(f"Nivel {nivel_id} - BLOQUEADO", True, (150, 150, 150))

            screen.blit(texto, (rect.x + 10, rect.y + 12))