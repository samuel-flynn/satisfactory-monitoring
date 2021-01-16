# satisfactory-monitoring
A process for monitoring the logs of Satisfactory, by Coffee Stain Studios, and sending alerts whenever certain conditions arise that may break multiplayer sessions

## Quick Start

## Development Setup
### Install build tools

`python -m venv .venv`

`./.venv/Scripts/activate`

`python -m pip install -r dev-requirements.txt`

### Run the build

`python -m build -sw`

### Install runtime dependencies

1. Run the build at least once

2. `python -m pip install -r satisfactory_monitoring.egg-info/requires.txt`