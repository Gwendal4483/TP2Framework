
### **README.md**
```md
#  TP2 - Framework de Traitement de Données

Un framework de traitement de données permettant de **lire, filtrer, transformer et exporter des données** de manière automatisée et interactive à l'aide de fichiers **YAML/TOML**.  

---

##  **1. Installation et Pré-requis**

### ** Prérequis**
- **Python 3.8+**
- **Dépendances** : `pandas`, `pyyaml`, `toml`
- **Fichiers de configuration** en **YAML ou TOML** (dans `config/`)

### ** Cloner le projet**
```bash
git clone https://github.com/TonUtilisateur/TP2Framework.git
cd TP2Framework
```

### **🔹 Installer les dépendances**
```bash
pip install -r requirements.txt
```

---

##  **2. Fonctionnement du framework**
Le framework fonctionne avec une **pipeline définie en YAML ou TOML** qui contient :
- **Les données en entrée** (`input`)
- **Les transformations à appliquer** (`steps`)
- **L'exportation des résultats** (`output`)

L'utilisateur **choisit dynamiquement** :  
 **Le fichier de configuration** (YAML/TOML)  
 **Le fichier CSV à traiter**  

---

## **3. Lancer le framework**
Dans un terminal :
```bash
python framework/pipeline.py
```

### ** Processus interactif**
1️⃣ **Sélection du fichier de configuration**
```
📂 Fichiers de configuration disponibles :
  1. pipeline_1.yaml
  2. pipeline_2.toml
  3. pipeline_3.yaml

 Entrez le numéro du fichier à utiliser :
```

2️⃣ **Sélection du fichier CSV**
```
📂 Fichiers disponibles :
  1. transactions_2023.csv
  2. transactions_2024.csv
  3. ventes.csv

🔹 Entrez le numéro du fichier à utiliser :
```

3️⃣ **Exécution interactive de chaque étape**
```
📌 Exécution de l'étape : filter avec paramètres {'column': 'amount', 'condition': '> 500'}
Voulez-vous exécuter cette étape ? (y/n)
```

4️⃣ **Affichage du résultat et confirmation de l’export**
```
🔍 Aperçu des données après transformation :
   id  amount  category
0   1    1000  Shopping
1   3    2000  Restaurant

Le résultat vous convient-il ? (y/n)
```

---

## **4. Exemple de configuration**
### **`config/pipeline_1.yaml` (Filtrage & Groupement)**
```yaml
pipeline:
  input:
    type: csv
  steps:
    - filter:
        column: amount
        condition: "> 500"
    - group_by:
        column: category
        aggregation:
          amount: "mean"
  output:
    type: json
    file: data/result_pipeline_1.json
```
**Explication :**  
**Filtre les transactions où `amount > 500`**  
**Groupe par `category` et calcule la moyenne des montants**  
**Export en JSON (`result_pipeline_1.json`)**  

---

## 📂 **5. Organisation du projet**
```
TP2Framework/
│── framework/             # Module principal du framework
│   ├── __init__.py
│   ├── pipeline.py        # Gestion de l'exécution des pipelines
│   ├── config_loader.py   # Chargement des fichiers YAML/TOML
│   ├── readers.py         # Lecture des fichiers CSV/JSON
│   ├── transformers.py    # Transformations des données (filtrage, regroupement)
│   ├── exporters.py       # Exportation des résultats
│── config/                # Fichiers de configuration YAML/TOML
│── data/                  # Données sources et résultats
│── README.md              # Documentation du projet
│── requirements.txt       # Liste des dépendances
```


