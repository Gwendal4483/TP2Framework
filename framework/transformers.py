import pandas as pd

def filter_data(df, column, condition):
    """
    Filtre les données d'un DataFrame en fonction d'une condition.

    - Comparaisons numériques : `>`, `<`, `>=`, `<=`, `=`
    - Comparaisons texte : `is`, `!=`, `contains`, `startswith`, `endswith`
    - Détection automatique des colonnes numériques / textuelles
    """
    
    condition = condition.strip()  # Nettoyer la condition

     # Vérifier si la colonne existe dans le DataFrame
    if column not in df.columns:
        raise ValueError(f"La colonne '{column}' n'existe pas dans les données.")




    # Vérifier si c'est une comparaison numérique
    if condition.startswith((">", "<", "=")):  
        operator = condition[:1] if condition[:2] not in (">=", "<=") else condition[:2] #on regarde si c'est <= ou >= ou autre chose
        value = condition[len(operator):].strip().strip("'\"")  # on retire les guillemets ou les / pour pouvoir traiter le filtre
        
        # Vérifier si la colonne est numérique
        is_numeric = pd.api.types.is_numeric_dtype(df[column])
        
        if is_numeric: #si c'est un nombre apres l'opérateur
            try:
                value = float(value)  # Convertir en nombre
                filtered_df = df.query(f"{column} {operator} @value")
                return filtered_df if not filtered_df.empty else pd.DataFrame(columns=df.columns)
            
            except Exception as e: #on a une erreur si le dataframe est vide, si aucune colonne ne réponds aux filtres entrés
                print(f"⚠️ Erreur lors de l'application du filtre {condition} : {e}")
                return pd.DataFrame(columns=df.columns)
        else:
            raise ValueError(f"L'opérateur '{operator}' est réservé aux valeurs numériques.")#si ce n'est pas un nombre apres l'opérateur alors ça ne fonctionne pas
        


    # Comparaisons pour les chaînes de caractères
    elif condition.startswith(("is", "!=", "contains", "startswith", "endswith")):
        parts = condition.split(" ", 1)  # Séparer l'opérateur et la valeur

        if len(parts) < 2: #on vérifie que le filtre soit composé de 2 mots, pas juste de l'opérateur ou de la valeur
            raise ValueError("Condition de filtrage invalide. Exemple correct : is 'Jean'.")

        operator, value = parts
        value = value.strip().strip("'\"")  # Nettoyer la valeur

        if operator == "is": #si on veut la valeur exacte
            filtered_df = df[df[column] == value]
        elif operator == "!=":#si on veut tout sauf la valeur exacte
            filtered_df = df[df[column] != value]
        elif operator == "contains": #si on veut tout ce qui contient la valeur exacte
            filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        elif operator == "startswith": #si on veut ce qui commence par la valeur exacte
            filtered_df = df[df[column].astype(str).str.startswith(value)]
        elif operator == "endswith":#si on veut ce qui finit par la valeur exacte
            filtered_df = df[df[column].astype(str).str.endswith(value)]
        else:
            raise ValueError(f"Opérateur non supporté : {operator}") #si c'est aucun des opérateurs supportés

        return filtered_df if not filtered_df.empty else pd.DataFrame(columns=df.columns)

    # Si aucun cas précédent n'est satisfait, lever une erreur
    raise ValueError(f"Opérateur non supporté : {condition}")



def group_by_column(df, column, aggregation):
    """
    Regroupe les données par une colonne et applique une fonction d'agrégation.
    - aggregation : dictionnaire de type {"colonne": "moyenne/somme/max/min"}
    """
    agg_mapping = { #on définit les différentes agrégations
        "sum": "sum", #sum pour la somme
        "mean": "mean", #mean pour la moyenne
        "max": "max",#max pour le maximum
        "min": "min" #min pour le minimum
    }

    # Vérifier que l'agrégation demandée est valide
    agg_functions = {col: agg_mapping[func] for col, func in aggregation.items() if func in agg_mapping}
    
    if not agg_functions: #si l'agrégation demandée n'est pas valide
        raise ValueError(f"Aucune fonction d'agrégation valide trouvée dans {aggregation}")

    return df.groupby(column, as_index=False).agg(agg_functions)#on utilise groupby() de pandas pour appliquer les agrégations









# ========================== TEST POUR LES FILTRES==========================
if __name__ == "__main__":
    # Création d'un DataFrame de test
    data = {
        "id": [1, 2, 3, 4, 5],
        "amount": [500, 1000, 300, 2000, 1000],  # Montants pour tester les filtres numériques
        "name": ["Alice", "Jean", "Charlie", "Jean-Claude", "Jean"]  # Noms pour tester les filtres texte
    }
    
    df = pd.DataFrame(data)
    
    print("🔹 Données avant filtrage:")
    print(df)

    # Filtrer les montants supérieurs à 1000€
    df_filtered_amount = filter_data(df, "amount", "> 1000")
    print("\n✅ Transactions supérieures à 1000:")
    print(df_filtered_amount)

    # Filtrer uniquement les "Jean" exacts avec `is`
    df_filtered_name = filter_data(df, "name", "is 'Jean'")
    print("\n✅ Personnes dont le nom est exactement 'Jean':")
    print(df_filtered_name)

    # Filtrer les noms contenant "Jean"
    df_filtered_contains = filter_data(df, "name", "contains 'Jean'")
    print("\n✅ Personnes dont le nom contient 'Jean':")
    print(df_filtered_contains)

    # Filtrer uniquement les "Paul" exacts avec `is` (Test si le nom cherché n'est pas présent)
    df_filtered_name = filter_data(df, "name", "is 'Paul'")
    print("\n✅ Personnes dont le nom est exactement 'Paul':")
    print(df_filtered_name)