import pygame
from escenas.ES_base import EscenaBase
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager

class EscenaAdvertencia(EscenaBase):
    def __init__(self):
        super().__init__()
        self.tiempo_transcurrido = 0
        self.tiempo_espera = 4.0  

        try:
            ruta_imagen = resource_path("ruta")
            self.imagen_advertencia = AssetManager.get_image(ruta_imagen)
            self.imagen_advertencia = pygame.transform.scale(self.imagen_advertencia, (800, 600))
        except:
            self.imagen_advertencia = pygame.Surface((800, 600))
            self.imagen_advertencia.fill((15, 15, 15))
            fuente = pygame.font.Font(resource_path("assets/fonts/fuente.ttf"), 30)
            texto = fuente.render("ADVERTENCIA: Contenido Exclusivo para +15", True, (255, 50, 50))
            self.imagen_advertencia.blit(texto, texto.get_rect(center=(400, 300)))

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                from escenas import MainMenu
                return MainMenu()
        return self

    def Update(self, dt, keys):
        self.tiempo_transcurrido += dt

        if self.tiempo_transcurrido >= self.tiempo_espera:
            from escenas import MainMenu
            return MainMenu()
            
        return self

    def draw(self, screen):
        screen.blit(self.imagen_advertencia, (0, 0))