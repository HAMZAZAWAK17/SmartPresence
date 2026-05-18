import cv2
import time
from face_recognition_system import FaceRecognitionSystem
from attendance import AttendanceManager
from utils import draw_modern_box, get_greeting_message, draw_translucent_rect

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

    # Variables pour la détection fluide sans retard (Frame Skipping)
    last_face_locations = []
    last_face_names = []
    process_this_frame = True

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
        fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 30
        prev_frame_time = new_frame_time

        # 3. Exécuter la détection et la reconnaissance (1 trame sur 2 pour éliminer les retards)
        if process_this_frame:
            last_face_locations, last_face_names = face_system.recognize_faces(frame)
        
        process_this_frame = not process_this_frame

        # 4. Traitement et Affichage graphique pour chaque visage (dessiné sur chaque trame pour la fluidité)
        for (top, right, bottom, left), name in zip(last_face_locations, last_face_names):
            # Comme on a réduit l'image par 4 dans 'recognize_faces',
            # on doit multiplier par 4 les coordonnées pour les dessiner sur l'image d'origine.
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Choix des couleurs du cadre selon l'identification :
            # Vert menthe = Étudiant enregistré, Rouge corail = Visage inconnu
            color = (46, 204, 113) if name != "Inconnu" else (231, 76, 60)

            # Dessiner la boîte moderne HUD autour du visage
            draw_modern_box(frame, top, right, bottom, left, name, color)

            # Si l'étudiant est identifié, on gère son enregistrement
            if name != "Inconnu":
                # Essayer d'enregistrer la présence de l'étudiant
                is_marked = attendance_manager.mark_attendance(name)
                
                if is_marked:
                    print(f"🎉 [PRESENCE] {name} a été marqué PRÉSENT à {time.strftime('%H:%M:%S')}")
                    # Enregistrer le moment de détection pour afficher le message d'accueil
                    active_greetings[name] = time.time()

        # 5. Affichage des messages d'accueil translucides à l'écran
        current_time = time.time()
        y_offset = 60 # Position de départ verticale pour afficher les messages
        
        for name, detection_time in list(active_greetings.items()):
            # Afficher le message d'accueil pendant 4 secondes maximum
            if current_time - detection_time < 4.0:
                greeting_text = get_greeting_message(name)
                
                # Carte d'accueil haute technologie translucide
                bg_card_color = (25, 28, 36) # Anthracite
                accent_color = (46, 204, 113) # Vert menthe
                
                # Rectangle translucide pour le fond de la carte
                draw_translucent_rect(frame, (20, y_offset - 35), (460, y_offset + 18), bg_card_color, alpha=0.85)
                # Bordure fine colorée
                cv2.rectangle(frame, (20, y_offset - 35), (460, y_offset + 18), accent_color, 1, cv2.LINE_AA)
                # Ligne verticale d'accentuation à gauche
                cv2.rectangle(frame, (20, y_offset - 35), (25, y_offset + 18), accent_color, cv2.FILLED)
                
                # Petit badge titre
                cv2.putText(frame, "NOTIFICATION / PRESENCE VALIDEE", (35, y_offset - 18), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.38, accent_color, 1, cv2.LINE_AA)
                
                # Message de bienvenue
                cv2.putText(frame, greeting_text, (35, y_offset + 6), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                
                y_offset += 65 # Décaler vers le bas pour le message suivant si plusieurs détections
            else:
                # Supprimer le message expiré de notre liste active
                del active_greetings[name]

        # 6. Affichage du tableau de bord système en bas de l'écran
        h, w, _ = frame.shape
        
        # Bandeau de fond translucide haute technologie
        bg_bar_color = (15, 18, 24) # Bleu-gris très sombre
        draw_translucent_rect(frame, (0, h - 50), (w, h), bg_bar_color, alpha=0.90)
        
        # Ligne de séparation supérieure style néon bleu
        border_color = (41, 128, 185) # Bleu cobalt
        cv2.line(frame, (0, h - 50), (w, h - 50), border_color, 1, cv2.LINE_AA)
        
        # Mode d'exécution (GPU vs CPU)
        mode_text = "MODE GPU (CNN)" if face_system.use_gpu else "MODE CPU (HOG)"
        mode_color = (46, 204, 113) if face_system.use_gpu else (149, 165, 166)
        
        # Affichage du compteur de présences à gauche
        total_presents = attendance_manager.get_total_presents()
        cv2.putText(frame, f"[+] Etudiants presents : {total_presents}", (20, h - 18), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.50, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Affichage du mode au centre
        cv2.putText(frame, f"System : {mode_text}", (w // 2 - 120, h - 18), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.50, mode_color, 1, cv2.LINE_AA)
        
        # Affichage des FPS à droite
        cv2.putText(frame, f"Vitesse : {int(fps)} FPS", (w - 180, h - 18), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.50, (41, 128, 185), 1, cv2.LINE_AA)

        # Afficher la fenêtre avec les interfaces graphiques enrichies
        cv2.imshow('SmartPresence v1.1 - Suivi Intelligent des Presences', frame)

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
