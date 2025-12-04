# 📘 README – Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Natarau Stefan-Ciprian  
**Link Repository GitHub:** https://github.com/AckyIT/Proiect-RN_Natarau-Stefan-Ciprian_20.11.2025.git
**Data:** 04.12.2025

-----

## Livrabile Obligatorii

### 1\. Tabelul Nevoie Reală → Soluție SIA → Modul Software

| Nevoie reală concretă | Cum o rezolvă SIA-ul vostru | Modul software responsabil |
| **Generarea datelor de antrenare:** Lipsa unui set de date public care să diferențieze vizual componentele PC după Socket (AM4/AM5/LGA) și tip Memorie (DDR4/DDR5). | Generarea automată a seturilor de date sintetice (imagini AI specifice) și conversia lor în format binar pentru antrenare. | **Modul 1: Data Logging** (Achiziție și Preprocesare) |
| **Clasificarea automată:** Identificarea vizuală a tipului de componentă dintr-o imagine (ex: CPU AM4 vs LGA1700) bazată pe forme și marcaje. | Rețea Neuronală (CNN) configurată să recunoască pattern-uri vizuale distincte (ex: forma IHS la procesor, cipuri la RAM) și să returneze clasa. | **Modul 2: Rețeaua Neuronală** (Arhitectură Definită) |
| **Validarea compatibilității:** Verificarea potrivirii tehnice între componente (ex: CPU și Placă de Bază) pentru a preveni erori de asamblare. | Interfață utilizator care preia rezultatele clasificării și verifică regulile logice (Ex: "Socket AM4" se potrivește doar cu "Placă AM4"). | **Modul 3: Web Services / UI** (Logică și Interfață) |

-----

### 2\. Contribuția Voastră Originală la Setul de Date – MINIM 40%

### Contribuția originală la setul de date:

**Total observații finale:** \~1000 imagini (organizate pe clase)
**Observații originale:** 1000 (100%) - Întreg setul de date este creat de mine.

**Tipul contribuției:**
Date sintetice prin metode avansate (Generare AI cu prompt-uri specifice pentru detalii tehnice)
Etichetare/adnotare manuală (Sortare și validare în structura de foldere)

**Descriere detaliată:**
Am creat un set de date complet original pentru a rezolva problema lipsei de imagini standardizate pentru compatibilitate. Am utilizat generarea de imagini AI pentru a crea variații vizuale ale componentelor, punând accent pe elementele distinctive de compatibilitate:

  * **RAM:** Diferențiere vizuală între DDR4 (design simplu) și DDR5 (prezența cipului PMIC și design radiator).
  * **CPU:** Diferențiere bazată pe forma IHS (pătrat vs. caracatiță vs. dreptunghi) și logo-uri.
  * **MB:** Diferențiere bazată pe socket-ul vizibil.

Acestea sunt organizate în structura `data/raw` și sunt procesate automat de **Modulul 1** pentru a crea vectorii de antrenare.

**Locația codului:** `src/data_acquisition/dataSet.vi` (VI-ul principal de procesare).
**Locația datelor:** `data/raw/` (organizate ierarhic: CPU, RAM, MB etc.).

**Dovezi:**

  - Structura folderului `data/raw` conține imagini unice, generate pentru acest proiect.
  - VI-ul de procesare (`dataSet.vi`) demonstrează conversia imaginilor custom în formatul necesar toolkit-ului LabVIEW.

-----

### 3\. Diagrama State Machine a Întregului Sistem (OBLIGATORIE)

Diagrama arhitecturală a stărilor se găsește în: `docs/screenshots/usr.png`

**Justificarea State Machine-ului ales:**

Am ales o arhitectură de tip **Event-Driven State Machine**, standard în LabVIEW, pentru a gestiona fluxul logic al aplicației:

**Stările principale:**

1.  **IDLE:** Așteptare încărcare imagini de la utilizator.
2.  **ACQUIRE\_DATA:** Preluarea imaginilor (Componenta 1 și 2).
3.  **PREPROCESS:** Redimensionare și conversie (utilizând `ImageP.vi` și `Color-to-Grayscale`).
4.  **INFERENCE:** Trimiterea datelor către Rețeaua Neuronală pentru identificarea claselor.
5.  **LOGIC\_CHECK:** Verificarea compatibilității între clasele detectate (ex: Dacă Piesa 1 este "RAM DDR4", Piesa 2 trebuie să fie "MB DDR4").
6.  **DISPLAY:** Afișarea rezultatului final (Compatibil / Incompatibil / Sugestie).

-----

### 4\. Scheletul Complet al celor 3 Module Cerute

Sistemul este dezvoltat modular în **LabVIEW**.

| Modul | Implementare LabVIEW (VIs) | Stadiu Actual (Etapa 4) |
| **1. Data Logging** | `src/data_acquisition/dataSet.vi` | **Funcțional.** VI-ul parcurge recursiv folderele din `data/raw`, utilizează subVI-urile `ImageP.vi` și `Color-to-Grayscale` pentru a converti imaginile în vectori numerici și generează dataset-ul binar. |
| **2. Neural Network** | `src/neural_network/` | **Definit.** Structura de directoare este pregătită pentru VI-urile de definire și antrenare a rețelei (bazate pe toolkit-ul NI), care vor prelua datele generate de Modulul 1. |
| **3. Web Services / UI** | `src/app/` | **Definit.** Arhitectura interfeței utilizator este stabilită pentru a permite încărcarea a două imagini și afișarea verdictului de compatibilitate. |

-----

## Structura Repository-ului la Finalul Etapei 4

Aceasta este structura organizată a proiectului:

```
proiect-rn-[nume-prenume]/
├── config/
│   └── class_labels.txt          # Lista etichetelor (clase: cpu_am4, ram_ddr4, etc.)
│
├── data/
│   ├── raw/                      # Imaginile originale generate AI
│   │   ├── CPU/ (AMD/Intel)
│   │   ├── RAM/ (DDR4/DDR5)
│   │   ├── MB/ ...
│   │   └── ...
│   └── processed/                # Fișiere binare rezultate din Data Logging
│
├── docs/
│   └── state_machine.png         # Diagrama stărilor
│
├── src/
│   ├── data_acquisition/         # MODUL 1: Data Logging
│   │   ├── dataSet.vi            # VI Principal generare dataset
│   │   ├── ImageP.vi             # VI procesare imagine (Resize/Resample)
│   │   └── 1394 Color-to-Grayscale_8_6.vi # VI conversie culoare
│   │
│   ├── neural_network/           # MODUL 2: Rețea Neuronală
│   │   └── [Aici vor fi VI-urile de antrenare și arhitectură]
│   │
│   └── app/                      # MODUL 3: UI / Logică
│       └── [Aici va fi VI-ul Principal de Rulare]
│
├── README.md                     # Readme general
└── requirements.txt              # Dependențe (NI LabVIEW, Vision Toolkit)
```

-----

### Checklist Final Etapa 4

  - [X] Tabelul Nevoie → Soluție → Modul completat.
  - [X] Declarație contribuție 100% date originale.
  - [X] Cod generare dataset (`dataSet.vi` + subVIs) funcțional .
  - [X] Diagrama State Machine inclusă.
  - [X] Repository structurat corect pe module.