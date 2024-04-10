from model_base import Model

#Costruttore e attributi della tabella Reports
class Reports(Model):
    def __init__(self, id_patient, id_medic, analysis, diagnosis, id_report=None):
        super().__init__()
        self.id_report = id_report
        self.id_patient = id_patient
        self.id_medic = id_medic
        self.analysis = analysis
        self.diagnosis = diagnosis

    def get_id_report(self):
        return self.id_report
    
    def get_id_patient(self):
        return self.id_patient
    
    def get_id_medic(self):
        return self.id_medic
    
    def get_analyses(self):
        return self.analysis
    
    def get_diagnosis(self):
        return self.diagnosis
    
#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_report is None:
            self.cur.execute('''INSERT INTO Reports (id_patient, id_medic, analyses, diagnosis, phone)
                                VALUES (?, ?, ?, ?, ?)''',
                             (self.id_patient, self.id_medic, self.analysis, self.diagnosis, self.phone))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE Reports SET id_patient=?, id_medic=?, analyses=?, diagnosis=?, phone=? WHERE id_report=?''',
                             (self.id_patient, self.id_medic, self.analysis, self.diagnosis, self.phone, self.id_report))
        self.conn.commit()
        self.id_report = self.cur.lastrowid

    def delete(self):
        if self.id_report is not None:
            self.cur.execute('DELETE FROM Reports WHERE id_report=?', (self.id_report,))
            self.conn.commit()
