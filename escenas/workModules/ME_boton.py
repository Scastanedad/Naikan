#from escenas.workModules import Filtros
import pygame

class Boton(pygame.sprite.Sprite):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        super().__init__()
        self.color_base_original = base_color
        self.color_hover_original = hovering_color
        self.imagen_original = image
        
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        from escenas.workModules import Filtros
        Filtros.unirse_lista(self)

        self.preparar_visuales()
        
    def preparar_visuales(self):
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        if self.imagen_original is None:
            self.image = self.text.copy()
        else:
            imagen_fondo = getattr(self, 'imagen_filtrada', self.imagen_original)
            self.image = imagen_fondo.copy()
            
            texto_rect = self.text.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
            self.image.blit(self.text, texto_rect)
        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros
        
        super_temp_base = pygame.Surface((1, 1), pygame.SRCALPHA)
        super_temp_base.fill(self.base_color)
        self.base_color = Filtros.aplicar_filtro(super_temp_base, nuevo_filtro).get_at((0, 0))

        super_temp_hover = pygame.Surface((1, 1), pygame.SRCALPHA)
        super_temp_hover.fill(self.hovering_color)
        self.hovering_color = Filtros.aplicar_filtro(super_temp_hover, nuevo_filtro).get_at((0, 0))
        
        if self.imagen_original:
            self.imagen_filtrada = Filtros.aplicar_filtro(self.imagen_original, nuevo_filtro)

        self.preparar_visuales()

    def update(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
        
        if self.imagen_original is not None:
            imagen_fondo = getattr(self, 'imagen_filtrada', self.imagen_original)
            self.image = imagen_fondo.copy()
            texto_rect = self.text.get_rect(center=(self.image.get_width()//2, self.image.get_height()//2))
            self.image.blit(self.text, texto_rect)
        else:
            self.image = self.text

    def checkForInput(self, position):
        return self.rect.collidepoint(position)
    