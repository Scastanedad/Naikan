import pygame

class Icono(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pos="topleft"):
        super().__init__()
        self.imagen_original = image
        self.image = self.imagen_original.copy()
        
        if pos == "topleft":
            self.rect = self.image.get_rect(topleft=(x, y))
        elif pos == "midtop":
            self.rect = self.image.get_rect(midtop=(x, y))
        
        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)

    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros
        self.image = Filtros.aplicar_filtro(self.imagen_original, nuevo_filtro)