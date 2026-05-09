import pygame,math
#Clase base para todas las entidades
class Entidad(pygame.sprite.Sprite):
    def __init__(self, x, y, vida, velocidad, width, heigth,color):
        super().__init__()
        self.x = x
        self.y = y
        self.vida = vida
        self.velocidad = velocidad
        self.width = width
        self.height = heigth
        
        self.color_original = color
        self.color_actual = color
        
        self.ss_original = None 
        self.ss_filtrada = None
        
        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)

        self.preparar_visuales()
        
    def preparar_visuales(self): #Se crea la imagen/superficie y su hitbox
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color_actual)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def configurar_filtro(self, nuevo_filtro): 
        from escenas.workModules.filtros import Filtros
        ss_origen = getattr(self, 'ss_original', None)
        
        if ss_origen is None and self.color_original is None: #En caso de no tener imagen ni color no se hace nada para evitar errores en el constructor
            return

        if ss_origen is not None:
            self.ss_filtrada = Filtros.aplicar_filtro(ss_origen, nuevo_filtro) #si tiene spritesheet se le aplica el filtro correspondiente
        
        if self.color_original is not None: #Si tiene es color (osea es un rectangulo sin la sprite), se hace el cambio también
            super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
            color_con_alpha = (self.color_original[0], self.color_original[1], self.color_original[2], 255)
            super_temp.fill(color_con_alpha)
            self.color_actual = Filtros.aplicar_filtro(super_temp, nuevo_filtro).get_at((0, 0))
        
        self.preparar_visuales() #Se vuelve a rehacer la superficie y la hitbox actualizada
    
    def recibirDaño(self,Daño):
        self.vida -= Daño

    def update(self,dt,keys,width, height):
        pass

    def actualizarRect(self):
        self.rect.center = (self.x, self.y)

class Proyectil(pygame.sprite.Sprite):
  
    def __init__(self, x ,y,direccion, velocidad = 600, modo = 1, color = (0,0,200), dueño="enemigo"):
        super().__init__()
        self.dueño = dueño
        self.x = x
        self.y = y
        self.modo = modo
        self.velocidad = velocidad
        self.direccion = direccion
        self.width = 5
        self.height = 5
        
        self.color_original = color
        self.color_actual = color

        self.grace_period = 0.1  # 100ms sin colisionar
        self.t = 0
        
        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)

        self.preparar_visuales()

    def preparar_visuales(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color_actual)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros
        
        super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
        color_con_alpha = (self.color_original[0], self.color_original[1], self.color_original[2], 255)
        super_temp.fill(color_con_alpha)
        self.color_actual = Filtros.aplicar_filtro(super_temp, nuevo_filtro).get_at((0, 0))
        
        self.preparar_visuales()
        
    def update (self,dt):
        self.t += dt
        self.grace_period -= dt
        match self.modo:
            case 1:
                self.x += dt * self.velocidad*self.direccion[0]
                self.y += dt *self.velocidad*self.direccion[1]
            case 2:
                perp_x = -self.direccion[1]
                perp_y = self.direccion[0]

                amplitud = 20
                frecuencia = 200

                offset = math.sin(self.t * frecuencia) * amplitud

                self.x += dt * self.velocidad * self.direccion[0] + perp_x * offset
                self.y += dt * self.velocidad * self.direccion[1] + perp_y * offset
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
            from escenas.workModules import Filtros
            Filtros.quitarse_lista(self)
        self.rect.center = (self.x, self.y)