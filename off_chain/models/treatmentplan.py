from models.model_base import Model

#Modello e attributi per la tabella TreatmentPlans
class TreatmentPlans(Model):
    def __init__(self, id_patient, id_medic, id_caregiver, description, start_date, end_date, id_treatment_plan=None):
        super().__init__()
        self.id_treatment_plan = id_treatment_plan
        self.id_patient = id_patient
        self.id_medic = id_medic
        self.id_caregiver = id_caregiver
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def get_id_treatment_plan(self):
        return self.id_treatment_plan
    
    def get_id_patient(self):
        return self.id_patient
    
    def get_id_medic(self):
        return self.id_medic
    
    def get_id_caregiver(self):
        return self.id_caregiver
    
    def get_description(self):
        return self.description
    
    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date
    
#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_treatment_plan is None:
            self.cur.execute('''INSERT INTO TreatmentPlans (id_patient, id_medic, id_caregiver, description, start_date, end_date)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (self.id_patient, self.id_medic, self.id_caregiver, self.description, self.start_date, self.end_date))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE TreatmentPlans SET id_patient=?, id_medic=?, id_caregiver=?, description=?, start_date=?, end_date=? WHERE id_treatment_plan=?''',
                             (self.id_patient, self.id_medic, self.id_caregiver, self.description, self.start_date, self.end_date, self.id_treatment_plan))
        self.conn.commit()
        self.id_treatment_plan = self.cur.lastrowid

    def delete(self):
        if self.id_treatment_plan is not None:
            self.cur.execute('DELETE FROM TreatmentPlans WHERE id_treatment_plan=?', (self.id_treatment_plan,))
            self.conn.commit()
