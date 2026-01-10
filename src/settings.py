"""src/settings.py
Use the saved settings (Settings.yaml)
"""

from pathlib import Path
import yaml

# Project root = one folder above /src
ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = ROOT / "Settings.yaml"

with SETTINGS_PATH.open("r", encoding="utf-8") as f:
    config = yaml.safe_load(f) or {}

if __name__ == "__main__":
    import display
    display.draw_centered(str(f))
    display.draw_centered(str(config))