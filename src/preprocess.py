import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import argparse
 
def preprocess_data(data_file, output_dir):
    """
    Preprocesses the data for model training and evaluation.
 
    Parameters:
        data_file (str): Path to the raw data file.
        output_dir (str): Directory to save the processed files.
    """
    try:
        print("Étape 1 : Vérification de l'existence du fichier d'entrée...")
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Le fichier de données '{data_file}' est introuvable.")
        print("=> Fichier d'entrée trouvé.")
 
        print("Étape 2 : Création du répertoire de sortie si nécessaire...")
        os.makedirs(output_dir, exist_ok=True)
        print("=> Répertoire de sortie prêt : ", output_dir)
 
        print("Étape 3 : Chargement des données...")
        data = pd.read_csv(data_file, encoding="utf-8")
        print("=> Données chargées avec succès. Nombre de lignes : ", len(data))
 
        print("Étape 4 : Vérification des colonnes nécessaires...")
        required_columns = ['family_id', 'sequence_name', 'family_accession', 'aligned_sequence', 'sequence']
        for col in required_columns:
            if col not in data.columns:
                raise KeyError(f"Colonne manquante dans le fichier de données : '{col}'")
        print("=> Toutes les colonnes nécessaires sont présentes.")
 
        print("Étape 5 : Suppression des valeurs manquantes...")
        data = data.dropna()
        print("=> Données après suppression des valeurs manquantes. Nombre de lignes : ", len(data))
 
        print("Étape 6 : Encodage de la colonne 'family_accession'...")
        encoder = LabelEncoder()
        data['family_accession_encoded'] = encoder.fit_transform(data['family_accession'])
        print("=> Encodage terminé. Valeurs uniques dans 'family_accession_encoded' : ", len(data['family_accession_encoded'].unique()))
 
        print("Étape 7 : Division des données en ensembles train/dev/test...")
        train, temp = train_test_split(data, test_size=0.3, random_state=42)
        dev, test = train_test_split(temp, test_size=0.5, random_state=42)
        print(f"=> Division réussie : train={len(train)}, dev={len(dev)}, test={len(test)}")
 
        print("Étape 8 : Sauvegarde des ensembles train/dev/test...")
        train_path = os.path.join(output_dir, 'train.csv')
        dev_path = os.path.join(output_dir, 'dev.csv')
        test_path = os.path.join(output_dir, 'test.csv')
 
        train.to_csv(train_path, index=False)
        dev.to_csv(dev_path, index=False)
        test.to_csv(test_path, index=False)
        print(f"=> Fichiers sauvegardés :\n  - Train : {train_path}\n  - Dev : {dev_path}\n  - Test : {test_path}")
 
    except Exception as e:
        print(f"Erreur : {e}")
 
def main():
    """
    Main function to parse command-line arguments and call preprocess_data.
    """
    parser = argparse.ArgumentParser(description="Prétraiter les données brutes pour l'analyse.")
    parser.add_argument("--data_file", type=str, required=True, help="Chemin vers le fichier de données brutes (CSV).")
    parser.add_argument("--output_dir", type=str, required=True, help="Répertoire de sortie pour les fichiers prétraités.")
    args = parser.parse_args()
 
    # Appeler la fonction preprocess_data avec les arguments fournis
    preprocess_data(args.data_file, args.output_dir)
 
if __name__ == "__main__":
    main()