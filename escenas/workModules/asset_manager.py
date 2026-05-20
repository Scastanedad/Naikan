import pygame
from G_utils import resource_path

class AssetManager:
    imagenes_cache = {}

    @classmethod
    def get_image(cls, ruta):
        if ruta not in cls.imagenes_cache:
            ruta_segura = resource_path(ruta)
            cls.imagenes_cache[ruta] = pygame.image.load(ruta_segura).convert_alpha()

        return cls.imagenes_cache[ruta]