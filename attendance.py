import pandas as pd
from datetime import datetime
import os

class AttendanceManager:
    """
    Gère l'enregistrement et le suivi des présences quotidiennes des étudiants.
    Enregistre les données dans un fichier CSV tout en évitant les doublons.
    """
    def __init__(self, report_dir="reports"):
        self.report_dir = report_dir
        
        # S'assurer que le dossier reports existe
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
            
        # Nom de fichier unique pour chaque jour (Exemple: reports/presence_report_2026-05-17.csv)
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.report_path = os.path.join(self.report_dir, f"presence_report_{self.current_date}.csv")
        
        # Charger les données existantes si le fichier existe déjà, sinon en créer un nouveau
        if os.path.exists(self.report_path):
            try:
                self.df = pd.read_csv(self.report_path)
            except Exception as e:
                print(f"⚠️ Erreur lors de la lecture du fichier existant: {e}. Création d'un nouveau fichier.")
                self.df = pd.DataFrame(columns=["Nom", "Heure de présence", "Statut"])
        else:
            self.df = pd.DataFrame(columns=["Nom", "Heure de présence", "Statut"])
            
        # Set pour stocker les étudiants déjà enregistrés aujourd'hui afin de bloquer les doublons instantanément
        self.recorded_names = set(self.df["Nom"].tolist())

    def mark_attendance(self, name):
        """
        Marque un étudiant présent s'il ne l'est pas déjà.
        
        Args:
            name: Le nom de l'étudiant reconnu.
            
        Returns:
            True si l'étudiant vient d'être marqué présent (première détection de la journée).
            False si l'étudiant était déjà enregistré aujourd'hui ou si c'est une personne "Inconnue".
        """
        # Ne pas enregistrer les personnes inconnues
        if name == "Inconnu":
            return False
            
        # Vérifier si l'étudiant n'est pas déjà marqué présent aujourd'hui
        if name not in self.recorded_names:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            
            # Créer une nouvelle ligne avec le nom, l'heure actuelle et le statut 'Présent'
            new_record = pd.DataFrame([{
                "Nom": name,
                "Heure de présence": time_str,
                "Statut": "Présent"
            }])
            
            # Concaténer la nouvelle présence au DataFrame global
            self.df = pd.concat([self.df, new_record], ignore_index=True)
            
            # Sauvegarder immédiatement le DataFrame mis à jour dans le fichier CSV
            self.df.to_csv(self.report_path, index=False)
            
            # Ajouter au set pour bloquer les futures tentatives aujourd'hui
            self.recorded_names.add(name)
            return True
            
        return False
        
    def get_total_presents(self):
        """
        Retourne le nombre total d'étudiants marqués présents aujourd'hui.
        """
        return len(self.recorded_names)
