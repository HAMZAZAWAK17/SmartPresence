import cv2

def draw_modern_box(frame, top, right, bottom, left, name, color=(0, 255, 0)):
    """
    Dessine un rectangle moderne avec des angles renforcés autour du visage 
    et affiche le nom de la personne avec un style professionnel.
    
    Args:
        frame: L'image (frame) de la vidéo sur laquelle dessiner.
        top, right, bottom, left: Les coordonnées du visage.
        name: Le nom de la personne détectée.
        color: La couleur du rectangle (BGR).
    """
    # Épaisseur du rectangle de base
    thickness = 2
    cv2.rectangle(frame, (left, top), (right, bottom), color, 1) # rectangle plus fin pour le contour complet
    
    # Longueur des segments pour les coins renforcés
    line_length = 20
    corner_thickness = 4
    
    # Coin Haut-Gauche
    cv2.line(frame, (left, top), (left + line_length, top), color, corner_thickness)
    cv2.line(frame, (left, top), (left, top + line_length), color, corner_thickness)
    
    # Coin Haut-Droite
    cv2.line(frame, (right, top), (right - line_length, top), color, corner_thickness)
    cv2.line(frame, (right, top), (right, top + line_length), color, corner_thickness)
    
    # Coin Bas-Gauche
    cv2.line(frame, (left, bottom), (left + line_length, bottom), color, corner_thickness)
    cv2.line(frame, (left, bottom), (left, bottom - line_length), color, corner_thickness)
    
    # Coin Bas-Droite
    cv2.line(frame, (right, bottom), (right - line_length, bottom), color, corner_thickness)
    cv2.line(frame, (right, bottom), (right, bottom - line_length), color, corner_thickness)

    # Style pour l'affichage du nom sous la boîte
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.6
    font_thickness = 1
    
    # Obtenir la taille du texte pour ajuster l'arrière-plan
    text_size = cv2.getTextSize(name, font, font_scale, font_thickness)[0]
    
    # Dessiner l'arrière-plan du texte (un rectangle plein sous le visage)
    cv2.rectangle(frame, 
                  (left, bottom), 
                  (left + text_size[0] + 14, bottom + text_size[1] + 12), 
                  color, 
                  cv2.FILLED)
    
    # Dessiner le texte en blanc par-dessus l'arrière-plan coloré
    cv2.putText(frame, 
                name, 
                (left + 7, bottom + text_size[1] + 6), 
                font, 
                font_scale, 
                (255, 255, 255), 
                font_thickness, 
                cv2.LINE_AA)

def get_greeting_message(name):
    """
    Génère un message d'accueil poli en français selon le prénom.
    Sépare les salutations Monsieur et Madame de façon simple et adaptative.
    """
    # Liste de prénoms féminins courants (modifiable et extensible)
    female_names = [
        "sara", "sarah", "fatima", "khadija", "aya", "nour", 
        "salma", "amina", "mariam", "meryem", "zineb", "yasmine",
        "chaima", "hafsa", "douae", "imane", "hajar", "kenza",
        "jessica", "salwa", "wissal"
    ]
    
    # Convertir en minuscule pour une comparaison insensible à la casse
    name_lower = name.lower()
    
    if name_lower in female_names:
        return f"Bonjour Madame {name}"
    else:
        return f"Bonjour Monsieur {name}"
