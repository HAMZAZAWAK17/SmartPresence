import cv2
import time
import math
import numpy as np

def draw_translucent_rect(frame, pt1, pt2, color, alpha=0.6):
    """
    Dessine un rectangle semi-transparent sur l'image pour un effet de verre/HUD moderne.
    Très optimisé : ne traite que la zone découpée du rectangle.
    """
    x1, y1 = pt1
    x2, y2 = pt2
    
    # Limiter les coordonnées à la taille de l'image pour éviter les erreurs d'index
    h, w, _ = frame.shape
    x1 = max(0, min(x1, w - 1))
    x2 = max(0, min(x2, w - 1))
    y1 = max(0, min(y1, h - 1))
    y2 = max(0, min(y2, h - 1))
    
    if x2 <= x1 or y2 <= y1:
        return
        
    sub_img = frame[y1:y2, x1:x2]
    rect_img = np.full(sub_img.shape, color, dtype=np.uint8)
    res = cv2.addWeighted(sub_img, 1 - alpha, rect_img, alpha, 0)
    frame[y1:y2, x1:x2] = res

def draw_modern_box(frame, top, right, bottom, left, name, color=(46, 204, 113)):
    """
    Dessine un masque HUD ultra-moderne de style cybernétique/IA autour du visage.
    Inclut :
      - Un rectangle de délimitation ultra-fin.
      - Des coins renforcés lumineux (effet néon).
      - Un balayage laser (scanline) animé.
      - Une carte d'information translucide avec icône et badge d'état.
    """
    face_w = right - left
    face_h = bottom - top
    
    # 1. Overlay léger semi-transparent sur le visage détecté (effet ciblage technologique)
    # On met une opacité de 8% pour un effet "radar" très subtil
    draw_translucent_rect(frame, (left, top), (right, bottom), color, alpha=0.08)
    
    # 2. Rectangle de base très fin (1px) pour encadrer le visage
    cv2.rectangle(frame, (left, top), (right, bottom), color, 1, cv2.LINE_AA)
    
    # 3. Coins renforcés style HUD (effet néon épais)
    line_length = max(15, int(face_w * 0.15))
    corner_thickness = 3
    
    # Haut-Gauche
    cv2.line(frame, (left, top), (left + line_length, top), color, corner_thickness, cv2.LINE_AA)
    cv2.line(frame, (left, top), (left, top + line_length), color, corner_thickness, cv2.LINE_AA)
    
    # Haut-Droite
    cv2.line(frame, (right, top), (right - line_length, top), color, corner_thickness, cv2.LINE_AA)
    cv2.line(frame, (right, top), (right, top + line_length), color, corner_thickness, cv2.LINE_AA)
    
    # Bas-Gauche
    cv2.line(frame, (left, bottom), (left + line_length, bottom), color, corner_thickness, cv2.LINE_AA)
    cv2.line(frame, (left, bottom), (left, bottom - line_length), color, corner_thickness, cv2.LINE_AA)
    
    # Bas-Droite
    cv2.line(frame, (right, bottom), (right - line_length, bottom), color, corner_thickness, cv2.LINE_AA)
    cv2.line(frame, (right, bottom), (right, bottom - line_length), color, corner_thickness, cv2.LINE_AA)
    
    # 4. Balayage laser horizontal animé (Scanline)
    # Utilise le temps système pour créer un mouvement continu de haut en bas
    t = time.time()
    scan_ratio = 0.5 + 0.5 * math.sin(t * 5.0)  # Oscille doucement entre 0 et 1
    scan_y = int(top + face_h * scan_ratio)
    
    # Dessiner la ligne de scan avec un léger effet lumineux
    cv2.line(frame, (left + 2, scan_y), (right - 2, scan_y), color, 1, cv2.LINE_AA)
    # Ligne d'effet halo plus épaisse et plus translucide autour du laser
    draw_translucent_rect(frame, (left + 4, max(top, scan_y - 2)), (right - 4, min(bottom, scan_y + 2)), color, alpha=0.20)
    
    # 5. Carte d'information moderne (badge HUD)
    # On affiche la carte en bas ou en haut selon la place disponible
    card_height = 46
    card_width = max(180, face_w + 40)
    
    # Centrer la carte d'info par rapport au visage
    card_left = left + (face_w - card_width) // 2
    # S'assurer que la carte ne sort pas de l'écran horizontalement
    frame_h, frame_w, _ = frame.shape
    card_left = max(10, min(card_left, frame_w - card_width - 10))
    
    # Positionnement vertical de la carte (au-dessus du visage par défaut, en dessous si pas de place)
    if top - card_height - 10 > 10:
        card_top = top - card_height - 10
        card_bottom = top - 10
    else:
        card_top = bottom + 10
        card_bottom = bottom + card_height + 10
        
    # Dessiner le fond de la carte translucide noir/bleu foncé (style verre givré)
    bg_color = (25, 28, 36) # Gris anthracite pro
    draw_translucent_rect(frame, (card_left, card_top), (card_left + card_width, card_bottom), bg_color, alpha=0.85)
    
    # Dessiner la bordure de la carte (fine bordure colorée)
    cv2.rectangle(frame, (card_left, card_top), (card_left + card_width, card_bottom), color, 1, cv2.LINE_AA)
    
    # Petite barre verticale d'accentuation sur le côté gauche de la carte
    cv2.rectangle(frame, (card_left, card_top), (card_left + 4, card_bottom), color, cv2.FILLED)
    
    # Style de police
    font = cv2.FONT_HERSHEY_DUPLEX
    
    # Icône et Texte d'état selon la détection
    if name != "Inconnu":
        status_text = "PRESENCE VALIDEE"
        status_color = (46, 204, 113) # Vert menthe
        display_name = name.upper()
        icon_char = "[OK]"
    else:
        status_text = "ACCES REFUSE / HORS BASE"
        status_color = (231, 76, 60) # Rouge corail
        display_name = "INCONNU"
        icon_char = "[!?]"
        
    # Dessiner l'état de détection en petit texte majuscule
    cv2.putText(frame, status_text, (card_left + 12, card_top + 15), font, 0.35, status_color, 1, cv2.LINE_AA)
    
    # Dessiner le nom en plus grand et blanc brillant
    cv2.putText(frame, f"{icon_char} {display_name}", (card_left + 12, card_top + 34), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

def get_greeting_message(name):
    """
    Génère un message d'accueil poli en français selon le prénom.
    Sépare les salutations Monsieur et Madame de façon simple et adaptative.
    """
    female_names = [
        "sara", "sarah", "fatima", "khadija", "aya", "nour", 
        "salma", "amina", "mariam", "meryem", "zineb", "yasmine",
        "chaima", "hafsa", "douae", "imane", "hajar", "kenza",
        "jessica", "salwa", "wissal"
    ]
    
    name_lower = name.lower()
    
    if name_lower in female_names:
        return f"Bonjour Madame {name} !"
    else:
        return f"Bonjour Monsieur {name} !"

