import streamlit as st
import pandas as pd
import numpy as np
import folium
from sklearn.neighbors import BallTree
from streamlit_folium import st_folium

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="CareMap Cameroon",
    page_icon="📍",
    layout="wide"
)

# --- STYLE CSS POUR LE DESIGN ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2ecc71; color: white; }
    .card { padding: 15px; border-radius: 10px; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    # Remplace par le nom exact de ton fichier CSV final
    try:
        df = pd.read_csv('df_final.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ Fichier 'df_final.csv' introuvable dans le dossier.")
        return None

df_final = load_data()

if df_final is not None:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/684/684908.png", width=100)
    st.sidebar.title("Paramètres CareMap")
    
    st.sidebar.divider()
    
    # Choix de la catégorie
    categories = sorted(df_final['Categorie'].unique())
    selected_cat = st.sidebar.selectbox("🔎 Que cherchez-vous ?", categories)
    
    # Nombre de résultats
    k_res = st.sidebar.slider("Nombre de structures proches", 1, 10, 3)
    
    # Coordonnées utilisateur (Odza par défaut)
    st.sidebar.subheader("📍 Ma Position")
    u_lat = st.sidebar.number_input("Latitude", value=3.8180, format="%.4f")
    u_lon = st.sidebar.number_input("Longitude", value=11.5221, format="%.4f")

    # --- MOTEUR DE RECOMMANDATION (KNN) ---
    def get_recommendations(lat, lon, cat, k):
        df_cat = df_final[df_final['Categorie'] == cat].copy()
        if df_cat.empty:
            return None
        
        # Création de l'arbre spatial
        coords_cat = np.deg2rad(df_cat[['latitude', 'longitude']].values)
        tree_cat = BallTree(coords_cat, metric='haversine')
        
        # Recherche des voisins
        dist, ind = tree_cat.query(np.deg2rad([[lat, lon]]), k=min(k, len(df_cat)))
        
        # Préparation des résultats
        res = df_cat.iloc[ind[0]].copy()
        res['distance_km'] = dist[0] * 6371 # Conversion en km
        return res

    # --- AFFICHAGE PRINCIPAL ---
    st.title("🏥 CareMap : L'accès aux soins en un clic")
    st.markdown(f"Affichage des **{selected_cat}** les plus proches de votre position.")

    recos = get_recommendations(u_lat, u_lon, selected_cat, k_res)

    col_map, col_list = st.columns([2, 1])

    with col_map:
        # Création de la carte Folium
        m = folium.Map(location=[u_lat, u_lon], zoom_start=13, tiles="cartodbpositron")
        
        # Marqueur utilisateur
        folium.Marker(
            [u_lat, u_lon], 
            tooltip="Moi", 
            icon=folium.Icon(color='blue', icon='user', prefix='fa')
        ).add_to(m)

        if recos is not None:
            for _, row in recos.iterrows():
                # Lien itinéraire
                url_gmaps = f"https://www.google.com/maps/dir/?api=1&destination={row['latitude']},{row['longitude']}"
                
                popup_html = f"""
                <div style='width:200px; font-family:Arial;'>
                    <b>{row['nom']}</b><br>
                    Quartier: {row['quartier']}<br>
                    Distance: {row['distance_km']:.2f} km<br><br>
                    <a href='{url_gmaps}' target='_blank' style='color:white; background:#2ecc71; padding:5px; border-radius:3px; text-decoration:none;'>🚀 Y aller</a>
                </div>
                """
                
                folium.Marker(
                    [row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=row['nom'],
                    icon=folium.Icon(color='red', icon='plus', prefix='fa')
                ).add_to(m)
        
        st_folium(m, width=900, height=600)

    with col_list:
        st.subheader("📋 Liste des structures")
        if recos is not None:
            for _, row in recos.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <h4 style="margin:0; color:#2c3e50;">{row['nom']}</h4>
                        <p style="margin:5px 0;">📍 {row['quartier']} ({row['ville']})</p>
                        <p style="margin:5px 0;">📞 {row['telephone']}</p>
                        <p style="margin:0; font-weight:bold; color:#27ae60;">📏 {row['distance_km']:.2f} km</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("") # Espacement
        else:
            st.warning("Aucune structure trouvée.")

else:
    st.info("💡 En attente du fichier de données pour démarrer l'analyse...")