import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(layout="wide")
from utils import requetes
import numpy as np


#-------------------------- <<<<<<<<<<<<<<<---->>>>>>>>>>>>>>> --------------------
#-----------------------------------------sidebar----------------------------------
#-------------------------- <<<<<<<<<<<<<<<---->>>>>>>>>>>>>>> --------------------

st.sidebar.write("sidebar")
iter1 = st.sidebar.checkbox('Analyse initiale', value=False)
iter2 = st.sidebar.checkbox('Outil graphique et planning', value=False)
iter3 = st.sidebar.checkbox('Machine learning', value=False)
iter4 = st.sidebar.checkbox('Développement final', value=False)


#-------------------------- <<<<<<<<<<<<<<<---->>>>>>>>>>>>>>> --------------------
#-----------------------------------conteneur principal----------------------------
#-------------------------- <<<<<<<<<<<<<<<---->>>>>>>>>>>>>>> --------------------



st.title("Dashboard : page d'échange avec les parties prenantes")

if iter1:
    
    st.subheader("Analyse de faisabilité : test de classification par danse, labellisation par webscrapping")
    
    col1, col2= st.columns(2)

    with col1:
    
        fig1, ax1 = plt.subplots(figsize=(8,3))
        df=requetes.repartition_danses_par_dossier()
        fig1.suptitle('répartition des airs par dossier')
        ax1.bar(df.iloc[:,0], df.iloc[:,1])
        leg = list(df.iloc[:,0])
        ax1.set_xticklabels(leg, rotation=75)
        st.pyplot(fig1, clear_figure=True)
        

        fig2, ax2 = plt.subplots(figsize=(8,3))
        df=requetes.repartition_danses()
        fig2.suptitle('répartition des airs labellisés par webscraping')
        ax2.bar(df.iloc[:,0], df.iloc[:,1])
        leg = list(df.iloc[:,0])
        ax2.set_xticklabels(leg, rotation=75)
        st.pyplot(fig2, clear_figure=True)

    with col2:
        st.image('images/classement_par_danses.png', width=500)

        st.markdown(
            "<i>0 : reel, 1 : jig, 3 : song</i><br><u>note sur la matrice de confusion (données de test) :</u><br>la classification est parfaite quand la diagonale haut-gauche bas-droit comprend tous les décomptes<br><br><b><u>Constatations :</u></b><br><ul><li>La répartiton des timbres des instruments n'est pas homogène</li><li>La labellisation n'est pas homogène</li><li>la classification ne fonctionne pas</li></ul>", unsafe_allow_html =True)

    st.markdown("<b><u>Proposition pour une deuxième itération :</u></b><br>créer un outil graphique qui permet une labellisation facilitée", unsafe_allow_html=True)

 
if iter2:
    
    st.subheader("Deuxième itération : livraison d'un outil graphique aux métiers en capacité de labelliser les données")
    
    col1, col2= st.columns(2)

    with col1:
        st.image("images/labellisator1.png")
    
    with col2:
        st.markdown("<b>Livraison d'un outil pour labelliser les fichiers sons</b>", unsafe_allow_html=True)


    st.subheader("Propostion de planning :")
    
    st.image("images/grapheAgile.png")
    st.image("images/planning_gantt.png")
    
    
if iter3:
    
    st.subheader("Résultats Machine learning")

    
    st.dataframe(requetes.resultats1())
    fig3, ax3 = plt.subplots(figsize=(8,3))
    decalage=0.15
    size_barres=0.15
    df=requetes.resultats1()
    fig3.suptitle('métriques de classification')
    ax3.bar(df.index-decalage, df['accuracy'], width=size_barres, color='green', label='accuracy')
    ax4 = ax3.twinx() 
    ax4.bar(df.index, df['precision_song'], width=size_barres, color='orange', label='precision chanson')
    ax5 = ax3.twinx() 
    ax5.bar(df.index+decalage, df['precision_instrumental'], width=size_barres, color='blue', label='precision instrumental')
    ax3.grid(True)
    ax4.grid(True)
    ax5.grid(True)
    ax3.set_ylabel('pourcentage')
    ax3.set_xlabel('modèle')
    fig3.legend(prop={'size': 4}, frameon=False, bbox_to_anchor=(0.23, 1))
    ax3.set_ylim([0,100])
    ax4.set_ylim([0,100])
    ax5.set_ylim([0,100])
    leg = list(df.iloc[:,0])
    ax3.set_xticks([0,1,2]) 
    ax3.set_xticklabels(leg)
    st.pyplot(fig3, clear_figure=True)
        
        
if iter4:

    st.subheader("Développement final et restitution")

    st.markdown("<b>Monitoring des modèles :</b>", unsafe_allow_html=True)
    st.markdown("classification par API :", unsafe_allow_html=True)
    st.image("images/monitoring.png")
    st.markdown("Graphiques d'apprentissage :", unsafe_allow_html=True)
    st.markdown("http://localhost:5001/", unsafe_allow_html=True)
    
    st.markdown("<b>API et lecteur : client/utilisateur</b>", unsafe_allow_html=True)
    st.markdown("test API :", unsafe_allow_html=True)
    st.markdown("http://erwan-diato.com/app.php?token=a1z2e3r4t5y6&id=instrus", unsafe_allow_html=True)
   
    st.image("images/api2.png")
    st.image("images/appli_finale.png")
    
    st.markdown("<b>Démonstration de l'application :</b>", unsafe_allow_html=True)
    st.video("images/demo_application.mp4", format="video/mp4", start_time=0)
    
    st.markdown("<b>Vérification de l'update :</b>", unsafe_allow_html=True)
    st.video("images/update.mp4", format="video/mp4", start_time=0)