import pandas as pd
import glob 
import os
from bdd.mg import Conn as Mg


def test_find_jsons() -> list:
    files = glob.glob('json/*')
    idx = [int(x.split('/')[-1].replace('.json', '')) for x in files]
    df = pd.DataFrame(list(zip(idx, files)), columns=['idx', 'files'])\
        .sort_values(by='idx', ascending=False)\
            .reset_index(drop=True)
    assert len(list(df['files'])) > 0


def test_mg(): 
    idx = Mg().get_ids()
    assert len(idx) > 0 
    

def test_get_data():
    data = Mg().get_data()
    assert len(data) > 0