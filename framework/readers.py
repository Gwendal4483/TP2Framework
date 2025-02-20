import pandas as pd
from pathlib import Path

def read_data(input_config):
    """Lit un fichier CSV ou JSON et retourne un DataFrame."""
    file_path = Path(input_config["file"])
    file_type = input_config["type"]

    if not file_path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")

    if file_type == "csv":
        return pd.read_csv(file_path)
    elif file_type == "json":
        return pd.read_json(file_path)
    else:
        raise ValueError("Format de fichier non supporté. Utilisez 'csv' ou 'json'.")

# Test rapide
if __name__ == "__main__":
    config = {"type": "csv", "file": "../data/test.csv"}
    df = read_data(config)
    print(df.head())  # Affiche les premières lignes
    