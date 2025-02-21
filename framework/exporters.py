import pandas as pd

def export_data(df, output_config):
    """
    Permet d'exporter les données dans un fichier CSV ou JSON (c'est précisé dans le .yaml ou /toml).
    
    - `df` : DataFrame contenant les données transformées
    - `output_config` : dictionnaire YAML/TOML contenant :
        - type : "csv" ou "json"
        - file : chemin du fichier de sortie
    """
    file_path = output_config["file"]
    file_type = output_config["type"]

    if file_type == "csv":
        df.to_csv(file_path, index=False, encoding="utf-8")
    elif file_type == "json":
        df.to_json(file_path, orient="records", indent=4)
    else:
        raise ValueError("Format non supporté. Utilisez 'csv' ou 'json'.")

    print(f"Fichier exporté dans : {file_path}")
