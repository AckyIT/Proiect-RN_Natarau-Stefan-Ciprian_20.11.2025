import streamlit as st
import cv2
import numpy as np
import joblib
from PIL import Image

# ================= CONFIGURARE =================
FISIER_MODEL = "retea_neuronala_antrenata.pkl"
IMG_SIZE = 64
CLASE = ["GPU", "HDD", "MOTHERBOARD", 
         "PROCESOR_AMD_AM4", "PROCESOR_AMD_AM5", 
         "PROCESOR_INTEL_LGA1200", "PROCESOR_INTEL_LGA1700", 
         "RAM_DDR4", "RAM_DDR5"]
# ===============================================

# Functia care incarca modelul (cu cache ca sa nu-l incarce la fiecare click)
@st.cache_resource
def incarca_creierul():
    try:
        model = joblib.load(FISIER_MODEL)
        return model
    except:
        return None

# Titlu si Design
st.title("PC Component Classifier AI")
st.write("Sistem inteligent de recunoastere a componentelor hardware.")
st.write("---")

# Incarcare Model
model = incarca_creierul()

if model is None:
    st.error(f"Nu gasesc fisierul '{FISIER_MODEL}'! Ruleaza intai 'retea.py' ca sa antrenezi modelul.")
else:
    # Zona de Drag & Drop
    uploaded_file = st.file_uploader("Trage o poza aici (Drag & Drop)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # 1. Afisam poza originala
        image = Image.open(uploaded_file)
        st.image(image, caption='Imaginea incarcata', width=300)

        # 2. Preprocesare (Exact ca la antrenare!)
        try:
            # Convertim din format PIL (Web) in OpenCV (Numpy)
            img_array = np.array(image)

            # Daca imaginea e color (RGB), o facem Grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Resize la 64x64
            img_resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))
            
            # Aplatizare si Normalizare
            img_vector = img_resized.flatten().astype('float64') / 255.0

            # 3. Predictie
            st.write("Analizez imaginea...")
            
            # Bara de progres pentru efect vizual
            my_bar = st.progress(0)
            for percent_complete in range(100):
                my_bar.progress(percent_complete + 1)

            # Facem predictia
            rezultat_index = model.predict([img_vector])[0]
            probabilitati = model.predict_proba([img_vector])[0]
            
            nume_predis = CLASE[rezultat_index]
            incredere = probabilitati[rezultat_index] * 100

            # 4. Afisare Rezultat
            if incredere > 70:
                st.success(f"Rezultat: **{nume_predis}**")
            elif incredere > 40:
                st.warning(f"Probabil este: **{nume_predis}**")
            else:
                st.error(f"Nu sunt sigur, dar cred ca e: **{nume_predis}**")
            
            st.metric(label="Grad de Incredere", value=f"{incredere:.2f}%")

            # Afisam grafic toate probabilitatile (Bonus vizual)
            st.write("Distributia probabilitatilor:")
            st.bar_chart(probabilitati)

        except Exception as e:
            st.error(f"Eroare la procesare: {e}")