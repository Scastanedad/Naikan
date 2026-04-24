import pygame

class Slider:
    def __init__(self, x, y, ancho, alto, valor_inicial=0.5):

        self.rect_barra = pygame.Rect(x, y, ancho, alto)
        
        self.radio_deslizador = alto + 2
        self.x_deslizador = x + (ancho * valor_inicial)
        self.y_deslizador = y + (alto // 2)
        
        self.arrastrar = False
        self.valor = valor_inicial 

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect_barra, border_radius=5)
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x_deslizador), self.y_deslizador), self.radio_deslizador)

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