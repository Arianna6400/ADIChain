from models.model_base import Model

#Costruttore e attributi della tabella Patients
class Patients(Model):
    def __init__(self, username, name, lastname, birthday, birth_place, residence, autonomous, phone, id_patient=None):
        super().__init__()
        self.id_patient = id_patient
        self.username = username
        self.name = name
        self.lastname = lastname
        self.birthday = birthday
        self.birth_place = birth_place
        self.residence = residence
        self.autonomous = autonomous
        self.phone = phone
    
    def get_id_patient(self):
        return self.id_patient
    
    def get_username(self):
        return self.username

    def get_name(self):
        return self.name
    
    def get_lastaname(self):
        return self.lastname
    
    def get_birthday(self):
        return self.birthday
    
    def get_birth_place(self):
        return self.birth_place
    
    def get_residence(self):
        return self.residence
    
    def get_autonomous(self):
        return self.autonomous
    
    def get_phone(self):
        return self.phone

#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_patient is None:
            self.cur.execute('''INSERT INTO Patients (username, name, lastname, birthday, birth_place, residence, autonomous, phone)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                             (self.username, self.name, self.lastname, self.birthday, self.birth_place, self.residence, self.autonomous, self.phone))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE Patients SET username=?, name=?, lastname=?, birthday=?, birth_place=?, residence=?, autonomous=?, phone=? WHERE id_patient=?''',
                             (self.username, self.name, self.lastname, self.birthday, self.birth_place, self.residence, self.autonomous, self.phone, self.id_patient))
        self.conn.commit()
        self.id_patient = self.cur.lastrowid

    def delete(self):
        if self.id_patient is not None:
            self.cur.execute('DELETE FROM Patients WHERE id_patient=?', (self.id_patient,))
            self.conn.commit()
