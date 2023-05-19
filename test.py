import os
import numpy as np
from machine_learning.prediction import Pred 
from api_sound.app.bdd import connect as connect_api


def test_window():
    assert Pred().window(test=True)
    
    
def test_choix_modele():
    cl = Pred()
    size, architecture = Pred().choix_modele(test=True)
    assert architecture == "lstm"
    assert size == 100
    
        
def test_load():
    res = Pred().load(nb_im=5, test=True)
    assert len(res)==5
    assert os.path.exists(f"/media/bob/media/images/{res[0]}.png")
    
    
def test_load_images():
    cl = Pred()
    cl.architecture = "lstm"
    im, idx = cl.load_images(nb_im=5, test=True)
    assert len(im) == len(idx) == 5
    
    
def test_predict():
    cl = Pred()
    _, _ = cl.choix_modele(test=True)
    assert cl.predict(nb_im=5, test = True)


def test_compte():
    cl = Pred()
    cl.column = "test"
    assert cl.compte(test = True) > 0
    
    
def test_find_cols():
    cl = connect_api.Conn()
    assert len(cl.find_cols()) > 0
    
    
def test_col_count_dict():
    cl = connect_api.Conn()
    assert len(cl.col_count_dict()) > 0
    