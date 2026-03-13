from clasesJ import EnemigoMelee, Obstaculo

class Habitacion():
    def __init__(self,datos):
        self.id = datos["id"]
        self.conexiones = datos["conexiones"]
        self.obstaculos = [Obstaculo(x,y) for x,y in datos["obstaculos"]]
        self.enemigos = [EnemigoMelee(x,y)for x,y in datos["enemigosM"]]
    
    def draw(self, screen):
        for o in self.obstaculos:
            o.draw(screen)