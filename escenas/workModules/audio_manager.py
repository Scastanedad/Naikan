import pygame
from escenas.UT_guardado import cargarConfig
class AudioManager:
    SFX = {}
    musica_actual = None
    musica_preparada = None
    volumen_musica = 0.7
    volumen_sfx = 1.0

    @classmethod
    def inicializar(cls):
        config = cargarConfig()
        cls.volumen_musica = config.get("volumen_musica", 0.7)
        cls.volumen_sfx = config.get("volumen_sfx", 1.0)
        cls.SFX["click"] = pygame.mixer.Sound("assets/sfx/click.ogg")
        cls.SFX["bala"] = pygame.mixer.Sound("assets/sfx/bala.ogg")
        cls.SFX["melee_mundo1"] = pygame.mixer.Sound("assets/sfx/mundo1/melee_mundo1.ogg")
        cls.SFX["distancia_mundo1"] = pygame.mixer.Sound("assets/sfx/mundo1/distancia_mundo1.ogg")
        cls.aplicar_volumenes()

    @classmethod
    def reproducir_sfx(cls, nombre):
        if nombre in cls.SFX:
            cls.SFX[nombre].play()

    @classmethod
    def aplicar_volumenes(cls):
        pygame.mixer.music.set_volume(cls.volumen_musica)

        for sonido in cls.SFX.values():
            sonido.set_volume(cls.volumen_sfx)
    @classmethod
    def cambiar_volumen_musica(cls, volumen):
        cls.volumen_musica = max(0.0, min(1.0, volumen))
        pygame.mixer.music.set_volume(cls.volumen_musica)

    @classmethod
    def cambiar_volumen_sfx(cls, volumen):
        cls.volumen_sfx = max(0.0, min(1.0, volumen))

        for sonido in cls.SFX.values():
            sonido.set_volume(cls.volumen_sfx)
    @classmethod
    def preparar_musica(cls, ruta_archivo):
        pygame.mixer.music.load(ruta_archivo)
        cls.musica_preparada = ruta_archivo

    @classmethod
    def reproducir_musica(cls, ruta_archivo, tiempo_transicion=1000):
        if cls.musica_actual == ruta_archivo:
            return

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(tiempo_transicion)
            
        if cls.musica_preparada != ruta_archivo:
            pygame.mixer.music.load(ruta_archivo)
            
        pygame.mixer.music.load(ruta_archivo)
        pygame.mixer.music.play(loops=-1, fade_ms=tiempo_transicion)            
        cls.musica_actual = ruta_archivo
        cls.musica_preparada = None
