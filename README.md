# The System

A Python-based desktop application inspired by the System from *Solo Leveling*. The project recreates its interface and progression mechanics, adapting them into a gamified approach to personal development, fitness, and productivity.

## Features

The application is divided into several independent interfaces, each accessible through the main System window.

- **Status** — Character profile and attribute tracking, including Strength, Agility, Vitality, Perception, and Intelligence.
- **Daily Quests** — Daily tasks and activity tracking.
- **Quests** — Quest management and progression.
- **Skills** — Skill management and upgrades.
- **Inventory** — Item storage and management.
- **Equipment** — Equipment management.
- **Shop** — In-application item purchasing.
- **Dungeons** — Dungeon interface.
- **Demon Castle** — Additional progression interface.
- **Fatigue** — Fatigue tracking and recovery.
- **Calories** — Calorie input and tracking.

The application also includes two visual themes based on the anime and manhwa adaptations of Solo Leveling.

## Interface

The GUI was designed in Figma and implemented using Tkinter, with Tkinter Designer used to translate the designs into Python interfaces.

## Technology

| Component | Technology |
|---|---|
| Language | Python |
| GUI | Tkinter |
| UI Design | Figma, Tkinter Designer |
| Image Processing | OpenCV, Pillow |
| Data Storage | JSON, CSV |
| Data Processing | Pandas, ujson |
| Background Processing | Python Threading |
| Speech Recognition | SpeechRecognition |

## Installation

**Platform:** Windows

Linux support is not currently provided.

### 1. Clone the repository

```bash
git clone https://github.com/Venexs/The-System.git
cd The-System
```

### 2. Install dependencies

Run the included installer:

```bat
installer.bat
```

Alternatively, install the required Python packages manually using the project's dependency list.

### 3. Launch

Run:

```bat
main.bat
```

Alternatively, launch `gui.py` directly using Python.

## Project Structure

```text
The-System/
│
├── Anime Version/       # Anime-themed interfaces
├── Manwha Version/      # Manhwa-themed interfaces
├── Files/               # Player data, settings and resources
├── First/               # Initial project resources
├── Fonts/               # Application fonts
├── Installer/           # Installation scripts
├── thesystem/            # Core system modules
├── assets/              # GUI assets
│
├── gui.py               # Main application interface
├── voice.py             # Voice command handling
├── update.py            # Application updater
├── npy_creator.py       # Image and video cache generation
├── installer.bat        # Dependency installer
├── main.bat             # Application launcher
└── Privacy Policy.md
```

## Data & Privacy

Player information and application settings are stored locally on the user's machine.

The application includes optional online functionality for updates and speech recognition. Refer to the [Privacy Policy](Privacy%20Policy.md) for further information.

## Contributing

Suggestions, bug reports, and improvements are welcome. For substantial changes, please open an issue before submitting a pull request.

