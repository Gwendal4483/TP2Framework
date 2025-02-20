import yaml
import toml
from pathlib import Path

def load_config(file_path):
    """Charge un fichier YAML ou TOML et retourne son contenu sous forme de dictionnaire."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")

    if path.suffix == ".yaml" or path.suffix == ".yml":
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif path.suffix == ".toml":
        with open(file_path, "r", encoding="utf-8") as f:
            return toml.load(f)
    else:
        raise ValueError("Format de fichier non supporté. Utilisez YAML ou TOML.")

# Exemple d'utilisation
if __name__ == "__main__":
    config = load_config("config/exemple.yaml")
    print(config)
