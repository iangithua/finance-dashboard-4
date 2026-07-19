from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).resolve().parents[2]

def load_settings(path: str = "config/settings.yaml") -> dict:
    config_path = ROOT_DIR / path
    with open(config_path, "r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)
    return settings
