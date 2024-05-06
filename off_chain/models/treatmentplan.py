from models.model_base import Model

#Modello e attributi per la tabella TreatmentPlans
class TreatmentPlans(Model):
    def __init__(self, id_treatment_plan, date, username_patient, username_medic, username_caregiver, description, start_date, end_date):
        super().__init__()
        self.id_treatment_plan = id_treatment_plan
        self.username_patient = username_patient
        self.username_medic = username_medic
        self.username_caregiver = username_caregiver
        #if autonomous == 0
        self.description = description
        
        self.start_date = start_date
        self.end_date = end_date

    def get_id_treatment_plan(self):
        return self.id_treatment_plan
    
    def get_username_patient(self):
        return self.username_patient
    
    def get_username_medic(self):
        return self.username_medic
    
    def get_username_caregiver(self):
        return self.username_caregiver
    
    def get_description(self):
        return self.description
    
    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date
    
#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_treatment_plan is None:
            self.cur.execute('''INSERT INTO TreatmentPlans (username_patient, username_medic, username_caregiver, description, start_date, end_date)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (self.username_patient, self.username_medic, self.username_caregiver, self.description, self.start_date, self.end_date))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE TreatmentPlans SET username_patient=?, username_medic=?, username_caregiver=?, description=?, start_date=?, end_date=? WHERE id_treatment_plan=?''',
                             (self.username_patient, self.username_medic, self.username_caregiver, self.description, self.start_date, self.end_date, self.id_treatment_plan))
        self.conn.commit()
        self.id_treatment_plan = self.cur.lastrowid

    def delete(self):
        if self.id_treatment_plan is not None:
            self.cur.execute('DELETE FROM TreatmentPlans WHERE id_treatment_plan=?', (self.id_treatment_plan,))
            self.conn.commit()
