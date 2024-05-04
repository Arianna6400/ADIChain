from models.model_base import Model

#Costruttore e attributi della tabella Reports
class Reports(Model):
    def __init__(self, id_report, username_patient, username_medic, analyses, diagnosis):
        super().__init__()
        self.id_report = id_report
        self.username_patient = username_patient
        self.username_medic = username_medic
        self.analyses = analyses
        self.diagnosis = diagnosis
        #DATA da inserire (oggi?)

    def get_id_report(self):
        return self.id_report
    
    def get_username_patient(self):
        return self.username_patient
    
    def get_username_medic(self):
        return self.username_medic
    
    def get_analyses(self):
        return self.analyses
    
    def get_diagnosis(self):
        return self.diagnosis
    
#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_report is None:
            self.cur.execute('''INSERT INTO Reports (username_patient, username_medic, analyses, diagnosis, phone)
                                VALUES (?, ?, ?, ?, ?)''',
                             (self.username_patient, self.username_medic, self.analyses, self.diagnosis, self.phone))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE Reports SET username_patient=?, username_medic=?, analyses=?, diagnosis=?, phone=? WHERE id_report=?''',
                             (self.username_patient, self.username_medic, self.analyses, self.diagnosis, self.phone, self.id_report))
        self.conn.commit()
        self.id_report = self.cur.lastrowid

    def delete(self):
        if self.id_report is not None:
            self.cur.execute('DELETE FROM Reports WHERE id_report=?', (self.id_report,))
            self.conn.commit()
