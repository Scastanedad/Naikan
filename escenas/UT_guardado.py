import json, os

BASE = os.path.dirname(os.path.dirname(__file__))  
RUTA_PROGRESO = os.path.join(BASE,"save","progreso.json")
RUTA_CONFIG   = os.path.join(BASE,"save", "config.json")

def cargarProgreso():
    with open(RUTA_PROGRESO, "r") as f:
        #Devuelve un diccionario de python
        return json.load(f)

def guardarProgreso(progreso):
    with open(RUTA_PROGRESO, "w") as f:
        #Carga al json el diccionario de python con sangria 4
        json.dump(progreso, f, indent=4)

def completarNivel(mundo: int, nivel: int):
    progreso = cargarProgreso()
    mundo_str = str(mundo)

    # Marcar este nivel como completado
    if nivel not in progreso["niveles_completados"][mundo_str]:
        progreso["niveles_completados"][mundo_str].append(nivel)

    # Desbloquear el siguiente
    if nivel < 4:
        siguiente = nivel + 1
        if siguiente not in progreso["niveles_desbloqueados"][mundo_str]:
            progreso["niveles_desbloqueados"][mundo_str].append(siguiente)
    else:
        # Era el nivel 4, desbloquear el siguiente mundo
        siguiente_mundo = mundo + 1
        if siguiente_mundo <= 4:
            sig_str = str(siguiente_mundo)
            if siguiente_mundo not in progreso["mundos_desbloqueados"]:
                progreso["mundos_desbloqueados"].append(siguiente_mundo)
            if 1 not in progreso["niveles_desbloqueados"][sig_str]:
                progreso["niveles_desbloqueados"][sig_str].append(1)

    guardarProgreso(progreso)

def cargarConfig():
    with open(RUTA_CONFIG, "r") as f:
        return json.load(f)

def guardarConfig(config):
    with open(RUTA_CONFIG, "w") as f:
        json.dump(config, f, indent=4)

def actualizarConfig(clave, valor):
    config = cargarConfig()
    config[clave] = valor
    guardarConfig(config)
    return config