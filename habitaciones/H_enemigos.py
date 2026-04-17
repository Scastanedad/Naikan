from habitaciones.H_base import Habitacion, Obstaculo
from entidades import EnemigoDistancia, EnemigoMelee, MiniBoss1,Proyectil
import pygame

class HabitacionEnemigos(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json
        self.obstaculos = pygame.sprite.Group(*[Obstaculo(x,y,datos["obstaculos"]) for x,y in datos["obstaculos"]]) # type: ignore
        self.enemigosM = pygame.sprite.Group(*[EnemigoMelee(x,y,[x,y],datos["enemigosM"]) for x,y in datos["enemigosM"]]) # type: ignore
        self.enemigosD = pygame.sprite.Group(*[EnemigoDistancia(x,y,[x,y],datos["enemigosD"]) for x,y in datos["enemigosD"]]) # type: ignore
        self.miniBoss = []
    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        eventos =[]
        # --- Enemigos Melee ---
        """

        # --- Enemigos Distancia ---


        # --- Colision proyectil -> jugador ---
        proyectiles_a_eliminar = []
        for p in self.Proyectiles:
            if p.rect.colliderect(Jugador1.rect):
                Jugador1.recibirDaño()
                proyectiles_a_eliminar.append(p)
        for p in proyectiles_a_eliminar:
            self.Proyectiles.remove(p)
        """
        # --- Actualizar proyectiles ---
        self.ManejoColisiones(Jugador1)
        self.enemigosM.update(dt,Jugador1.sprite)
        for e in self.enemigosD:
            proyectil = e.update(dt, Jugador1.sprite)
            if proyectil:
                self.Proyectiles.add(proyectil)
        self.Proyectiles.update(dt)


        """
        for m in self.miniBoss:
            if Jugador1.rect.colliderect(m.rect):
                Jugador1.x = WIDTH//2
                Jugador1.y = HEIGTH//2
                Jugador1.recibirDaño(1)
            for p in self.Proyectiles[:]:
                if p.rect.colliderect(m.rect):
                    self.Proyectiles.remove(p)
                    m.recibirDaño(1)
                    if (m.vida<0):
                        self.miniBoss.remove(m)
                        
        for b in self.miniBoss:
            eventos = b.update(dt,Jugador1)          
        if eventos: 
            for e in eventos:
                if isinstance(e,Proyectil):
                    proyectil = e
                    if proyectil:
                        self.Proyectiles.add(proyectil)
                if isinstance(e,EnemigoMelee):
                    enemigo = e
                    if enemigo:
                        self.enemigosM.add(e)

        #Para el miniBoss

        
    """
    def draw(self, screen):
        self.Proyectiles.draw(screen)
        self.obstaculos.draw(screen)
        self.enemigosM.draw(screen)
        self.enemigosD.draw(screen)
        """
        for e in self.enemigosD:
            e.draw(screen)
        for m in self.miniBoss:
            m.draw(screen)"""

    def SpawnMiniBoss(self,mundo):
        if ( mundo == 1):
            self.miniBoss.append(MiniBoss1(400,300))
    
    def ManejoColisiones(self,Jugador1):
        self.ColJugadorObstaculo(Jugador1)
        self.ColObsProyectil()
        self.ColProyEnemM()
        self.ColEneMJugador(Jugador1)
        self.ColProyEnemD()
    
    def ColJugadorObstaculo(self,Jugador1):
        colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , self.obstaculos, False) # type: ignore
        if colisiones:
            for obs in colisiones:
                self.datos["obstaculos"] = obs.destruir()
            Jugador1.sprite.recibirDaño() # type: ignore

    def ColObsProyectil(self):
        colisiones = pygame.sprite.groupcollide(self.Proyectiles, self.obstaculos,True,False)
        for proyectil, obstaculos in colisiones.items():
            for obs in obstaculos:
                self.datos["obstaculos"] = obs.destruir()
    
    def ColProyEnemM(self):
        colisiones = pygame.sprite.groupcollide(self.Proyectiles,self.enemigosM,True, False)
        for proyectil, enemigos in colisiones.items():
            for enem in enemigos:
                #Estructura para implementar enemigos con vida 
                self.datos["enemigosM"] = enem.destruir() if enem.destruir() else self.datos["enemigosM"]
    
    def ColEneMJugador(self,Jugador1):
        colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , self.enemigosM, False) # type: ignore
        if colisiones:
            if (Jugador1.sprite.dañoCooldown >= 1):
                Jugador1.sprite.dañoCooldown = 0
                Jugador1.sprite.recibirDaño() # type: ignore
    
    def ColProyEnemD(self):
        colisiones = pygame.sprite.groupcollide(self.Proyectiles,self.enemigosD,True, False)
        for proyectil, enemigos in colisiones.items():
            for enem in enemigos:
                #Estructura para implementar enemigos con vida 
                self.datos["enemigosD"] = enem.destruir() if enem.destruir() else self.datos["enemigosD"]
    
        