from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee
import math,pygame, random

FRAME_CONFIG_miniBOSS2 = {
    (1,  0): {"fila": 0,   "count": 4},   
    (-1, 0): {"fila": 64,  "count": 4},  
    (0, -1): {"fila": 128, "count": 4},  
    (0,  1): {"fila": 192, "count": 4}, 
}

class miniBoss2(Enemigos):
    def __init__(self, x, y,in_pos):
        super().__init__(x, y, vida=15, velocidad=50, width=64, heigth=64, color = (200,200,100), sprite_path="assets/sprites/bosses/boss_mundo1.png", frame_config=FRAME_CONFIG_miniBOSS2, escala=2)
        self.in_pos = in_pos
        self.vidaInicial =15
        
    def update(self, dt, jugador):
        eventos = []
        dx = jugador.sprite.x - self.x
        dy = jugador.sprite.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        #Obtenemos los vectores direccion en x y en y
        if distancia !=0:
            dx = dx/ distancia
            dy = dy/distancia
        
        self.x += dx * dt * self.velocidad
        self.y += dy * dt * self.velocidad
        
        if abs(dx) > abs(dy):
            self.direccion = (1, 0) if dx > 0 else (-1, 0)
        else:
            self.direccion = (0, 1) if dy > 0 else (0, -1)
            
        self.moviendo = True
        self.animar(dt)
        
        
        self.actualizarRect()
        #Si le pegan spawnea a un enemigoMelee
        if self.vidaInicial > self.vida:
            self.vidaInicial = self.vida
            eventos.append(EnemigoMelee(self.x,self.y,2,[self.x,self.y]))

    
    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)
    
    def draw(self, screen, color=(100,0,0)):
        #pygame.draw.rect(screen, color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
        screen.blit(self.image, self.rect)
        
        color_vida = (0, 255, 0)
        
        from escenas.workModules.filtros import Filtros
        filtro_actual = Filtros.filtro_actual
        
        if filtro_actual != "ninguno" and filtro_actual in Filtros.MATRICES:
            super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
            super_temp.fill(color_vida)
            super_filtrada = Filtros.aplicar_filtro(super_temp, filtro_actual)
            color_vida = super_filtrada.get_at((0, 0))

        for i in range(self.vida):
            pygame.draw.rect(screen, color_vida, (400 + 10*i, 10, 5, 5))
            
    def destruir(self,miniBossD):
        self.recibirDaño(1)
        if (self.vida <= 0):
            miniBossD.remove(self)
            from escenas.workModules.filtros import Filtros
            Filtros.quitarse_lista(self)
            self.kill()
        
#Esta clase al no tener sprite todavía usa la lógica más base de los filtros que es para los rectangulos, que está en la lógica
#de la clase Entidad
