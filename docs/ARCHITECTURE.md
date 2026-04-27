# Architecture

## Overview

This repo is a small Pygame story game with a launcher. The launcher is the entry point for development and packaged builds.

## Components

- **Launcher** (`opener.py`)
  - Presents a home screen and level selector.
  - Starts Level 1 when selected.
- **Level 1** (`Cursed McDonalds 1/`)
  - Contains the game code/assets for the first level.
- **Packaging**
  - Windows and macOS builds are produced via PyInstaller (`Cursed McDonalds.spec`) and GitHub Actions.

## Runtime assumptions

- Python 3.11+ recommended for development.
- `pygame` is the only required dependency (`requirements.txt`).

