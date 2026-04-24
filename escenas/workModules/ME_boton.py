import pygame

class Boton(pygame.sprite.Sprite):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        super().__init__()
        self.imagen_original = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
        if self.imagen_original is None:
            self.image = self.text.copy()
        else:
            self.image = self.imagen_original.copy()
        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
        
        if self.imagen_original is not None: 
            self.image = self.imagen_original.copy()
            self.image.blit(self.text, self.text_rect)
        else:
            self.image = self.text

    def checkForInput(self, position):
        return self.rect.collidepoint(position)
    