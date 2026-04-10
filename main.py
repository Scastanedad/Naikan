#Archivo Principal, no tiene mucha explicacion, 
# pylint: disable=no-member
import pygame
import sys
from escenas import MainMenu, EscenaBase
pygame.init()
pygame.display.set_caption('Naikan')
juego_base = pygame.Surface((EscenaBase.WIDTH, EscenaBase.HEIGTH))
screen = pygame.display.set_mode((EscenaBase.WIDTH, EscenaBase.HEIGTH), pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()
escena_principal = MainMenu()   
while running:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_f:
               pygame.display.toggle_fullscreen()
    
    escena_principal = escena_principal.HandleEvents(events) 
    escena_principal = escena_principal.Update(dt,keys) or escena_principal
    escena_principal.draw(juego_base)
    screen.blit(pygame.transform.scale(juego_base, screen.get_size()), (0,0))
    pygame.display.update()
pygame.quit()
sys.exit()