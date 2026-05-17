# 🎓 SmartPresence - Système Intelligent de Gestion des Présences par IA

**SmartPresence** est un projet complet en Python basé sur la reconnaissance faciale en temps réel. Il a été conçu spécifiquement dans un but pédagogique pour les étudiants débutants ou intermédiaires en informatique et intelligence artificielle (adapté pour les Travaux Pratiques universitaires).

Le système permet de détecter automatiquement les visages des étudiants via la webcam, de les comparer à une base de données d'images connues, d'afficher un accueil personnalisé et de consigner automatiquement leur présence dans un rapport CSV horodaté et sécurisé contre les doublons.

---

## 🎯 Objectifs du Projet

1. **Reconnaissance en Temps Réel** : Capturer le flux vidéo d'une webcam, y détecter les visages et les identifier instantanément.
2. **Interface Graphique Moderne** : Mettre en place un affichage soigné avec des cadres de détection stylisés et des animations textuelles.
3. **Automatisation administrative** : Éliminer la corvée de l'appel papier en générant un rapport numérique de présence.
4. **Zéro Doublon** : Garantir qu'un étudiant n'est enregistré qu'une seule fois par session pour éviter de surcharger les fichiers de données.

---

## 🛠️ Technologies Utilisées

* **Python 3.8+** : Le cœur de l'application.
* **OpenCV (`opencv-python`)** : Gère la capture du flux vidéo de la caméra, le traitement d'image et le rendu de l'interface en temps réel.
* **face_recognition** : Développé au-dessus de **dlib**, ce module utilise des réseaux de neurones profonds (Deep Learning) pour générer des encodages faciaux ultra-précis à 128 dimensions.
* **Pandas** : Utilisé pour structurer les données et exporter facilement le rapport au format `.csv`.
* **NumPy** : Utilisé en arrière-plan pour les calculs de distance euclidienne rapide entre les encodages faciaux.

---

## 📂 Structure du Projet

```bash
SmartPresence/
│
├── students/                  # Base d'images des étudiants (ex: Ahmed.jpg, Sara.png)
├── reports/                   # Dossier contenant les rapports CSV générés
│
├── main.py                    # Script principal orchestrant la capture et l'affichage
├── face_recognition_system.py # Moteur IA (chargement et comparaison de visages)
├── attendance.py              # Logique de gestion et d'exportation des présences
├── utils.py                   # Fonctions graphiques et helpers de salutation
│
├── requirements.txt           # Dépendances externes à installer
└── README.md                  # Ce guide d'utilisation et de documentation
```

---

## 🚀 Guide d'Installation et Lancement

### Étape 1 : Prérequis système
Certaines dépendances comme `face_recognition` s'appuient sur `dlib`, qui nécessite un compilateur C++ installé sur votre système :
* **Sur Windows** : Installez [Visual Studio Build Tools](https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/) et cochez l'option *Développement Desktop en C++*.
* **Sur macOS / Linux** : Installez CMake via Homebrew ou votre gestionnaire de paquets (`brew install cmake` ou `sudo apt install cmake`).

### Étape 2 : Installer les bibliothèques Python
Clonez ou téléchargez le projet, ouvrez votre terminal ou invite de commande dans le répertoire `SmartPresence`, et exécutez la commande suivante :
```bash
pip install -r requirements.txt
```

### Étape 3 : Alimenter la base de données d'étudiants
1. Ouvrez le dossier `students/` (s'il n'existe pas encore, il sera créé au premier démarrage).
2. Ajoutez-y des photos de portraits de vos camarades ou de vous-même.
3. **Format du nom** : Nommez chaque fichier selon l'identité de l'étudiant (par exemple : `Ahmed.jpg`, `Sara.png`, `Youssef.jpeg`). Le programme chargera automatiquement ces noms pour l'affichage !

### Étape 4 : Démarrer l'application
Lancez le script principal via la commande :
```bash
python main.py
```
* **Pour quitter l'application** : Cliquez sur la fenêtre d'affichage et appuyez sur la touche **`q`** de votre clavier.

---

## 🧠 Explication pas-à-pas du Code

Le projet est modulaire afin de faciliter l'apprentissage et le débogage :

### 1. [utils.py](file:///c:/Users/Hamza/Desktop/Desktop-folders/estem-2025/S2/TP/AI_PYTHON/SmartPresence/utils.py) - Design & Cosmétique
Ce module contient deux fonctions cruciales :
* `draw_modern_box(...)` : Dessine un rectangle autour du visage détecté. Au lieu d'un rectangle classique OpenCV uniforme, cette fonction ajoute des sur-épaisseurs aux quatre coins de la boîte pour donner un style "ATH / Technologique" moderne de haute qualité, ainsi qu'un bandeau coloré pour le nom.
* `get_greeting_message(...)` : Détermine de manière adaptative si l'étudiant est un homme ou une femme en fonction de son prénom afin d'afficher un accueil distingué : *« Bonjour Monsieur Ahmed »* ou *« Bonjour Madame Sara »*.

### 2. [attendance.py](file:///c:/Users/Hamza/Desktop/Desktop-folders/estem-2025/S2/TP/AI_PYTHON/SmartPresence/attendance.py) - Suivi & Exportation
Gère l'écriture dans le fichier CSV :
* Initialise un nom de fichier unique basé sur la date du jour : `reports/presence_report_AAAA-MM-JJ.csv`.
* Charge le fichier existant s'il existe déjà pour reprendre le travail de la journée.
* La méthode `mark_attendance(name)` utilise une structure de type `set` (`self.recorded_names`) pour une recherche rapide en complexité $O(1)$ afin de rejeter instantanément les doublons. Si l'étudiant est vu pour la première fois, il est inséré avec son nom, l'heure exacte à la seconde près, et le statut "Présent".

### 3. [face_recognition_system.py](file:///c:/Users/Hamza/Desktop/Desktop-folders/estem-2025/S2/TP/AI_PYTHON/SmartPresence/face_recognition_system.py) - L'Intelligence Artificielle
Ce module encapsule l'algorithme d'IA :
* **Phase d'initialisation** : Parcourt le dossier `students/`, extrait le visage de chaque image, puis génère un encodage (une signature numérique unique du visage).
* **Phase de détection** : Pendant la diffusion de la webcam, l'image est réduite de 75 % (mise à l'échelle 0.25) pour garantir un flux fluide (taux de FPS élevé). Les visages détectés sont comparés aux signatures connues grâce à un seuil de tolérance (fixé à 0.55 pour maximiser la précision).

### 4. [main.py](file:///c:/Users/Hamza/Desktop/Desktop-folders/estem-2025/S2/TP/AI_PYTHON/SmartPresence/main.py) - Chef d'Orchestre
Il relie tous les modules :
* Ouvre le périphérique vidéo.
* Démarre une boucle infinie de traitement d'images.
* Fait appel à `FaceRecognitionSystem` pour obtenir la position des visages et les noms associés.
* Enregistre les présences via `AttendanceManager`.
* Affiche des messages d'accueil temporaires en haut de l'écran pendant exactement 4 secondes avant de les effacer proprement.
* Affiche un tableau de bord moderne en bas de l'écran qui affiche en temps réel le nombre total d'élèves présents aujourd'hui ainsi que les FPS système.

---

## 📈 Exemples de Livrables Générés

### Structure du fichier de rapport (`reports/presence_report_2026-05-17.csv`) :
```csv
Nom,Heure de présence,Statut
Ahmed,10:19:15,Présent
Sara,10:20:02,Présent
Youssef,10:20:45,Présent
```

---

## 🚀 Pistes d'Améliorations Futures (Pour vos projets universitaires)

Si vous souhaitez étendre ce TP universitaire, voici quelques pistes intéressantes à explorer :
1. **Intégration d'une Base de Données** : Remplacer le système d'enregistrement CSV par une base de données SQL (SQLite ou MySQL) afin de stocker des fiches d'étudiants plus complètes (Classe, Filière, Adresse mail).
2. **Notifications Automatiques** : Ajouter un script d'envoi d'e-mail automatique (via `smtplib`) pour alerter les parents d'élèves ou l'administration en cas d'absence.
3. **Interface Graphique avec Tkinter ou PyQt** : Construire une belle interface utilisateur de bureau avec des boutons pour ajouter/supprimer des photos d'étudiants directement depuis l'application.
4. **Calcul de l'heure limite** : Ajouter une règle de gestion des retards (Ex: si l'heure d'arrivée est supérieure à 08h15, le statut devient automatiquement "En retard" au lieu de "Présent").
