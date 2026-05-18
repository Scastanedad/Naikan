import pygame
from G_utils import resource_path
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
        cls.SFX["click"] = pygame.mixer.Sound(resource_path("assets/sfx/click.ogg"))
        cls.SFX["bala"] = pygame.mixer.Sound(resource_path("assets/sfx/bala.ogg"))
        cls.SFX["melee_mundo1"] = pygame.mixer.Sound(resource_path("assets/sfx/mundo1/melee_mundo1.ogg"))
        cls.SFX["distancia_mundo1"] = pygame.mixer.Sound(resource_path("assets/sfx/mundo1/distancia_mundo1.ogg"))
        cls.SFX["melee_mundo2"] = pygame.mixer.Sound(resource_path("assets/sfx/mundo2/melee_mundo2.ogg"))
        cls.SFX["distancia_mundo2"] = pygame.mixer.Sound(resource_path("assets/sfx/mundo2/distancia_mundo2.ogg"))
        cls.SFX["melee_mundo3"] = pygame.mixer.Sound(resource_path("assets/sfx/mundo3/melee_mundo3.ogg"))
        cls.SFX["distancia_mundo3"] = pygame.mixer.Sound(resource_path("assets/sfx/mundo3/distancia_mundo3.ogg"))
        cls.SFX["melee_mundo4"] = pygame.mixer.Sound(resource_path("assets/sfx/mundo4/melee_mundo4.ogg"))
        #cls.SFX["distancia_mundo4"] = pygame.mixer.Sound("assets/sfx/mundo4/distancia_mundo4.ogg")
        cls.SFX["asamiDaño"] = pygame.mixer.Sound(resource_path("assets/sfx/asamirecibiendoimpacto.ogg"))
        cls.SFX["obstaculo"] = pygame.mixer.Sound(resource_path("assets/sfx/obstaculodestruido.ogg"))
        cls.SFX["impactoEnemigo"] = pygame.mixer.Sound(resource_path("assets/sfx/impactorecibidoenemigo.ogg"))
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
        ruta_archivo  = resource_path(ruta_archivo)
        pygame.mixer.music.load(ruta_archivo)
        cls.musica_preparada = ruta_archivo

    @classmethod
    def reproducir_musica(cls, ruta_archivo, tiempo_transicion=1000):
        ruta_archivo  = resource_path(ruta_archivo)
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
