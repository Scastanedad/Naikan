from entidades.enemigos.ET_E_base import Enemigos
from entidades.enemigos import EnemigoMelee, EnemigoDistancia
from entidades.ET_general import Proyectil
import math,pygame, random
class Boss2(Enemigos):
    def __init__(self, x, y,in_pos):
        super().__init__(x, y, vida=15, velocidad=50, width=30, heigth=30, color = (200,200,100))
        #Estos intervalos determinan cada cuanto dispara y cada cuanto aparece enemigos
        self.cooldownP = 0
        self.cooldownSP = 0
        self.intervaloP = 1.5
        self.intervaloSP = 4
        #Cada cuanto se dibuja el sprite en pantalla con el que se puede interactuar
        #Render <- R y Draw <- D
        self.coolDownR = 0
        self.intervaloR = 15
        self.coolDownD = 0
        self.intervaloD = 5
        self.estado = "fueraP"
        self.in_pos = in_pos
        
    def update(self, dt, jugador):
        eventos = []
        self.coolDownR += dt
        self.cooldownP += dt
        self.cooldownSP += dt

        #Bloque de codigo correspondiente a hallar la posicion del jugador y vectores direccion
        dx = jugador.sprite.x - self.x
        dy = jugador.sprite.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)
        #Obtenemos los vectores direccion en x y en y
        if distancia !=0:
            dx = dx/ distancia
            dy = dy/distancia
        
       
        if self.coolDownR < self.intervaloR and self.cooldownP == 0:
            self.estado = "fueraP"
            self.x = 900
            self.y = 900
            if self.cooldownP >= self.intervaloP:
                self.cooldownP = 0
                spawn_x = random.randint(random.randint(0,jugador.sprite.x - 10),random.randint(jugador.sprite.x + 10,800))
                spawn_y = random.randint(random.randint(0,jugador.sprite.y - 10),random.randint(jugador.sprite.y + 10,600))
                # En ET_E_miniBoss1.py, justo antes de crear el proyectil:
                eventos.append(Proyectil(spawn_x, spawn_y, (dx, dy), 800, 2, dueño="Boss"))
            
            if self.cooldownSP >= self.intervaloSP:
                self.cooldownSP = 0
                if (random.randint(1,2) == 1):
                    eventos.append(EnemigoMelee(self.x,self.y,2,[self.x,self.y]))
                else:
                    eventos.append(EnemigoDistancia(self.x,self.y,2,[self.x,self.y]))
            return eventos
        else:
            if self.coolDownD < self.intervaloD : 
                self.estado = "dentroP"
                self.coolDownR = 0
                self.coolDownD += dt
                #Como lo queremos renderizar, vamos a pintarlo en una esquina de la pantalla
                match random.randint(1,4):
                    case 1:
                        self.x = 200
                        self.y = 150
                        self.actualizarRect()
                    case 2:
                        self.x = 600
                        self.y = 150
                        self.actualizarRect()
                    case 3: 
                        self.x = 200
                        self.y = 450
                        self.actualizarRect()
                    case 4:
                        self.x = 600
                        self.y = 450
                        self.actualizarRect()
            else:
                self.estado = "fueraP"
                self.coolDownD = 0
    def recibirDaño(self, Danio):
        return super().recibirDaño(Danio)
    
    def draw(self, screen, color=(100,0,0)):
        if self.estado == "dentroP":
            pygame.draw.rect(screen, color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
        elif self.estado == "fueraP":
            screen.fill((100,100,100))
        for i in range(self.vida):
            pygame.draw.rect(screen, (0,255,0), (400 + 10*i, 10, 5, 5))
    
    def destruir(self,BossD):
        self.recibirDaño(1)
        if (self.vida <= 0):
            BossD.remove(self)
            self.kill()
        
        