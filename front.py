import streamlit as st
import requests

# Configurer la page
st.set_page_config(page_title="Moteur de Recherche", layout="wide", page_icon=":mag:", initial_sidebar_state="expanded")

# Appliquer le CSS pour la couleur de fond et la couleur du texte
css = """
<style>
    .stApp { background-color: #FFC595 !important; }
    .stApp, .stApp .css-1d391kg, .stApp .css-145kmo2 { color: #000000 !important; }  /* Couleur du texte noir */
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# URL de l'API Flask (ajustez selon vos besoins)
FLASK_API_URL = "http://localhost:5000/search"

# Centrer l'image
col1, col2, col3 = st.columns([3,1,3])
with col2:
    st.image("9mois.jpg", use_column_width=True)

# Champs de recherche
query = st.text_input("Entrez votre requête de recherche :", placeholder ="Si vous n'avez aucun résultat pertinent, assurez-vous de l'orthographie de votre recherche, ou contactez un administrateur :)")
# Cases à cocher pour les tables
table_choices = []
if st.checkbox("Articles", value=True):
    table_choices.append("articles")
if st.checkbox("Food"):
    table_choices.append("food")
if st.checkbox("Questions"):
    table_choices.append("questions")
if st.checkbox("Recipes"):
    table_choices.append("recipes")

if st.button("Rechercher"):
    if query:
        # Appeler l'API Flask pour obtenir les résultats
        params = {"query": query, "table": ",".join(table_choices) if table_choices else "Toutes"}
        response = requests.get(FLASK_API_URL, params=params)

        if response.status_code == 200:
            results = response.json().get("results", [])
            for result in results:
                if result['score'] > 0:
                    st.write(f"Table: {result['table']}, Score: {result['score']}")
                    st.write(result['document'])
                    st.write("---")
        else:
            st.error("Erreur lors de la recherche.")
    else:
        st.warning("Veuillez entrer une requête de recherche.")