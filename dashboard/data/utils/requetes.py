from bdd import connect
import pandas as pd
import numpy as np


def repartition_danses_par_dossier() -> pd.DataFrame:
    return connect.Conn().to_df("select * from repartition_danses_par_dossier;")

   
def repartition_danses() -> pd.DataFrame:
    return connect.Conn().to_df("select * from repartition_danses;")


def resultats1() -> pd.DataFrame:
    return connect.Conn().to_df("select * from metrics();")