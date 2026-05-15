import pygame

def ManejoColisiones(hab,Jugador1,mundo):
    ColJugadorObstaculo(hab,Jugador1)
    ColObsProyectil(hab)
    ColProyEnemM(hab)
    ColEneMJugador(hab,Jugador1,mundo)
    ColProyEnemD(hab)
    ColJugadorProyectil(hab,Jugador1)
    ColJugadorMB(hab,Jugador1)
    ColProyMiniBoss(hab)
    ColJugadorB(hab,Jugador1)
    ColProyBoss(hab)

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

def ColEneMJugador(hab,Jugador1, mundo):
    colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , hab.enemigosM, False) # type: ignore
    if colisiones:
        if (Jugador1.sprite.dañoCooldown >= 1):
            for enemigo in colisiones: 
                from escenas.workModules.audio_manager import AudioManager
                AudioManager.reproducir_sfx("melee_mundo{mundo}") 
                Jugador1.sprite.dañoCooldown = 0
                Jugador1.sprite.y -= 50
                Jugador1.sprite.x -= 50
                Jugador1.sprite.actualizarRect()
                enemigo.y += 50
                enemigo.x += 50
                enemigo.actualizarRect()
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

def ColJugadorB(hab,Jugador1):
    colisiones = pygame.sprite.spritecollide(Jugador1.sprite  , hab.Boss, False) # type: ignore
    if colisiones:
        if (Jugador1.sprite.dañoCooldown >= 1):
            Jugador1.sprite.dañoCooldown = 0
            Jugador1.sprite.recibirDaño() # type: ignore


def ColProyBoss(hab):
    colisiones = pygame.sprite.groupcollide(hab.Proyectiles, hab.Boss, False, False)
    for proyectil, enemigos in colisiones.items():
        if proyectil.grace_period > 0 and proyectil.dueño == "Boss":  # ignorar si está en grace period
            continue
        proyectil.kill()  # destruir el proyectil
        for enem in enemigos:
            enem.destruir(hab.Boss)

