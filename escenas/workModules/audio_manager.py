import pygame

class AudioManager:
    SFX = {}
    musica_actual = None

    @classmethod
    def inicializar(cls):
        cls.SFX["click"] = pygame.mixer.Sound("assets/sfx/click.ogg")
        cls.SFX["bala"] = pygame.mixer.Sound("assets/sfx/bala.ogg")
        cls.SFX["melee_mundo1"] = pygame.mixer.Sound("assets/sfx/mundo1/melee_mundo1.ogg")
        cls.SFX["distancia_mundo1"] = pygame.mixer.Sound("assets/sfx/mundo1/distancia_mundo1.ogg")

    @classmethod
    def reproducir_sfx(cls, nombre):
        if nombre in cls.SFX:
            cls.SFX[nombre].play()

    @classmethod
    def reproducir_musica(cls, ruta_archivo, tiempo_transicion=1000):
        if cls.musica_actual == ruta_archivo:
            return

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(tiempo_transicion)
            
        pygame.mixer.music.load(ruta_archivo)
        pygame.mixer.music.play(loops=-1, fade_ms=tiempo_transicion)            
        cls.musica_actual = ruta_archivo
