import pygame
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager

class SpriteSheet:
    def __init__(self, origen): #filename ahora es origen
        if isinstance(origen, str):
            self.sheet = AssetManager.get_image(origen)
        else:
            self.sheet = origen

    def get_fila(self, y, width, height, count, escala=1):
        frames = []
        for i in range(count):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(self.sheet, (0, 0), (i * width, y, width, height))
            if escala != 1:
                frame = pygame.transform.scale(frame, (width * escala, height * escala))
            frames.append(frame)
        return frames