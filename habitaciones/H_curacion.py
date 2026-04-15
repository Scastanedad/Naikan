from habitaciones.H_base import Habitacion

class HabitacionCura(Habitacion):
    def __init__(self, datos):
        super().__init__(datos)

    def draw(self, screen):
        screen.fill((0,0,200))
    
    #Cuando entre a esta habitacion se curara
    def update(self, dt, keys, Jugador1, WIDTH, HEIGTH):
        if ( Jugador1.vida < 3):
            Jugador1.vida += 1
        
        
    

