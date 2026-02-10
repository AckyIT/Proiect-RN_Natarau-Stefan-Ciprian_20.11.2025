import cv2
import numpy as np
import os
import glob
import joblib  # Pentru salvarea retelei antrenate
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ================= CONFIGURARE =================
# Calea unde ai toate pozele PNG (GPU (1).png, etc.
CALE_POZE = r"F:\RN\proiect\data\processed"

# Fisierul unde salvam "creierul" antrenat
FISIER_MODEL = "retea_neuronala_antrenata.pkl"

# Clasele (Trebuie sa fie exact cum incep numele fisierelor)
CLASE = ["GPU", "HDD", "MOTHERBOARD", "PROCESOR_AMD_AM4", "PROCESOR_AMD_AM5", "PROCESOR_INTEL_LGA1200", "PROCESOR_INTEL_LGA1700", "RAM_DDR4", "RAM_DDR5"]

IMG_SIZE = 64   # Dimensiunea la care redimensionam (64x64)
# ===============================================

def incarca_date():
    print(f"[INFO] incarc imaginile din {CALE_POZE}...")
    data = []
    labels = []
    
    if not os.path.exists(CALE_POZE):
        print(f"[EROARE] Nu gasesc folderul: {CALE_POZE}")
        return None, None

    for index, nume_clasa in enumerate(CLASE):
        # Cautam fisiere png care incep cu numele clasei (ex: GPU*.png)
        pattern = os.path.join(CALE_POZE, f"{nume_clasa}*.png")
        imagini_gasite = glob.glob(pattern)
        
        print(f"  > Clasa '{nume_clasa}': {len(imagini_gasite)} imagini.")
        
        for cale_img in imagini_gasite:
            try:
                # 1. Citire (Alb-negru)
                img = cv2.imread(cale_img, cv2.IMREAD_GRAYSCALE)
                # img = cv2.imread(cale_img, cv2.IMREAD_COLOR)
                if img is None: continue
                
                # 2. Resize (64x64)
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                
                # 3. Aplatizare (Vector 1D) si Normalizare (0-1)
                img_vector = img.flatten().astype('float64') / 255.0
                
                data.append(img_vector)
                labels.append(index) # Salvam ID-ul clasei (0, 1, 2...)

            except Exception as e:
                print(f"Eroare la {cale_img}: {e}")

    return np.array(data), np.array(labels)

def antreneaza_retea():
    X, y = incarca_date()
    if X is None or len(X) == 0:
        print("[EROARE] Nu am date pentru antrenare!")
        return None

    # impartim datele: 80% antrenare, 20% testare
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"\n[INFO] incep antrenarea pe {len(X_train)} imagini...")
    
    # Cream reteaua (2 straturi ascunse: 100 si 50 neuroni)
    mlp = MLPClassifier(hidden_layer_sizes=(100, 50), 
                        activation='relu', 
                        solver='adam', 
                        max_iter=1000,
                        random_state=42,
                        verbose=True) # verbose=True arata progresul in timp real

    mlp.fit(X_train, y_train)
    print("[INFO] Antrenare completa!")

    # Testam acuratetea
    predictii = mlp.predict(X_test)
    acuratete = accuracy_score(y_test, predictii)
    print(f"[REZULTAT] Acuratete retea: {acuratete * 100:.2f}%")

    # Salvam modelul
    joblib.dump(mlp, FISIER_MODEL)
    print(f"[INFO] Reteaua a fost salvata in '{FISIER_MODEL}'.")
    return mlp

def prezice_imagine(cale_imagine, model=None):
    # Daca nu avem modelul in memorie, incercam sa-l incarcam de pe disc
    if model is None:
        print("[INFO] incarc modelul salvat...")
        model = joblib.load(FISIER_MODEL)

    # Procesam imaginea de test EXACT la fel ca la antrenare

    #=======================================================
    # Functia de remove background 
    # "F:\RN\proiect\src\data_acquisition\bgrmv.py"
    # Trebuie folosita in avans
    #=======================================================

    img = cv2.imread(cale_imagine, cv2.IMREAD_GRAYSCALE)
    # img = cv2.imread(cale_imagine, cv2.IMREAD_COLOR)
    if img is None:
        print(f"[EROARE] Nu pot citi imaginea: {cale_imagine}")
        return

    img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img_vector = img_resized.flatten().astype('float64') / 255.0
    cv2.imwrite('output_image.png', img_resized)
    # Facem predictia (trebuie sa fie lista de liste, de aia punem [img_vector])
    rezultat_index = model.predict([img_vector])[0]
    probabilitati = model.predict_proba([img_vector])[0]
    
    nume_predis = CLASE[rezultat_index]
    incredere = probabilitati[rezultat_index] * 100
    
    print("\n" + "="*30)
    print(f" COMPONENTA:  {nume_predis.upper()}")
    print(f" POTRIVIRE:  {incredere:.2f}%")
    print("="*30 + "\n")

# ================= MAIN =================
if __name__ == "__main__":
    model = None
    #os.remove("retea_neuronala_antrenata.pkl") 
    # Antrenam (Daca nu avem deja fisierul .pkl)
    if not os.path.exists(FISIER_MODEL):
        model = antreneaza_retea()

    # PASUL 2: Testam o imagine (Schimba calea de aici cu ce poza vrei tu!)
    # Exemplu: luam una la intamplare din folder
    imagine_de_test = r"F:\RN\proiect\data\validation\img.png"
    
    print(f"Testez imaginea: {imagine_de_test}")
    prezice_imagine(imagine_de_test, model)

    # Utilizatorul sa bage input de la tastatura
    # while True:
    #     path = input("Baga calea catre o poza (sau 'exit'): ")
    #     if path.lower() == 'exit': break
    #     prezice_imagine(path.strip('"'), model)0
    os.system('pause')