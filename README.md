# Ali — Autonomous Robotics Platform

Ali is a safety-first robotics software project. Development starts with a deterministic desktop simulator and modular Python components, then grows toward real sensors and motor controllers only after hardware is available.

> **Current stage:** software simulation and navigation foundation. This repository does not make a phone or laptop move a physical robot by itself. Real motion requires a compatible controller, motor driver, motors, power system, emergency stop, and appropriate sensors.

## What is included
- Interactive Tkinter grid simulator
- A* path planning with diagonal corner-cut prevention
- Explicit robot state and command limits
- Hardware interface with a safe dry-run backend (no real motor output)
- Optional camera adapter boundary; OpenCV is not required for simulation
- Unit tests and GitHub Actions CI
- Configuration and safety notes

## Requirements
- Python 3.11+
- Windows, macOS, or Linux with Tkinter available
- No paid services or API keys required

## Run on Windows
1. Install Python from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Download this repository using **Code → Download ZIP**, then extract it.
3. Double-click `Run-Ali.bat`, or open PowerShell in the extracted folder and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m ali
```

If PowerShell blocks activation, run `.venv\Scripts\python.exe -m ali` after installing dependencies.

## Simulator controls
- Left click: set the destination
- Right click: toggle an obstacle
- Space: pause/resume
- R: reset the map
- Arrow keys: move one cell manually (only if safe)

## Tests
```powershell
python -m pytest
```

## Project layout
```
src/ali/
  __main__.py       CLI entry point
  app.py            simulator UI
  config.py         validated configuration
  core/             robot state and command models
  navigation/       grid world and A* planner
  control/          bounded command generation
  hardware/         safe hardware abstraction / dry run
  vision/           optional camera adapter boundary
tests/
config/
docs/
.github/workflows/
```

## Safety
- The default motor backend is dry-run and cannot actuate hardware.
- Do not connect real motors until an emergency stop, hardware watchdog, power isolation, and a tested driver are in place.
- Never rely on software alone as the only emergency stop.
- Camera input and hardware control are deliberately separate from the simulator.
- Do not test autonomous motion around people, pets, stairs, roads, or fragile objects.

## Roadmap
1. Validate simulator and planning tests.
2. Add a sensor abstraction and recorded-image tests.
3. Select the physical platform and controller based on budget and availability.
4. Implement a hardware-specific driver with watchdog and physical emergency stop.
5. Add localization, obstacle sensing, and closed-loop motion with staged safety tests.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/SAFETY.md](docs/SAFETY.md).
