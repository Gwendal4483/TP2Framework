import pandas as pd

def filter_data(df, column, condition):
    """
    Filtre les données d'un DataFrame en fonction d'une condition.

    - Comparaisons numériques : `>`, `<`, `>=`, `<=`, `=`
    - Comparaisons texte : `is`, `!=`, `contains`, `startswith`, `endswith`
    - Détection automatique des colonnes numériques / textuelles
    """
    
    condition = condition.strip()  # Nettoyer la condition

    # Vérifier si c'est une comparaison numérique
    if condition.startswith((">", "<", "=")):  
        operator = condition[:1] if condition[:2] not in (">=", "<=") else condition[:2] #on regarde si c'est <= ou >= ou autre chose
        value = condition[len(operator):].strip().strip("'\"")  # on retire les guillemets ou les / pour pouvoir traiter le filtre
        
        # Vérifier si la colonne est numérique
        is_numeric = pd.api.types.is_numeric_dtype(df[column])
        
        if is_numeric: #si c'est un nombre 
            value = float(value)  # Convertir en nombre 
            return df.query(f"{column} {operator} @value")
        else:
            raise ValueError(f"L'opérateur '{operator}' est réservé aux valeurs numériques.")#si on a mis le mauvais opérateur devant du texte

    # Comparaisons pour les chaînes de caractères
    elif condition.startswith(("is", "!=", "contains", "startswith", "endswith")):
        parts = condition.split(" ", 1)  # Séparer l'opérateur et la valeur

        if len(parts) < 2:
            raise ValueError("Condition de filtrage invalide. Exemple correct : is 'Jean'.")

        operator, value = parts
        value = value.strip().strip("'\"")  # Nettoyer la valeur

        if operator == "is":
            return df[df[column] == value]
        elif operator == "!=":
            return df[df[column] != value]
        elif operator == "contains":
            return df[df[column].astype(str).str.contains(value, case=False, na=False)]
        elif operator == "startswith":
            return df[df[column].astype(str).str.startswith(value)]
        elif operator == "endswith":
            return df[df[column].astype(str).str.endswith(value)]
        else:
            raise ValueError(f"Opérateur non supporté : {operator}")

    else:
        raise ValueError(f"Opérateur non supporté : {condition}")

# ========================== TEST ==========================
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
