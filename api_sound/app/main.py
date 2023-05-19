from flask import Flask, render_template, jsonify
from flask import request
import json
import shutil
import os
import pandas as pd
from pydub import AudioSegment
from pydub.playback import play
from images_api import Mp3_to_png
from bdd.connect import Conn
from flask_cors import CORS
from bdd.mg import Conn as Mg
from typing import Tuple


app = Flask(__name__)
CORS(app)

"""  
API avec flask : 
    l'api recevoit des fichiers mp3 zippés
    l'api effectue/renvoie la classification de la musique : chanson/instrumental 
    3 modèles sont disponibles (vgg16, cnn, lstm) ; le meilleur modèle est VGG16, le modèle de plus léger LSTM
"""


#######################################################################################################################
#######################################################################################################################
# fonctions utilitaires


def remove_folders():    
        # opérations sur les dossiers : 
        # suppression/création des répertoires pour ne pas charger inutilement le disque dur
    if os.path.exists('archives'):
        shutil.rmtree('archives')
        os.mkdir('archives')
    if os.path.exists('im'):
        shutil.rmtree('im')
        os.mkdir('im')


def unpack_zip(file) -> None:  
    # dézipper le fichier reçu
    file.save('./received/temp.zip')
    shutil.unpack_archive('./received/temp.zip', 'archives', 'zip')


def find_jsons() -> Tuple[(list, list)]:
    files = ['json/'+x for x in os.listdir('json')]
    idx = [int(x.split('/')[-1].replace('.json', '')) for x in files]
    df = pd.DataFrame(list(zip(idx, files)), columns=['idx', 'files'])\
        .sort_values(by='idx')\
            .reset_index(drop=True)
    return list(df['files']), list(df['idx'].astype(str))


#######################################################################################################################
#######################################################################################################################
# fonction api


@app.route('/lstm', methods=['POST', 'OPTIONS'])
def lstm():
    # recevoir un zip, exporter la prédiction avec le modèle LSTM
        
    remove_folders()
    unpack_zip(request.files['file'])
    
    cl = Mp3_to_png()
    res = str(cl.main('lstm'))
    
    remove_folders()
    return res


@app.route('/vgg', methods=['POST', 'OPTIONS'])
def vgg():
    # recevoir un zip, exporter la prédiction avec le modèle vgg16
    
    remove_folders()
    unpack_zip(request.files['file'])

    cl = Mp3_to_png()
    res = str(cl.main('vgg'))
    
    remove_folders()
    return res


@app.route('/cnn', methods=['POST', 'OPTIONS'])
def cnn():
    # recevoir un zip, exporter la prédiction avec le modèle cnn

    remove_folders()
    unpack_zip(request.files['file'])

    cl = Mp3_to_png()
    res = str(cl.main('cnn'))

    remove_folders()
    return res


@app.route("/")
def index():
    idx = Mg().get_ids()
    return render_template("index.html", files=idx)


# by UIDs
@app.route('/1431766f-b5ce-4603-9e17-1de15d0e6c81', methods=['GET', 'POST'])
def histo_get():
    if request: 
        content = request.get_json(silent=True)
        data = Mg().fetch_one({"nom" : content['jsonFile']})
        return jsonify(data)
    else:
        return jsonify({'request':'error'})


@app.route('/7eb9e62c-f64c-11ed-b67e-0242ac120002', methods=['GET', 'POST'])
def onload_get():
        my_json = Mg().get_data()
        return jsonify(my_json)
    

@app.errorhandler(404)
def page_not_found(e):
    # page d'erreur 404
    
    return {"message":"erreur"}, 404