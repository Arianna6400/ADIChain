from models.model_base import Model

#Costruttore e attributi della tabella Caregivers
class Caregivers(Model):
    def __init__(self, username_patient, username, name, lastname, relationship, phone):
        super().__init__()
        self.username_patient = username_patient
        self.username = username
        self.name = name
        self.lastname = lastname
        self.relationship = relationship
        self.phone = phone

    def get_username_patient(self):
        return self.username_patient

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name

    def get_lastname(self):
        return self.lastname

    def get_relationship(self):
        return self.relationship

    def get_phone(self):
        return self.phone 
    
    def set_username_patient(self, username_patient):
        self.username_patient = username_patient

    def set_username(self, username):
        self.username = username
    
    def set_name(self, name):
        self.name = name
    
    def set_lastname(self, lastname):
        self.lastname = lastname
    
    def set_relationship(self, relationship):
        self.relationship = relationship
    
    def set_phone(self, phone):
        self.phone = phone   

# Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        try: 
            if self.username is None:
                self.cur.execute('''INSERT INTO Caregivers (username_patient, username, name, lastname, relationship, phone)
                                    VALUES (?, ?, ?, ?, ?, ?)''',
                                (self.username_patient, self.username, self.name, self.lastname, self.relationship, self.phone))
                                    #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
            else:
                self.cur.execute('''UPDATE Caregivers SET username_patient=?, name=?, lastname=?, relationship=?, phone=? WHERE username=?''',
                                (self.username_patient, self.name, self.lastname, self.relationship, self.phone, self.username))
            self.conn.commit()
            self.username = self.cur.lastrowid
            print('Information saved correctly!\n')
        except: 
            print('Internal error!')

    def delete(self):
        if self.username is not None:
            self.cur.execute('DELETE FROM Caregivers WHERE username=?', (self.username,))
            self.conn.commit()
