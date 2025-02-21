from config_loader import load_config
from readers import read_data
from transformers import filter_data, group_by_column
from exporters import export_data


class Pipeline:
    def __init__(self, config_path):
        """Charge la configuration et initialise la pipeline."""
        self.config = load_config(config_path)
        self.steps = self.config.get("pipeline", {}).get("steps", [])
        self.input_config = self.config.get("pipeline", {}).get("input", {})
        self.output_config = self.config.get("pipeline", {}).get("output", {})


    def run(self):
        """Exécute chaque étape du pipeline sur les données."""
        data = read_data(self.input_config)#on charge les données
        for step in self.steps:#pour chaque étape dans le .yaml ou .tolml
            step_name, params = list(step.items())[0]  # On récupère le nom et les paramètres de l'étape
            print(f"Exécution de l'étape : {step_name} avec paramètres {params}")

            if step_name == "filter":#si c'est un filtre
                data = filter_data(data, params["column"], params["condition"])

            elif step_name == "group_by":#si c'est un groupement
                data = group_by_column(data, params["column"], params["aggregation"])

        print("Pipeline terminée avec succès !")
        print("Le .CSV contiendra ces valeurs :  ")
        print(data.head())

        export_data(data, self.output_config)


        

# Exemple d'utilisation
if __name__ == "__main__":
    pipeline = Pipeline("config/exemple.yaml")
    pipeline.run()  # Pour l'instant, on ne traite pas encore de données