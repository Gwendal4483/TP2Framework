from framework.config_loader import load_config
from framework.readers import read_data
from framework.transformers import filter_data, group_by_column
from framework.exporters import export_data

def verif(question, default="yes"):
        """Pose une question Oui/Non à l'utilisateur. Permet la confirmation de chaque étape"""
        while True:
            choice = input(f"{question} (y/n) ").strip().lower()
            if choice in ["y", "yes"]:
                return True
            elif choice in ["n", "no"]:
                return False
            elif choice == "" and default:
                return default == "yes"
            print("Veuillez répondre par 'y' ou 'n'.")


class Pipeline:
    def __init__(self):

        """Demande à l'utilisateur s'il veut utiliser un fichier YAML ou TOML."""
        while True:
            file_type = input("Voulez-vous charger un fichier YAML ou TOML ? (yaml/toml) ").strip().lower()
            if file_type in ["yaml", "toml"]:
                break
            print("Format invalide. Veuillez entrer 'yaml' ou 'toml'.")
        config_path = f"config/exemple.{file_type}"

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


            if not verif(f"Voulez-vous exécuter l'étape '{step_name}' avec paramètres {params} ?"):#ON DEMANDE CONFIRMATION AVANT CHAQUE ETAPE
                print(f"⏩ Étape '{step_name}' ignorée.")
                continue

            print(f"Exécution de l'étape : {step_name} avec paramètres {params}")

            if step_name == "filter":#si c'est un filtre
                data = filter_data(data, params["column"], params["condition"])

            elif step_name == "group_by":#si c'est un groupement
                data = group_by_column(data, params["column"], params["aggregation"])

        print("Pipeline terminée avec succès !")
        print("Aperçu des données après transformation :  ")
        print(data.head())

        if not verif("Le résultat vous convient-il ?"):#ON DEMANDE LA VALIDATION DU RESULTAT
            print("Pipeline arrêtée.")
            return

        print(f"Le fichier prévu pour l'export est : {self.output_config['file']}")
        if not verif("Ce chemin vous convient-il ?"):
            new_path = input("Entrez le nouveau chemin de sortie : ").strip()
            self.output_config["file"] = new_path

        #on exporte les données
        export_data(data, self.output_config)



        
        

# Exemple d'utilisation
if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()  