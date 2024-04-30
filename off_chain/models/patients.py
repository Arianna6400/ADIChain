from models.model_base import Model

#Costruttore e attributi della tabella Patients
class Patients(Model):
    def __init__(self, username, name, lastname, birthday, birth_place, residence, autonomous, phone):
        super().__init__()
        self.username = username
        self.name = name
        self.lastname = lastname
        self.birthday = birthday
        self.birth_place = birth_place
        self.residence = residence
        self.autonomous = autonomous
        self.phone = phone
    
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
    
    def set_name(self, name):
        self.name = name
    
    def set_lastname(self, lastname):
        self.lastname = lastname
    
    def set_birthday(self, birthday):
        self.birthday = birthday
    
    def set_birth_place(self, birth_place):
        self.birth_place = birth_place
    
    def set_residence(self, residence):
        self.residence = residence
    
    def set_autonomous(self, autonomous):
        self.autonomous = autonomous
    
    def set_phone(self, phone):
        self.phone = phone

#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        try:
            if self.username is None:
                self.cur.execute('''INSERT INTO Patients (username, name, lastname, birthday, birth_place, residence, autonomous, phone)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                (self.username, self.name, self.lastname, self.birthday, self.birth_place, self.residence, self.autonomous, self.phone))
                                    #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
            else:
                self.cur.execute(""" UPDATE Patients SET name = ?, lastname = ?, birthday = ?, birth_place = ?, residence = ?, phone = ? WHERE username = ? """,
                                (self.name, self.lastname, self.birthday, self.birth_place, self.residence, self.phone, self.username))
            self.conn.commit()
            self.username = self.cur.lastrowid
            print('Informations saved correctly!\n')
        except Exception as e: 
            print (e)
            print('Internal error!')

    def delete(self):
        if self.username is not None:
            self.cur.execute('DELETE FROM Patients WHERE username=?', (self.username,))
            self.conn.commit()
