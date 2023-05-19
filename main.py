from utils import mp3_to_bdd
from utils import rentrer_danse_noms
from utils import images
from utils import dataset
from machine_learning import apprentissage, prediction
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--run', type=str, required=True, help='options disponibles : train, predict')
parser.add_argument('--model', type=str, help='options disponibles pour l\'apprentissage: vgg16, cnn, lstm')
parser.add_argument('--epochs', type=str, help='il est possible de fixer un nombre d\'epochs, sinon c\'est 10 par défaut')
args = parser.parse_args()


def main():

    """
        lancer le programme : rentrer les mp3 en bdd, créer un dataset, effectuer apprentissage et prédiction
        les quatres premières étapes sont à réaliser une seule fois, elles sont donc désactivées.
        ne pas réactiver si la base de données est créée et remplie. 
    """

    # rentrer mes chemins de fichiers dans la base de données
    # etape1 = mp3_to_bdd.Entree_bdd()
    # etape1.main()

    # rentrer les noms d'airs webscrappés dans la base de données
    # etape2 = rentrer_danse_noms.Danse_noms()
    # etape2.main()

    # convertir les mp3 en spectrogrammes
    # etape3 = images.Mp3_to_png()
    # etape3.main()

    # créer un dataset d'apprentissage
    # etape4 = dataset.Create_dataset()
    # etape4.main()
    
    if args.run == "train":
        if not args.model:
            raise Exception("--model veuillez choisir l'option vgg16, cnn ou lstm")
        epochs = 10 if not args.epochs else int(args.epochs)
        etape5 = apprentissage.Train(epochs=epochs)
        etape5.main(args.model)
      
    
    elif args.run == "predict":
        etape6 = prediction.Pred()
        etape6.main()
    
    else:
        raise NameError("Veuillez choisir l'option train ou l'option predict")

main()