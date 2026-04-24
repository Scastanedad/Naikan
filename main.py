#Archivo Principal, no tiene mucha explicacion, 
# pylint: disable=no-member
import pygame
import sys
from escenas import MainMenu, EscenaBase
from escenas.UT_guardado import cargarConfig

pygame.init()
pygame.display.set_caption('Naikan')
config = cargarConfig()
estado_pantalla = config["pantalla_completa"]
sw = pygame.SCALED | pygame.RESIZABLE
if estado_pantalla:
    sw |= pygame.FULLSCREEN
screen = pygame.display.set_mode((EscenaBase.WIDTH, EscenaBase.HEIGTH), sw)
running = True
clock = pygame.time.Clock()
escena_principal = MainMenu()
   
while running:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    config_actual = cargarConfig() 
    if config_actual["pantalla_completa"] != estado_pantalla:
        pygame.display.toggle_fullscreen()
        estado_pantalla = config_actual["pantalla_completa"] 
    for event in events:
        if event.type == pygame.QUIT:
            running = False
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_f:
#               pygame.display.toggle_fullscreen()
    escena_principal = escena_principal.HandleEvents(events) 
    escena_principal = escena_principal.Update(dt,keys) or escena_principal
    escena_principal.draw(screen)
    pygame.display.update()
pygame.quit()
sys.exit()