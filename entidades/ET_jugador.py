from entidades.ET_general import Entidad
from entidades.UT_spritesheet import SpriteSheet
from escenas.UT_guardado import cargarConfig
import pygame

ESCALA = 2 # 32 * 3 = 96px visual, hitbox sigue siendo 32x32

class Jugador(Entidad):
    def __init__(self, x, y, vida=None, velocidad=None, width=None, heigth=None):
        self.ss_objeto = None #Se asigna None para evitar errores al llamar al super
        
        # Hitbox sigue siendo 32x32
        super().__init__(x, y, vida=3, velocidad=300, width=32, heigth=32, color=(0,0,100)) #Aquí se une a la lista de observadores y se llama a configurar filtro por defecto de Entidad
        
        self.ss_objeto = SpriteSheet("assets/sprites/jugador/spriteJugador.png") #Se crea el objeto de la spritesheet para poder hacer las animaciones
        self.ss_original = self.ss_objeto.sheet.copy() #Estas son las superficies solamente
        self.ss_filtrada = self.ss_original.copy()
        
        self.direccion = (1, 0)
        self.dañoCooldown = 1
        self.intervaloD = 1
        self.cooldown = 2
        self.intervalo = 2

        # Animación
        self.timer_anim = 0
        self.frame_index = 0
        self.anim_speed = 0.1
        self.moviendo = False
        
        
        self.animaciones = {}
        
        from escenas.workModules.filtros import Filtros
        self.configurar_filtro(Filtros.filtro_actual) #Se aplica el filtro de nuevo manualmente porque en el super no se aplicó realmente

        """ # Sprite sheet escalada 3x visualmente
        ss = SpriteSheet("assets/sprites/jugador/spriteJugador.png")
        self.animaciones = {
            (1,  0): ss.get_fila(y=0,  width=32, height=32, count=4, escala=ESCALA),
            (-1, 0): ss.get_fila(y=32, width=32, height=32, count=4, escala=ESCALA),
            (0, -1): ss.get_fila(y=64, width=32, height=32, count=4, escala=ESCALA),
            (0,  1): ss.get_fila(y=96, width=32, height=32, count=4, escala=ESCALA),
        }
        self.image = self.animaciones[self.direccion][0] """
        
    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros
        self.ss_filtrada = Filtros.aplicar_filtro(self.ss_original, nuevo_filtro)
        super().configurar_filtro(nuevo_filtro)
        
        self.preparar_visuales()

    def preparar_visuales(self):
        if self.ss_objeto is not None and hasattr(self, 'ss_filtrada'): #Validacion para que no tire error
            self.ss_objeto.sheet = self.ss_filtrada
            ESCALA = 2
            self.animaciones = {
                (1,  0): self.ss_objeto.get_fila(y=0,  width=32, height=32, count=4, escala=ESCALA),
                (-1, 0): self.ss_objeto.get_fila(y=32, width=32, height=32, count=4, escala=ESCALA),
                (0, -1): self.ss_objeto.get_fila(y=64, width=32, height=32, count=4, escala=ESCALA),
                (0,  1): self.ss_objeto.get_fila(y=96, width=32, height=32, count=4, escala=ESCALA),
            }
            
            self.image = self.animaciones[self.direccion][self.frame_index]
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt, keys, width, height):
        self.mover(dt, keys, width, height)
        self.animar(dt)

    def animar(self, dt):
        frames = self.animaciones[self.direccion]
        if self.moviendo:
            self.timer_anim += dt
            if self.timer_anim >= self.anim_speed:
                self.timer_anim = 0
                self.frame_index = (self.frame_index + 1) % len(frames)
        else:
            self.frame_index = 0
            self.timer_anim = 0

        self.image = frames[self.frame_index]
        # El rect se recalcula centrado en la posición del jugador
        # Así el sprite grande queda centrado sobre la hitbox chica
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def mover(self, dt, keys, width, height):
        configuracion = cargarConfig()
        teclas = configuracion["teclas"]
        self.cooldown += dt
        self.dañoCooldown += dt
        self.moviendo = False

        if (keys[teclas["arriba"]] or keys[pygame.K_UP]) and (self.y > 40):
            self.y -= self.velocidad * dt
            self.direccion = (0, -1)
            self.moviendo = True
        if (keys[teclas["abajo"]] or keys[pygame.K_DOWN]) and (self.y < height - 40):
            self.y += self.velocidad * dt
            self.direccion = (0, 1)
            self.moviendo = True
        if (keys[teclas["derecha"]] or keys[pygame.K_RIGHT]) and (self.x < width - 40):
            self.x += self.velocidad * dt
            self.direccion = (1, 0)
            self.moviendo = True
        if (keys[teclas["izquierda"]] or keys[pygame.K_LEFT]) and (self.x > 40):
            self.x -= self.velocidad * dt
            self.direccion = (-1, 0)
            self.moviendo = True

        if keys[pygame.K_c] and (self.cooldown >= self.intervalo):
            self.cooldown = 0
            if (self.x < 680) and (self.x > 120):
                self.x += 100 * self.direccion[0]
            if (self.y < 480) and (self.y > 120):
                self.y += 100 * self.direccion[1]
                
            self.moviendo = True

        self.actualizarRect()

    def recibirDaño(self, Daño=None):
        return super().recibirDaño(Daño=1)

    def actualizarRect(self):
        return super().actualizarRect()