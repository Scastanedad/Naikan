from escenas.ES_base import EscenaBase
import os, json, pygame
from habitaciones import HabitacionEnemigos, HabitacionCura, HabitacionGema, HabitacionSobrevivir  # type: ignore
from entidades import Jugador, Proyectil
from G_utils import resource_path
from escenas.workModules.asset_manager import AssetManager
from escenas.CO_victoria import (
    MatarTodosEnemigos,
    MiniBoss,
    RecogerGema,
    SobrevivirTiempo,
    Boss,
)
from escenas.UT_guardado import completarNivel
from escenas.UT_guardado import cargarConfig
from escenas.workModules.icono import Icono


# Esta clase es la que trae el json a un diccionario de python
# El que carga el nivel es el hub
def CargarNivel(NumeroNivel, MundoActual):
    base = os.path.dirname(__file__)
    ruta = os.path.abspath(os.path.join(
        base,
        "..",
        "mundos",
        f"mundo{MundoActual}",
        "niveles",
        f"nivel{NumeroNivel}.json",
    ))
    ruta = resource_path(ruta)
    with open(ruta, "r") as archivo:
        raw = json.load(archivo)
    return {
        "mundo": raw["mundo"],
        "habitacion_inicial": raw["habitacion_inicial"],
        "cond_victoria": raw["cond_victoria"],
        "c_hab": raw["cantidad_hab"],
        # Cargamos las caracteristicas de las habitaciones en un diccionario que tiene como clave el id
        "habitaciones": {h["id"]: h for h in raw["habitaciones"]},
    }


# Con esta clase definimos que tipo de habitacion vamos a retornar
def ManejoHabitaciones(TipoHab, DatosHabitacion, mundo,iniciado = None):
    match TipoHab:
        case "HabitacionEnemigo":
            return HabitacionEnemigos(DatosHabitacion, mundo,iniciado)
        case "HabitacionCura":
            return HabitacionCura(DatosHabitacion,mundo,iniciado)
        case "HabitacionGema":
            return HabitacionGema(DatosHabitacion,mundo,iniciado)
        case "HabitacionSobrevivir":
            return HabitacionSobrevivir(DatosHabitacion, mundo,iniciado)
        case _:
            return print("Tipo de habitacion no valida")


# Que condicion de victoria vamos a utilizar
def ManejoCondicionVictoria(DatosNivel, t=None):
    cond_v = DatosNivel["cond_victoria"]
    match cond_v:
        case "MatarTodos":
            return MatarTodosEnemigos(DatosNivel)
        case "MiniBoss":
            return MiniBoss(DatosNivel)
        case "Boss":
            return Boss(DatosNivel)
        case "Gema":
            return RecogerGema(DatosNivel)
        case "SobrevivirTiempo":
            return SobrevivirTiempo(t)


# Es la escena que renderiza las habitaciones
class EscenaJuego(EscenaBase):
    def __init__(
        self,
        numeroNivel,
        mundoActual,
        habitacion_id=None,
        vida=3,
        x=None,
        y=None,
        currentData=None,
    ):
        # Si el nivel esta en progreso, se carga el diccionario modificado, si es la primera vez se accede al diccionario del json
        self.mundoActual = mundoActual
        self.numeroNivel = numeroNivel
        self.nivel = (
            currentData if currentData else CargarNivel(numeroNivel, mundoActual)
        )
        if self.nivel.get("iniciado") is None:
            self.nivel["iniciado"] = 1
        elif self.nivel.get("iniciado") is not None:
            self.nivel["iniciado"] = 2


        # Si es un nivel con miniBoss
        if (
            self.nivel["cond_victoria"] == "MiniBoss"
            and "miniboss_spawned" not in self.nivel
        ):
            self.nivel["miniboss_spawned"] = False
            self.nivel["miniboss_muerto"] = False
        if self.nivel["cond_victoria"] == "Boss" and "boss_spawned" not in self.nivel:
            self.nivel["boss_spawned"] = False
            self.nivel["boss_muerto"] = False

        # Dependiendo de si esta en progreso o no se accede a determinada habitacion
        habitacion_ACT = (
            habitacion_id if habitacion_id else self.nivel["habitacion_inicial"]
        )
        self.habitacion = ManejoHabitaciones(
            self.nivel["habitaciones"][habitacion_ACT]["tipoHab"],
            self.nivel["habitaciones"][habitacion_ACT],
            self.mundoActual, self.nivel["iniciado"]
        )
        self.numeroNivel = numeroNivel

        from escenas.workModules.audio_manager import AudioManager

        if self.nivel.get("boss_spawned", False) or self.nivel.get(
            "miniboss_spawned", False
        ):
            ruta_musica = f"assets/musica/mundo{self.mundoActual}/boss_mundo{self.mundoActual}.ogg"
        else:
            ruta_musica = f"assets/musica/mundo{self.mundoActual}/habitacion_mundo{self.mundoActual}.ogg"

        AudioManager.reproducir_musica(resource_path(ruta_musica))

        if self.nivel["cond_victoria"] in ["Boss", "MiniBoss"]:
            if not self.nivel.get("boss_spawned", False) and not self.nivel.get(
                "miniboss_spawned", False
            ):
                ruta_boss_precarga = f"assets/musica/mundo{self.mundoActual}/boss_mundo{self.mundoActual}.ogg"
                AudioManager.preparar_musica(resource_path(ruta_boss_precarga))

        # Para que las transciciones entre habitaciones tengan logica dimensional( Si bajo aparezco en la parte de arriba y asi)
        if x is not None and y is not None:
            self.Jugador1 = Jugador(x, y)
        else:
            self.Jugador1 = Jugador(self.WIDTH // 2, self.HEIGTH // 2)
        self.Jugador1.vida = vida
        self.grupoJugador = pygame.sprite.GroupSingle(self.Jugador1)  # type: ignore

        imagen_corazon = AssetManager.get_image(resource_path("assets/sprites/jugador/corazon.png"))
        imagen_corazon = pygame.transform.scale(imagen_corazon, (25, 25))
        self.icono_corazon = Icono(0, 0, imagen_corazon)
        imagen_puerta = AssetManager.get_image(resource_path(f"assets/tiles/mundo{self.mundoActual}/PuertaMundo{self.mundoActual}.png"))
        self.imagen_fuente = AssetManager.get_image(resource_path("assets/tiles/fuente.png"))
        self.imagen_fuente = pygame.transform.scale(self.imagen_fuente,(200,200))
        imagen_puertaDerecha = pygame.transform.rotate(imagen_puerta, 90)
        imagen_puertaArriba = pygame.transform.rotate(imagen_puerta, 0)     
        imagen_puertaIzquierda = pygame.transform.rotate(imagen_puerta, 270)
        self.icono_puertaAbajo = Icono(self.WIDTH//2, self.HEIGTH//2, imagen_puerta)
        self.icono_puertaDerecha = Icono(self.WIDTH//2, self.HEIGTH//2, imagen_puertaDerecha)
        self.icono_puertaIzquierda = Icono(self.WIDTH//2, self.HEIGTH//2, imagen_puertaIzquierda)
        self.icono_puertaArriba = Icono(self.WIDTH//2, self.HEIGTH//2, imagen_puertaArriba)
        ruta_base = f"assets/tiles/mundo{self.mundoActual}/fondo{self.mundoActual}.png"
        ruta_final =resource_path(ruta_base)

            
        imagen_original = AssetManager.get_image(ruta_final)
        
        self.fondo_original = pygame.transform.scale(imagen_original, (800, 600))
        
        self.fondo_integrado = self.fondo_original.copy()

        from escenas.workModules.filtros import Filtros
        Filtros.unirse_lista(self)    
        
        """ imagen_original = AssetManager.get_image(ruta_final)
        
        self.fondo_integrado = pygame.transform.scale(imagen_original, (800,600)) """
        
    def configurar_filtro(self, nuevo_filtro):
        from escenas.workModules.filtros import Filtros
        if hasattr(self, 'fondo_original') and self.fondo_original is not None:
            self.fondo_integrado = Filtros.aplicar_filtro(self.fondo_original, nuevo_filtro)

    def HandleEvents(self, events):
        configuracion = cargarConfig()
        tecla_disparo = configuracion["teclas"]["disparo"]

        for event in events:
            if tecla_disparo == 430:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    from escenas.workModules.audio_manager import AudioManager

                    AudioManager.reproducir_sfx("bala")
                    self.habitacion.Proyectiles.add(Proyectil(self.Jugador1.x + self.Jugador1.direccion[0] * 30, self.Jugador1.y + self.Jugador1.direccion[1] * 30, self.Jugador1.direccion, 600, 1, (0, 0, 200), "jugador", self.Jugador1.sprite_bala))  # type: ignore

            else:
                if event.type == pygame.KEYDOWN and event.key == tecla_disparo:
                    from escenas.workModules.audio_manager import AudioManager

                    AudioManager.reproducir_sfx("bala")
                    self.habitacion.Proyectiles.add(Proyectil(self.Jugador1.x + self.Jugador1.direccion[0] * 30, self.Jugador1.y + self.Jugador1.direccion[1] * 30, self.Jugador1.direccion, 600, 1, (0, 0, 200), "jugador", self.Jugador1.sprite_bala))  # type: ignore

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # from escenas.ES_estaticas import MainMenu
                    from escenas.estaticas import Menu_Pausa

                    return Menu_Pausa(self)
        return self

    def Update(self, dt, keys):

        self.grupoJugador.update(dt, keys, self.WIDTH, self.HEIGTH)
        self.habitacion.update(dt, keys, self.grupoJugador, self.WIDTH, self.HEIGTH)  # type: ignore
        match self.nivel["cond_victoria"]:
            case "MatarTodos":
                if ManejoCondicionVictoria(self.nivel):
                    completarNivel(self.mundoActual, self.numeroNivel)
                    from escenas.estaticas import EndGame

                    return EndGame(self.numeroNivel, self.mundoActual)
            case "Gema":
                if type(self.habitacion) == HabitacionGema:
                    if self.habitacion.datos["gema_recogida"] == 1:
                        completarNivel(self.mundoActual, self.numeroNivel)
                        from escenas.estaticas import EndGame

                        return EndGame(self.numeroNivel, self.mundoActual)
            case "SobrevivirTiempo":
                if ManejoCondicionVictoria(self.nivel, self.habitacion.timer):  # type: ignore
                    completarNivel(self.mundoActual, self.numeroNivel)
                    from escenas.estaticas import EndGame

                    return EndGame(self.numeroNivel, self.mundoActual)
            case "MiniBoss":
                if self.nivel["miniboss_spawned"] == False:
                    if (ManejoCondicionVictoria(self.nivel) == "spawnear") and (
                        type(self.habitacion) != HabitacionCura
                    ):
                        self.nivel["miniboss_spawned"] = True
                        self.habitacion.conexiones = {"arriba": None, "abajo": None, "izquierda": None, "derecha": None}  # type: ignore
                        self.habitacion.SpawnMiniBoss(self.nivel["mundo"])  # type: ignore

                        """ from escenas.workModules.audio_manager import AudioManager
                        ruta_musica = f"assets/musica/mundo{self.mundoActual}/miniboss_mundo{self.mundoActual}.ogg"
                        AudioManager.reproducir_musica(ruta_musica) """

                if (self.nivel["miniboss_spawned"] == True) and (len(self.habitacion.miniBoss) == 0):  # type: ignore
                    completarNivel(self.mundoActual, self.numeroNivel)
                    from escenas.estaticas import EndGame

                    return EndGame(self.numeroNivel, self.mundoActual)
            case "Boss":
                if self.nivel["boss_spawned"] == False:
                    if (ManejoCondicionVictoria(self.nivel) == "spawnear") and (
                        type(self.habitacion) != HabitacionCura
                    ):
                        self.nivel["boss_spawned"] = True
                        self.habitacion.conexiones = {"arriba": None, "abajo": None, "izquierda": None, "derecha": None}  # type: ignore
                        self.habitacion.SpawnBoss(self.nivel["mundo"])  # type: ignore

                        from escenas.workModules.audio_manager import AudioManager

                        ruta_musica = f"assets/musica/mundo{self.mundoActual}/boss_mundo{self.mundoActual}.ogg"
                        AudioManager.reproducir_musica(resource_path(ruta_musica))

                if (self.nivel["boss_spawned"] == True) and (len(self.habitacion.Boss) == 0):  # type: ignore
                    completarNivel(self.mundoActual, self.numeroNivel)
                    from escenas.estaticas import EndGame

                    return EndGame(self.numeroNivel, self.mundoActual)
            case _:
                if ManejoCondicionVictoria(self.nivel):
                    completarNivel(self.mundoActual, self.numeroNivel)
                    from escenas.estaticas import EndGame

                    return EndGame(self.numeroNivel, self.mundoActual)

        # Manejo de conexiones entre habitaciones, en el diccionario se establece hacia donde puede ir, y si esta en la puerta para ir hasta alla, se accede y ya
        conexiones = self.habitacion.conexiones  # type: ignore
        if (
            self.Jugador1.y <= 40
            and conexiones["arriba"] is not None
            and (self.Jugador1.x > 380 and self.Jugador1.x < 420)
        ):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            from escenas.workModules.filtros import Filtros
            Filtros.quitarse_lista(self)
            return EscenaJuego(
                self.numeroNivel,
                self.mundoActual,
                conexiones["arriba"],
                self.Jugador1.vida,
                self.Jugador1.x,
                self.HEIGTH - 60,
                self.nivel,
            )  
        if (
            self.Jugador1.y >= (self.HEIGTH - 60)
            and conexiones["abajo"] is not None
            and (self.Jugador1.x > 380 and self.Jugador1.x < 420)
        ):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            return EscenaJuego(
                self.numeroNivel,
                self.mundoActual,
                conexiones["abajo"],
                self.Jugador1.vida,
                self.Jugador1.x,
                60,
                self.nivel,
            ) 
        if (
            self.Jugador1.x <= 40
            and conexiones["izquierda"] is not None
            and (self.Jugador1.y > 280 and self.Jugador1.y < 320)
        ):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            return EscenaJuego(
                self.numeroNivel,
                self.mundoActual,
                conexiones["izquierda"],
                self.Jugador1.vida,
                self.WIDTH - 60,
                self.Jugador1.y,
                self.nivel,
            ) 
        if (
            self.Jugador1.x >= (self.WIDTH - 40)
            and conexiones["derecha"] is not None
            and (self.Jugador1.y > 280 and self.Jugador1.y < 320)
        ):
            self.nivel["habitaciones"][str(self.habitacion.id)] = self.habitacion.datos  # type: ignore
            return EscenaJuego(
                self.numeroNivel,
                self.mundoActual,
                conexiones["derecha"],
                self.Jugador1.vida,
                60,
                self.Jugador1.y,
                self.nivel,
            )  
        # Si se muere da pantalla final
        if self.Jugador1.vida <= 0:
            from escenas.estaticas import DeadScreen

            return DeadScreen(self.numeroNivel, self.mundoActual)

        return self

    def draw(self, screen):
        screen.blit(self.fondo_integrado, (0, 0))
        conexiones = self.habitacion.conexiones
        self.habitacion.draw(screen)
        if isinstance(self.habitacion, HabitacionCura):
            screen.blit(self.imagen_fuente, ((self.WIDTH // 2 +20) - (self.imagen_fuente.get_width() // 2), (self.HEIGTH // 2) - (self.imagen_fuente.get_height() // 2)))
        if isinstance(self.habitacion, HabitacionGema):
            pass
        ancho_puerta = self.icono_puertaArriba.image.get_width()
        alto_puerta  = self.icono_puertaAbajo.image.get_height()

        if conexiones["arriba"] is not None:
            screen.blit(self.icono_puertaArriba.image, (412 - ancho_puerta // 2, 0))

        if conexiones["abajo"] is not None:
            print("hey")
            screen.blit(self.icono_puertaAbajo.image, (412 - ancho_puerta // 2, self.HEIGTH - alto_puerta))

        if conexiones["derecha"] is not None:
            
            alto_d = self.icono_puertaDerecha.image.get_height()
            ancho_d = self.icono_puertaDerecha.image.get_width()
            screen.blit(self.icono_puertaDerecha.image, (self.WIDTH - ancho_d, 305 - alto_d // 2))

        if conexiones["izquierda"] is not None:
            alto_i = self.icono_puertaIzquierda.image.get_height()
            screen.blit(self.icono_puertaIzquierda.image, (0, 295 - alto_i // 2))

        self.grupoJugador.draw(screen)
        for i in range(self.Jugador1.vida):
            pos_x = 10 + (30 * i)
            screen.blit(self.icono_corazon.image, (pos_x, 10))
