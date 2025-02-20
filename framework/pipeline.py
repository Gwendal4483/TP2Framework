from config_loader import load_config

class Pipeline:
    def __init__(self, config_path):
        """Charge la configuration et initialise la pipeline."""
        self.config = load_config(config_path)
        self.steps = self.config.get("pipeline", {}).get("steps", [])

    def run(self, data):
        """Exécute chaque étape du pipeline sur les données."""
        for step in self.steps:
            step_name, params = list(step.items())[0]  # On récupère le nom et les paramètres de l'étape
            print(f"Exécution de l'étape : {step_name} avec paramètres {params}")
            #TO DO

        print("Pipeline terminée avec succès !")

# Exemple d'utilisation
if __name__ == "__main__":
    pipeline = Pipeline("config/exemple.yaml")
    pipeline.run(None)  # Pour l'instant, on ne traite pas encore de données