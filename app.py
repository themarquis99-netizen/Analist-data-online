import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="Analyseur Pro v2",
    layout="centered"
)

# --- BASE DE DONNÉES (SESSION) ---
if "db_utilisateurs" not in st.session_state:
    st.session_state["db_utilisateurs"] = []

# --- FONCTION ---
def enregistrer_acces(parametres, resultat):
    st.session_state["db_utilisateurs"].append({
        "Date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Paramètres": parametres,
        "Résultat": resultat
    })

# --- MENU ---
st.sidebar.title("Menu Principal")
page = st.sidebar.selectbox(
    "Aller vers",
    ["🏠 Application", "🔐 Administration"]
)

# =====================
# PAGE APPLICATION
# =====================
if page == "🏠 Application":
    st.title("Système de Prédiction Intelligente")

    with st.expander("ℹ️ Aide"):
        st.info(
            "Entrez les paramètres puis lancez l’analyse.\n\n"
            "Le score est une simulation."
        )

    with st.form("form_prediction"):
        valeur_x = st.slider("Niveau d’intensité", 0, 100, 50)
        valeur_y = st.number_input("Facteur numérique", value=10.0)
        lancer = st.form_submit_button("Lancer la prédiction")

    if lancer:
        with st.spinner("Analyse en cours..."):
            time.sleep(1)
            score = valeur_x + valeur_y
            resultat = f"Positif (Score : {score}%)"
            st.success(resultat)

            enregistrer_acces(
                {"Intensité": valeur_x, "Facteur": valeur_y},
                resultat
            )

# =====================
# PAGE ADMIN
# =====================
elif page == "🔐 Administration":
    st.title("Administration")

    password = st.text_input("Mot de passe", type="password")

    if password == "admin123":
        st.success("Accès autorisé")

        if st.session_state["db_utilisateurs"]:
            df = pd.DataFrame(st.session_state["db_utilisateurs"])
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Télécharger le rapport",
                csv,
                "rapport.csv",
                "text/csv"
            )
        else:
            st.warning("Aucune donnée disponible")

    elif password != "":
        st.error("Mot de passe incorrect")
