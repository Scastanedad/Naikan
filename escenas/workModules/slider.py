import pygame

class Slider:
    def __init__(self, x, y, ancho, alto, valor_inicial=0.5):

        self.rect_barra = pygame.Rect(x, y, ancho, alto)
        
        self.radio_deslizador = alto + 2
        self.x_deslizador = x + (ancho * valor_inicial)
        self.y_deslizador = y + (alto // 2)
        
        self.arrastrar = False
        self.valor = valor_inicial 
        
        self.color_barra_original = (50, 50, 50)
        self.color_circulo_original = (245, 240, 225)
        
        self.color_barra_actual = self.color_barra_original
        self.color_circulo_actual = self.color_circulo_original

        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)
        
    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros

        temp_barra = pygame.Surface((1, 1), pygame.SRCALPHA)
        color_barra_alpha = (self.color_barra_original[0], self.color_barra_original[1], self.color_barra_original[2], 255)
        temp_barra.fill(color_barra_alpha)
        self.color_barra_actual = Filtros.aplicar_filtro(temp_barra, nuevo_filtro).get_at((0, 0))

        temp_circulo = pygame.Surface((1, 1), pygame.SRCALPHA)
        color_circulo_alpha = (self.color_circulo_original[0], self.color_circulo_original[1], self.color_circulo_original[2], 255)
        temp_circulo.fill(color_circulo_alpha)
        self.color_circulo_actual = Filtros.aplicar_filtro(temp_circulo, nuevo_filtro).get_at((0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_barra_actual, self.rect_barra, border_radius=5)
        pygame.draw.circle(screen, self.color_circulo_actual, (int(self.x_deslizador), self.y_deslizador), self.radio_deslizador)

    def Update(self):
        if self.arrastrar:
            mouse_x = pygame.mouse.get_pos()[0]
            if mouse_x < self.rect_barra.left:
                self.x_deslizador = self.rect_barra.left
            elif mouse_x > self.rect_barra.right:
                self.x_deslizador = self.rect_barra.right
            else:
                self.x_deslizador = mouse_x
            
            self.valor = (self.x_deslizador - self.rect_barra.left) / self.rect_barra.width

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                distancia = ((mouse_pos[0] - self.x_deslizador)**2 + (mouse_pos[1] - self.y_deslizador)**2)**0.5
                if distancia <= self.radio_deslizador:
                    self.arrastrar = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.arrastrar = False