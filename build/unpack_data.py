import os
import pandas as pd


def unpack_data(input_dir, output_file):
    """
    Exercice : Fonction pour décompresser et combiner plusieurs fichiers CSV à partir d'un répertoire en un seul fichier CSV.

    Objectifs :
    1. Lire tous les fichiers CSV dans un répertoire donné.
    2. Combiner les fichiers dans un seul DataFrame.
    3. Sauvegarder le DataFrame combiné dans un fichier CSV final.

    Étapes :
    - Parcourez tous les fichiers dans `input_dir`.
    - Vérifiez que les fichiers sont au format CSV ou contiennent "data-" dans leur nom.
    - Chargez chaque fichier dans un DataFrame Pandas.
    - Combinez tous les DataFrames dans un seul DataFrame.
    - Enregistrez le DataFrame combiné dans `output_file`.

    Paramètres :
    - input_dir (str) : Chemin vers le répertoire contenant les fichiers CSV.
    - output_file (str) : Chemin vers le fichier CSV combiné de sortie.

    Indices :
    - Utilisez `os.listdir` pour parcourir les fichiers.
    - Utilisez `os.path.join` pour construire le chemin complet des fichiers.
    - Utilisez `pd.read_csv` pour lire un fichier CSV en DataFrame.
    - Combinez les DataFrames avec `pd.concat`.
    - Sauvegardez le résultat avec `to_csv`.
    """

    dataframes = []
    # Parcourir tous les fichiers et dossiers dans input_dir
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)
        # Si l'élément est un fichier...
        if os.path.isfile(item_path) and (item.endswith(".csv") or "data-" in item):
            df = pd.read_csv(item_path)
            dataframes.append(df)
        # Si l'élément est un dossier...
        elif os.path.isdir(item_path):
            # Appeler récursivement unpack_data pour traiter le sous-dossier
            dataframes.extend(unpack_data(item_path, output_file)) 

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv(output_file, index=False)
    return dataframes  # Retourner la liste des dataframes


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Unpack and combine protein data")
    parser.add_argument("--input_dir", type=str, required=True, help="Path to input directory")
    parser.add_argument("--output_file", type=str, required=True, help="Path to output combined CSV file")
    args = parser.parse_args()

    unpack_data(args.input_dir, args.output_file)