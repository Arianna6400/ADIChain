from models.model_base import Model

#Costruttore e attributi della tabella Caregivers
class Caregivers(Model):
    def __init__(self, username_patient, username, name, lastname, patient_relationship, phone, id_caregiver=None):
        super().__init__()
        self.id_caregiver = id_caregiver
        self.username_patient = username_patient
        self.username = username
        self.name = name
        self.lastname = lastname
        self.patient_relationship = patient_relationship
        self.phone = phone

    def get_id_caregiver(self):
        return self.id_caregiver

    def username_patient(self):
        return self.username_patient

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name

    def get_lastname(self):
        return self.lastname

    def get_patient_relationship(self):
        return self.patient_relationship

    def get_phone(self):
        return self.phone    

#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_caregiver is None:
            self.cur.execute('''INSERT INTO Caregivers (username_patient, username, name, lastname, patient_relationship, phone)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (self.username_patient, self.username, self.name, self.lastname, self.patient_relationship, self.phone))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE Caregivers SET username_patient=?, username=?, name=?, lastname=?, patient_relationship=?, phone=? WHERE id_caregiver=?''',
                             (self.username_patient, self.username, self.name, self.lastname, self.patient_relationship, self.phone, self.id_caregiver))
        self.conn.commit()
        self.id_caregiver = self.cur.lastrowid

    def delete(self):
        if self.id_caregiver is not None:
            self.cur.execute('DELETE FROM Caregivers WHERE id_caregiver=?', (self.id_caregiver,))
            self.conn.commit()
