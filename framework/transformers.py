import pandas as pd

def filter_data(df, column, condition):
    """
    Filtre les données d'un DataFrame en fonction d'une condition.

    - Supporte les comparaisons numériques (`>`, `<`, `>=`, `<=`, `=`)
    - Supporte les filtres texte (`=`, `!=`, `contains`, `startswith`, `endswith`)
    - Détecte automatiquement si une colonne est numérique ou textuelle
    """
    
    condition = condition.strip()  # Nettoyer les espaces au début/fin
    
    # Vérifier si l'utilisateur utilise un opérateur numérique (>1000, =200, etc.)
    if condition.startswith((">", "<", "=")):  
        operator = condition[:1] if condition[:2] not in (">=", "<=") else condition[:2]
        value = condition[len(operator):].strip().strip("'\"")  # Retirer les espaces et guillemets
        
        # Vérifier si la colonne est numérique (pour éviter l'erreur si on veut comparer du texte)
        is_numeric = pd.api.types.is_numeric_dtype(df[column])
        
        if is_numeric: #si c'est bien un nombre
            value = float(value)  # Convertir en nombre

        return df.query(f"{column} {operator} @value")  # Utilisation de `query()` pour un filtre propre en entrant la valeur et le filtre a appliquer


    # Si l'opérateur commence par `!=`, `contains`, `startswith`, `endswith`, alors c'est un texte (ou si is_numeric est en false)
    elif condition.startswith(("!=", "contains", "startswith", "endswith")):
        parts = condition.split(" ", 1)  # Séparer l'opérateur et la valeur
        
        if len(parts) < 2:
            raise ValueError("Condition de filtrage invalide. Exemple correct : contains 'Jean'.")

        operator, value = parts
        value = value.strip().strip("'\"")  # Nettoyer la valeur

        if operator == "!=":
            return df[df[column] != value]
        elif operator == "contains":
            return df[df[column].astype(str).str.contains(value, case=False, na=False)] #si la valeur CONTIENT le filtre entré
        elif operator == "startswith":
            return df[df[column].astype(str).str.startswith(value)]#si la valeur COMMENCE par le filtre entré
        elif operator == "endswith":
            return df[df[column].astype(str).str.endswith(value)]#si la valeur TERMINE par le filtre entré

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


    # Filtrer les noms contenant "Jean"
    df_filtered_contains = filter_data(df, "name", "contains 'Jean'")
    print("\n✅ Personnes dont le nom contient 'Jean':")
    print(df_filtered_contains)
