#Ya implementamos diseño de niveles y manejo por escenas, por tanto main mas limpio y manejo de archivos
# pylint: disable=no-member
import pygame
import sys
from escenas import MainMenu
pygame.init()
pygame.display.set_caption('Naikan')
Width = 800
Heigth = 600
screen = pygame.display.set_mode((Width, Heigth))
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
    
    escena_principal = escena_principal.HandleEvents(events) 
    escena_principal = escena_principal.Update(dt,keys) or escena_principal
    escena_principal.draw(screen)

    pygame.display.update()
    
pygame.quit()
sys.exit()