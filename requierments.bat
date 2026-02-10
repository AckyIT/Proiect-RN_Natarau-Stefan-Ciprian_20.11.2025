@echo off
title Instalare Mediu Proiect AI

:: Afisare text informativ
echo ========================================================
echo                 INFORMATII PROIECT
echo ========================================================
echo.
echo Proiectul foloseste Python 3.10 si urmatoarele biblioteci externe:
echo.
echo    - scikit-learn: "Creierul" proiectului. O folosim pentru algoritmul AI (MLPClassifier) si pentru antrenarea retelei.
echo    - opencv-python (cv2): O folosim pentru a citi pozele, a le face alb-negru si a le redimensiona la 64x64 pixeli.
echo    - numpy: O folosim pentru calcule matematice, transformand pozele in tablou de numere (vectori).
echo    - joblib: O folosim ca sa salvam modelul antrenat in fisierul .pkl si sa il incarcam rapid cand facem predictii, fara sa re-antrenam de la zero.
echo    - streamlit: O folosim pentru Interfata Grafica (GUI). Ea ne genereaza site-ul web local unde facem Drag & Drop la poze.
echo    - Pillow (PIL): O folosim in interfata grafica pentru a procesa imaginile incarcate de utilizator.
echo    - requests: O folosim in scriptul bgrmv.py pentru a trimite pozele la API-ul remove.bg ca sa le scoatem fundalul.
echo.
echo ========================================================
echo.
echo Apasa orice tasta pentru a incepe instalarea...
pause >nul

:: 1. Instalare Python 3.10
echo.
echo [1/8] Se verifica/instaleaza Python 3.10...
winget install -e --id Python.Python.3.10 --scope machine

echo.
echo NOTA: Daca Python abia s-a instalat, e posibil sa fie nevoie de un restart
echo la calculator pentru ca 'pip' sa fie recunoscut. 
echo Daca ai deja Python, totul va merge.
echo.

:: 2. Instalare biblioteci
echo [2/8] Se instaleaza scikit-learn...
pip install scikit-learn

echo.
echo [3/8] Se instaleaza opencv-python...
pip install opencv-python

echo.
echo [4/8] Se instaleaza numpy...
pip install numpy

echo.
echo [5/8] Se instaleaza joblib...
pip install joblib

echo.
echo [6/8] Se instaleaza streamlit...
pip install streamlit

echo.
echo [7/8] Se instaleaza Pillow...
pip install Pillow

echo.
echo [8/8] Se instaleaza requests...
pip install requests

echo.
echo ========================================================
echo Operatiune completa!
echo Toate bibliotecile au fost verificate/instalate.
echo ========================================================
pause