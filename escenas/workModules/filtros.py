import pygame

class Filtros:
    FILTROS = {
        "Protanopia": (0.567, 0.433, 0), 
        "Deuteranopia": (0.625, 0.375, 0), 
        "Tritanopia": (0.95, 0.05, 0), 
        "Ninguno": None
    }

    @staticmethod
    def aplicar_filtro(imagen_original, tipo):
        if tipo == "Ninguno" or tipo not in Filtros.FILTROS:
            return imagen_original.copy()

        copia_imagen = imagen_original.copy()

        superficie = pygame.Surface(copia_imagen.get_size()).convert_alpha()
        
        color_tinte = Filtros.FILTROS[tipo]
        
        superficie.fill(color_tinte)
        
        copia_imagen.blit(superficie, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        return copia_imagen