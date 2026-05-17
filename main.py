import cv2
import time
from face_recognition_system import FaceRecognitionSystem
from attendance import AttendanceManager
from utils import draw_modern_box, get_greeting_message

def main():
    print("=========================================================")
    print("🎓   SmartPresence - Système de Reconnaissance Faciale  🎓")
    print("=========================================================\n")
    
    # 1. Initialiser le système de reconnaissance et la gestion des présences
    face_system = FaceRecognitionSystem(students_dir="students")
    attendance_manager = AttendanceManager(report_dir="reports")
    
    # 2. Ouvrir la webcam système
    print("🎥 Initialisation de la caméra...")
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("❌ Erreur : Impossible d'accéder à la caméra système.")
        print("   Veuillez vérifier que votre webcam est connectée et n'est pas utilisée par une autre application.")
        return

    # Ajuster la résolution de capture (facultatif mais recommandé pour une belle image)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("🟢 Système démarré avec succès !")
    print("👉 Astuce : Placez les visages des étudiants dans le champ de la caméra.")
    print("👉 Appuyez sur la touche 'q' pour quitter proprement le programme.")
    print("---------------------------------------------------------")

    # Dictionnaire pour gérer l'affichage temporaire des messages d'accueil
    # Clé: Nom de l'étudiant, Valeur: Le temps en secondes de la détection
    active_greetings = {}

    # Variable pour mesurer le taux de rafraîchissement (FPS)
    prev_frame_time = 0
    new_frame_time = 0

    while True:
        # Lire la trame (frame) actuelle de la webcam
        ret, frame = video_capture.read()
        if not ret:
            print("⚠️ Impossible de lire les images depuis la caméra. Fermeture...")
            break
            
        # Effet miroir horizontal pour que ce soit plus intuitif à l'écran
        frame = cv2.flip(frame, 1)

        # Calculer les FPS (frames par seconde) pour surveiller la performance
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # 3. Exécuter la détection et la reconnaissance
        face_locations, face_names = face_system.recognize_faces(frame)

        # 4. Traitement et Affichage graphique pour chaque visage
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Comme on a réduit l'image par 4 dans 'recognize_faces',
            # on doit multiplier par 4 les coordonnées pour les dessiner sur l'image d'origine.
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Choix des couleurs du cadre selon l'identification :
            # Vert = Étudiant enregistré
            # Rouge = Visage inconnu
            color = (46, 204, 113) if name != "Inconnu" else (231, 76, 60) # Couleurs modernes HSL/RGB

            # Dessiner la boîte moderne autour du visage
            draw_modern_box(frame, top, right, bottom, left, name, color)

            # Si l'étudiant est identifié, on gère son enregistrement
            if name != "Inconnu":
                # Essayer d'enregistrer la présence de l'étudiant
                is_marked = attendance_manager.mark_attendance(name)
                
                if is_marked:
                    print(f"🎉 [PRESENCE] {name} a été marqué PRÉSENT à {time.strftime('%H:%M:%S')}")
                    # Enregistrer le moment de détection pour afficher le message d'accueil
                    active_greetings[name] = time.time()

        # 5. Affichage des messages d'accueil à l'écran
        current_time = time.time()
        y_offset = 50 # Position de départ verticale pour afficher les messages
        
        for name, detection_time in list(active_greetings.items()):
            # Afficher le message d'accueil pendant 4 secondes maximum
            if current_time - detection_time < 4.0:
                greeting_text = get_greeting_message(name)
                
                # Dessiner une bannière de bienvenue translucide (fond vert menthe professionnel)
                cv2.rectangle(frame, (15, y_offset - 30), (450, y_offset + 10), (46, 204, 113), cv2.FILLED)
                
                # Texte noir très lisible par-dessus
                cv2.putText(frame, greeting_text, (25, y_offset - 5), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.65, (255, 255, 255), 1, cv2.LINE_AA)
                
                y_offset += 55 # Décaler vers le bas pour le message suivant si plusieurs détections
            else:
                # Supprimer le message expiré de notre liste active
                del active_greetings[name]

        # 6. Affichage du tableau de bord système en bas de l'écran
        h, w, _ = frame.shape
        
        # Bandeau noir translucide de pied de page pour un look moderne et pro
        cv2.rectangle(frame, (0, h - 50), (w, h), (44, 62, 80), cv2.FILLED)
        
        # Affichage du compteur de présences
        total_presents = attendance_manager.get_total_presents()
        cv2.putText(frame, f"Etudiants presents aujourd'hui : {total_presents}", (20, h - 18), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Affichage des FPS à droite
        cv2.putText(frame, f"FPS: {int(fps)}", (w - 110, h - 18), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.55, (149, 165, 166), 1, cv2.LINE_AA)

        # Afficher la fenêtre avec les interfaces graphiques enrichies
        cv2.imshow('SmartPresence v1.0 - Suivi Inteligent des Presences', frame)

        # 7. Quitter la boucle si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libération propre de la caméra et destruction de toutes les fenêtres OpenCV
    print("\n---------------------------------------------------------")
    print("🛑 Arrêt du système...")
    video_capture.release()
    cv2.destroyAllWindows()
    print("👋 Système SmartPresence fermé. Passez une excellente journée !")

if __name__ == "__main__":
    main()
