import face_recognition
import os
import cv2
import numpy as np

class FaceRecognitionSystem:
    """
    Gère le chargement des images de référence des étudiants,
    le calcul de leurs encodages faciaux et la reconnaissance en temps réel.
    """
    def __init__(self, students_dir="students"):
        self.students_dir = students_dir
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Détection dynamique et flexible de l'accélération GPU
        import dlib
        self.use_gpu = dlib.DLIB_USE_CUDA
        self.model_name = "cnn" if self.use_gpu else "hog"
        
        print("=========================================================")
        if self.use_gpu:
            print("🚀 ACCÉLÉRATION GPU : ACTIVÉE (Modèle CNN Haute Précision)")
        else:
            print("💻 ACCÉLÉRATION GPU : INDISPONSIBLE (Utilisation CPU - Modèle HOG)")
        print(f"   Modèle de détection actif : {self.model_name.upper()}")
        print("=========================================================\n")
        
        # S'assurer que le dossier des étudiants existe
        if not os.path.exists(self.students_dir):
            os.makedirs(self.students_dir)
            
        # Charger directement tous les visages connus
        self.load_known_faces()

    def load_known_faces(self):
        """
        Scanne le dossier 'students/', charge chaque image et calcule son encodage.
        Le nom du fichier (sans extension) est utilisé comme identifiant de l'étudiant.
        """
        print(f"🔄 Balayage du dossier '{self.students_dir}' à la recherche de visages...")
        
        # Liste tous les fichiers dans le dossier
        files = os.listdir(self.students_dir)
        
        if not files:
            print("⚠️ Le dossier 'students/' est vide. Veuillez y ajouter des photos (.jpg, .png, .jpeg) !")
            return
            
        for filename in files:
            # Filtrer pour ne garder que les formats d'images courants
            if filename.lower().endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(self.students_dir, filename)
                
                # Extraire le nom de l'étudiant à partir du nom de fichier (ex: Ahmed.jpg -> Ahmed)
                student_name = os.path.splitext(filename)[0]
                
                try:
                    # 1. Charger le fichier image avec face_recognition
                    image = face_recognition.load_image_file(image_path)
                    
                    # 2. Extraire les coordonnées et encodages du visage dans l'image
                    encodings = face_recognition.face_encodings(image)
                    
                    if len(encodings) > 0:
                        # On prend le premier visage trouvé dans l'image
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_names.append(student_name)
                        print(f"   ✅ Visage encodé pour l'étudiant : {student_name}")
                    else:
                        print(f"   ❌ Aucun visage détecté dans l'image : {filename}")
                except Exception as e:
                    print(f"   💥 Erreur lors du chargement de {filename} : {e}")
                    
        print(f"📊 Initialisation terminée : {len(self.known_face_names)} visage(s) chargé(s).\n")

    def recognize_faces(self, frame):
        """
        Prend un frame (image de la webcam), détecte tous les visages et les compare
        avec la base de données des visages connus.
        
        Args:
            frame: Image capturée par OpenCV.
            
        Returns:
            face_locations: Liste des coordonnées des visages détectés.
            face_names: Liste des noms correspondants aux visages détectés.
        """
        # Redimensionner l'image à 1/4 de sa taille pour accélérer le traitement du flux vidéo
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # OpenCV utilise le format BGR, face_recognition utilise le format RGB.
        # Il faut donc convertir l'image.
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Détecter toutes les zones de visage dans le frame actuel en utilisant le modèle flexible (GPU/CPU)
        face_locations = face_recognition.face_locations(rgb_small_frame, model=self.model_name)
        
        # Calculer les encodages faciaux pour chaque visage détecté
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        
        for face_encoding in face_encodings:
            name = "Inconnu"
            
            # Comparer si le visage correspond à notre liste connue
            if len(self.known_face_encodings) > 0:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.55)
                
                # Calculer la distance euclidienne par rapport à tous nos visages connus
                # Une distance plus petite signifie une meilleure ressemblance
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                
                # Sélectionner l'index ayant la plus petite distance
                best_match_index = np.argmin(face_distances)
                
                # Si le match est validé à cet index, on associe le nom de l'étudiant
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    
            face_names.append(name)
            
        return face_locations, face_names
