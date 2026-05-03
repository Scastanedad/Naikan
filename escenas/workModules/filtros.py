import pygame
import numpy as np
from escenas.UT_guardado import cargarConfig

class Filtros:
    #Matrices para cambiar los valores de RGB
    MATRICES = {
        "protanopia": np.array([
            [0.0, 1.051, -0.051],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]),
        "deuteranopia": np.array([
            [1.0, 0.0, 0.0],
            [0.951, 0.0, 0.049],
            [0.0, 0.0, 1.0]
        ]),
        "tritanopia": np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [-0.86, 1.86, 0.0]
        ])
    }
    
    #Lista de observadores
    observadores = []
    
    #Para saber siempre cual es el filtro puesto en la configuración
    config = cargarConfig()
    filtro_actual = config["filtro"]

    @classmethod
    def unirse_lista(cls, sprite):
        if sprite not in cls.observadores:
            cls.observadores.append(sprite)
            sprite.configurar_filtro(cls.filtro_actual) #Se une el objeto a la lista y se pone el filtro seleccionado

    @classmethod
    def quitarse_lista(cls, sprite):
        if sprite in cls.observadores:
            cls.observadores.remove(sprite) #Se elimina al objeto de la lista una vez es destruido

    @classmethod
    def notificar_cambio(cls, nuevo_filtro):
        cls.filtro_actual = nuevo_filtro
        for sprite in cls.observadores:
            sprite.configurar_filtro(nuevo_filtro) #Cuando se cambia la configuración se le avisa a todos los observadores

    @staticmethod
    def aplicar_filtro(imagen_original, tipo):
        if imagen_original is None: #Si no existe una imagen del objeto, no se hace nada (para evitar errores en los constructores)
            return None
        
        if tipo == "ninguno" or tipo not in Filtros.MATRICES: #En caso de no tener un filtro aplicado se deja la imagen como está
            return imagen_original.copy()

        array_rgb = pygame.surfarray.pixels3d(imagen_original) #Se obtieen los RGB de la imagen en una matriz
        
        matriz = Filtros.MATRICES[tipo] #Se obtiene la matriz de cambio de RGB dado el caso
        array_corregido = np.dot(array_rgb, matriz.T) #Se multiplican las matrices
        
        array_corregido = np.clip(array_corregido, 0, 255).astype(np.uint8) #Se "capea" los valores para que no salgan de los rangos y se formatean en valores estandares para el computador
        
        nueva_imagen = pygame.surfarray.make_surface(array_corregido)  #Se crea una nueva superficie con los colores
        
        nueva_imagen = nueva_imagen.convert_alpha() #Se le añade la capacidad de tener alpha
        alpha_original = pygame.surfarray.pixels_alpha(imagen_original) #Se obtiene el alpha original
        pygame.surfarray.pixels_alpha(nueva_imagen)[:,:] = alpha_original #Se le inyecta
        
        return nueva_imagen