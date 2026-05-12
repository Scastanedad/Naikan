import pygame
#Clase abstracta que es base para todas las habitaciones
class Habitacion():
    def __init__(self,datos):
        #Los datos proviene del diccionario que utilizamos en escenas dinamicas
        self.id = datos["id"]
        self.datos = datos 
        self.conexiones = datos["conexiones"]
        #Para renderizar los proyectiles los cargamos todos en una lista
        self.Proyectiles = pygame.sprite.Group() 
        
    def update(self, dt, keys,Jugador1, WIDTH, HEIGTH):
        pass
    def draw(self, screen):
        pass

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, listaO):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 10
        self.heigth = 10
        self.pos = [x,y]
        self.listaO = listaO
        #Sistema de colisiones para obstaculos
        self.image = pygame.Surface((self.width,self.heigth))
        self.image.fill((0,200,0))
        self.rect = pygame.Rect(self.x,self.y,self.width, self.heigth)
    
    def destruir(self):
        if self.pos in self.listaO:
            self.listaO.remove(self.pos)
        self.kill()    
        return self.listaO
    
class Gema(pygame.sprite.Sprite):
    def __init__(self, x,y, image=None):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        
        self.imagen_original = image
        self.imagen_filtrada = image
        
        self.color_original = (100, 0, 0)
        self.color_actual = self.color_original
        
        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)

        self.preparar_visuales()
        
        """ #Sistema de colisiones para obstaculos
        self.image = pygame.Surface((self.width,self.heigth))
        self.image.fill((100,0,0))
        self.rect = pygame.Rect(self.x,self.y,self.width, self.heigth) """
        
    def preparar_visuales(self):
        if self.imagen_original is not None:
            self.image = self.imagen_filtrada.copy()
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(self.color_actual)
        
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros
        if self.imagen_original is not None:
            self.imagen_filtrada = Filtros.aplicar_filtro(self.imagen_original, nuevo_filtro)
            
        if self.color_original is not None:
            super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
            color_con_alpha = (self.color_original[0], self.color_original[1], self.color_original[2], 255)
            super_temp.fill(color_con_alpha)
            self.color_actual = Filtros.aplicar_filtro(super_temp, nuevo_filtro).get_at((0, 0))
            
        self.preparar_visuales()

    def destruir(self):
        from escenas.workModules.filtros import Filtros
        Filtros.quitarse_lista(self)
        self.kill()