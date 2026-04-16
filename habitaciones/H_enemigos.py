from habitaciones.H_base import Habitacion, Obstaculo
from entidades import EnemigoDistancia, EnemigoMelee, MiniBoss1,Proyectil

class HabitacionEnemigos(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)
        #Carga en  listas separadas todos los obstaculos, enemigos a melee y enemigos a la distancia del Json
        self.obstaculos = [Obstaculo(x,y) for x,y in datos["obstaculos"]]
        self.enemigosM = [EnemigoMelee(x,y) for x,y in datos["enemigosM"]]
        self.enemigosD = [EnemigoDistancia(x,y) for x,y in datos["enemigosD"]]
        self.miniBoss = []
    
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        eventos =[]
        # --- Enemigos Melee ---
        for e in self.enemigosM:
            #Colisiones jugador-enemigo
            if Jugador1.rect.colliderect(e.rect):
                Jugador1.x = WIDTH//2
                Jugador1.y = HEIGTH//2
                Jugador1.recibirDaño()
            for p in self.Proyectiles[:]:
                #Colision Jugador enemigo
                if p.rect.colliderect(e.rect):
                    self.Proyectiles.remove(p)
                    self.enemigosM.remove(e)
                    self.datos["enemigosM"] = self.enemigosM

        for e in self.enemigosM:
            e.update(dt, Jugador1)

        # --- Obstaculos ---
        for o in self.obstaculos:
            #Colision jugador-obstaculo
            if Jugador1.rect.colliderect(o.rect):
                Jugador1.x = WIDTH//2
                Jugador1.y = HEIGTH//2
                Jugador1.recibirDaño()
            for p in self.Proyectiles[:]:
                #Colision obstaculo-proyectil
                if p.rect.colliderect(o.rect):
                    self.obstaculos.remove(o)
                    self.Proyectiles.remove(p)
                    self.datos["obstaculos"] = self.obstaculos

        # --- Enemigos Distancia ---
        for e in self.enemigosD:
            if Jugador1.rect.colliderect(e.rect):
                Jugador1.x = WIDTH//2
                Jugador1.y = HEIGTH//2
                Jugador1.recibirDaño(1)
            for p in self.Proyectiles[:]:
                if p.rect.colliderect(e.rect):
                    self.enemigosD.remove(e)
                    self.Proyectiles.remove(p)
                    self.datos["enemigosD"] = self.enemigosD

        for e in self.enemigosD:
            proyectil = e.update(dt, Jugador1)
            if proyectil:
                self.Proyectiles.append(proyectil)

        # --- Colision proyectil -> jugador ---
        proyectiles_a_eliminar = []
        for p in self.Proyectiles:
            if p.rect.colliderect(Jugador1.rect):
                Jugador1.recibirDaño()
                proyectiles_a_eliminar.append(p)
        for p in proyectiles_a_eliminar:
            self.Proyectiles.remove(p)

        # --- Actualizar proyectiles ---
        for p in self.Proyectiles:
            p.update(dt)

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
                        self.Proyectiles.append(proyectil)
                if isinstance(e,EnemigoMelee):
                    enemigo = e
                    if enemigo:
                        self.enemigosM.append(e)

        #Para el miniBoss

        
        # --- Limpiar proyectiles fuera de pantalla ---
        self.Proyectiles = [p for p in self.Proyectiles if 0 <= p.x <= WIDTH and 0 <= p.y <= HEIGTH]

    def SpawnMiniBoss(self,mundo):
        if ( mundo == 1):
            self.miniBoss.append(MiniBoss1(400,300))
            
    def draw(self, screen):
        for o in self.obstaculos:
            o.draw(screen)
        for p in self.Proyectiles:
            p.draw(screen)
        for e in self.enemigosM:
            e.draw(screen)
        for e in self.enemigosD:
            e.draw(screen)
        for m in self.miniBoss:
            m.draw(screen)