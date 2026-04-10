# Naikan 🎮

**Naikan** es un roguelike 2D inspirado en *Cult of the Lamb* y *The Binding of Isaac*, ambientado en el mundo de las idols japonesas y la problemática del cyberbullying. Explora mazmorras, enfrenta enemigos y sobrevive en un mundo oscuro y estilizado.

---

## 🎯 Descripción

El jugador toma el rol de una idol que debe enfrentarse a los horrores del cyberbullying en un mundo inspirado en la cultura japonesa. Cada run es única gracias a la generación procedural de habitaciones y enemigos.

---

## 👥 Integrantes

| Nombre | Rol |
|---|---|
| Samuel Castañeda | Backend y lógica |
| Sebastián Blanco | Frontend y diseño |
| Santiago Lobo | Diseño de sonido y UI |
| Sebastián Sánchez | Creación de sprites |
| Juan Sierra | Diseño de niveles y mundos |

---

## ⚙️ Requisitos

- Windows 10/11
- Conexión a internet (solo para la instalación)
- Python 3.11.9 (el instalador lo descarga automáticamente si no lo tienes)

---

## 🚀 Instalación

1. Clona el repositorio con **GitHub Desktop**
2. Abre la carpeta del proyecto
3. Haz doble click en `setup.bat`
4. El script instala Python y pygame automáticamente
5. Una vez termine, corre el juego con:

```bash
python main.py
```

> ⚠️ Si el `setup.bat` instala Python por primera vez, te pedirá que lo cierres y lo vuelvas a abrir. Esto es normal.

---

## 🕹️ Controles

| Tecla | Acción |
|---|---|
| `W` `A` `S` `D` / Flechas | Moverse |
| `X` | Disparar |
| `Enter` | Confirmar / Volver al menú |
| `F` | Pantalla completa |

---

## 📁 Estructura del proyecto

```
Naikan/
├── entidades/       # Jugador, enemigos y proyectiles
├── escenas/         # Menú principal, juego y pantallas estáticas
├── habitaciones/    # Lógica de habitaciones (enemigos, curación)
├── mundos/          # Niveles en formato JSON
├── assets/          # Sprites, sonidos y cinemáticas (próximamente)
├── main.py          # Archivo principal
├── setup.bat        # Instalador automático para Windows
└── requirements.txt # Dependencias de Python
```

---

## 📦 Dependencias

- `pygame 2.5.2`

---

## 📌 Estado del proyecto

🚧 En desarrollo — Trabajo Final de Programación Orientada a Objetos
