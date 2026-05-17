from habitaciones.H_base import Habitacion, Obstaculo,Gema
from habitaciones.H_colManager import ManejoColisiones
from entidades import EnemigoDistancia, EnemigoMelee,Proyectil
import pygame,random

class HabitacionSobrevivir(Habitacion):
    def __init__(self, datos,mundo):
        super().__init__(datos)
        self.mundo = mundo
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json
        self.obstaculos = pygame.sprite.Group(*[Obstaculo(x,y,datos["obstaculos"]) for x,y in datos["obstaculos"]]) # type: ignore
        self.enemigosM = pygame.sprite.Group(*[EnemigoMelee(x,y,mundo,[x,y],datos["enemigosM"]) for x,y in datos["enemigosM"]]) # type: ignore
        self.enemigosD = pygame.sprite.Group(*[EnemigoDistancia(x,y,mundo,[x,y],datos["enemigosD"]) for x,y in datos["enemigosD"]]) # type: ignore
        self.miniBoss = pygame.sprite.Group()
        self.Boss = pygame.sprite.Group()
        self.timer = 0 
        self.timer_melee = 0
        self.timer_distancia = 0

    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        self.timer += dt
        # En update:
        self.timer_melee += dt
        self.timer_distancia += dt

        if self.timer_melee >= 3.0:  
            x = random.randint(100, 700)
            y = random.randint(200, 500)
            self.enemigosM.add(EnemigoMelee(x, y))
            self.timer_melee = 0  
        if self.timer_distancia >= 2.0:  
            x = random.randint(100, 700)
            y = random.randint(200, 500)
            self.enemigosD.add(EnemigoDistancia(x, y)) 
            self.timer_distancia = 0
        ManejoColisiones(self,Jugador1,self.mundo)
        self.enemigosM.update(dt,Jugador1.sprite)
        for e in self.enemigosD:
            proyectil = e.update(dt, Jugador1.sprite)
            if proyectil:
                self.Proyectiles.add(proyectil)
        self.Proyectiles.update(dt)

        #Para el miniBoss

    def draw(self, screen):

        color_vida = (0, 255, 0)
        
        from escenas.workModules.filtros import Filtros
        filtro_actual = Filtros.filtro_actual
        
        if filtro_actual != "ninguno" and filtro_actual in Filtros.MATRICES:
            super_temp = pygame.Surface((1, 1), pygame.SRCALPHA)
            super_temp.fill(color_vida)
            super_filtrada = Filtros.aplicar_filtro(super_temp, filtro_actual)
            color_vida = super_filtrada.get_at((0, 0))

        
                # Una sola vez (en __init__ o al iniciar la escena)
        fuente = pygame.font.Font(None, 36)  # None = fuente por defecto, 36 = tamaño

        # En el draw / update
        texto_surface = fuente.render(f"Tiempo transcurrido: {int(self.timer)}", True, color_vida)
        texto_rect = texto_surface.get_rect(topright=(780, 10))  # 800 = ancho pantalla, 10 = margen
        screen.blit(texto_surface, texto_rect)
        self.Proyectiles.draw(screen)
        self.obstaculos.draw(screen)
        self.enemigosM.draw(screen)
        self.enemigosD.draw(screen)


        
