import pygame

def ManejoColisiones(hab,Jugador1):
    ColJugadorObstaculo(hab,Jugador1)
    ColObsProyectil(hab)
    ColProyEnemM(hab)
    ColEneMJugador(hab,Jugador1)
    ColProyEnemD(hab)
    ColJugadorProyectil(hab,Jugador1)
    ColJugadorMB(hab,Jugador1)
    ColProyMiniBoss(hab)

def ColJugadorObstaculo(hab,Jugador1):
    colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , hab.obstaculos, False) # type: ignore
    if colisiones:
        for obs in colisiones:
            hab.datos["obstaculos"] = obs.destruir()
        Jugador1.sprite.recibirDaño() # type: ignore

def ColObsProyectil(hab):
    colisiones = pygame.sprite.groupcollide(hab.Proyectiles, hab.obstaculos,True,False)
    for proyectil, obstaculos in colisiones.items():
        for obs in obstaculos:
            hab.datos["obstaculos"] = obs.destruir()

def ColProyEnemM(hab):
    colisiones = pygame.sprite.groupcollide(hab.Proyectiles,hab.enemigosM,True, False)
    for proyectil, enemigos in colisiones.items():
        for enem in enemigos:
            #Estructura para implementar enemigos con vida 
            hab.datos["enemigosM"] = enem.destruir() if enem.destruir() else hab.datos["enemigosM"]

def ColEneMJugador(hab,Jugador1):
    colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , hab.enemigosM, False) # type: ignore
    if colisiones:
        if (Jugador1.sprite.dañoCooldown >= 1):
            Jugador1.sprite.dañoCooldown = 0
            Jugador1.sprite.recibirDaño() # type: ignore

def ColProyEnemD(hab):
    colisiones = pygame.sprite.groupcollide(hab.Proyectiles,hab.enemigosD,True, False)
    for proyectil, enemigos in colisiones.items():
        for enem in enemigos:
            #Estructura para implementar enemigos con vida 
            hab.datos["enemigosD"] = enem.destruir() if enem.destruir() else hab.datos["enemigosD"]

def ColJugadorProyectil(hab,Jugador1):
    colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , hab.Proyectiles, False) # type: ignore
    if colisiones:
        for proyectil in colisiones:
            if proyectil.dueño != "jugador":
                proyectil.kill()
                Jugador1.sprite.recibirDaño() # type: ignore

def ColJugadorMB(hab,Jugador1):
    colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , hab.miniBoss, False) # type: ignore
    if colisiones:
        if (Jugador1.sprite.dañoCooldown >= 1):
            Jugador1.sprite.dañoCooldown = 0
            Jugador1.sprite.recibirDaño() # type: ignore

def ColProyMiniBoss(hab):
    colisiones = pygame.sprite.groupcollide(hab.Proyectiles, hab.miniBoss, False, False)
    for proyectil, enemigos in colisiones.items():
        if proyectil.grace_period > 0 and proyectil.dueño == "Boss":  # ignorar si está en grace period
            continue
        proyectil.kill()  # destruir el proyectil
        for enem in enemigos:
            enem.destruir(hab.miniBoss)

