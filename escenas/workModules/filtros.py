import pygame
import numpy as np
from escenas.UT_guardado import cargarConfig

class Filtros:
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
    
    observadores = []
    
    config = cargarConfig()
    filtro_actual = config["filtro"]

    @classmethod
    def unirse_lista(cls, sprite):
        if sprite not in cls.observadores:
            cls.observadores.append(sprite)
            sprite.configurar_filtro(cls.filtro_actual)

    @classmethod
    def quitarse_lista(cls, sprite):
        if sprite in cls.observadores:
            cls.observadores.remove(sprite)

    @classmethod
    def notificar_cambio(cls, nuevo_filtro):
        cls.filtro_actual = nuevo_filtro
        for sprite in cls.observadores:
            sprite.configurar_filtro(nuevo_filtro)

    @staticmethod
    def aplicar_filtro(imagen_original, tipo):
        if imagen_original is None:
            return None
        
        if tipo == "ninguno" or tipo not in Filtros.MATRICES:
            return imagen_original.copy()

        array_rgb = pygame.surfarray.pixels3d(imagen_original)
        
        matriz = Filtros.MATRICES[tipo]
        array_corregido = np.dot(array_rgb, matriz.T) 
        
        array_corregido = np.clip(array_corregido, 0, 255).astype(np.uint8)
        
        nueva_imagen = pygame.surfarray.make_surface(array_corregido)
        
        nueva_imagen = nueva_imagen.convert_alpha()
        alpha_original = pygame.surfarray.pixels_alpha(imagen_original)
        pygame.surfarray.pixels_alpha(nueva_imagen)[:,:] = alpha_original
        
        return nueva_imagen