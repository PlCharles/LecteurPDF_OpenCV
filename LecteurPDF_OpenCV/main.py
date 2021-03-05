import subprocess # permet d'executer des lignes de commandes batch
import os



def main():
    # on cherche chaque fichier PDF dans le dossier PDF
    for file in os.listdir('./Documents'):
        if file.endswith('.pdf') or file.endswith('.Documents'):
            print(file)
            subprocess.call("python .\engine.py -p \"./Documents/"+ file )
            
    print("Traitement termine")

main()