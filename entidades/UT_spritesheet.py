import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_fila(self, y, width, height, count):
        frames = []
        for i in range(count):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(self.sheet, (0, 0), (i * width, y, width, height))
            frames.append(frame)
        return frames