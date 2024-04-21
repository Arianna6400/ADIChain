from models.model_base import Model

#Costruttore e attributi della tabella Medics
class Medics(Model):
    def __init__(self, id_medic, username, name, lastname, birthday, specialization, mail, phone):
        super().__init__()
        self.id_medic = id_medic
        self.username = username
        self.name = name
        self.lastname = lastname
        self.birthday = birthday
        self.specialization = specialization
        self.mail = mail
        self.phone = phone

    def get_id_medic(self):
        return self.id_medic
    
    def get_username(self):
        return self.username

    def get_name(self):
        return self.name
    
    def get_lastname(self):
        return self.lastname
    
    def get_birthday(self):
        return self.birthday
    
    def get_specialization(self):
        return self.specialization
    
    def get_mail(self):
        return self.mail
    
    def get_phone(self):
        return self.phone

#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_medic is None:
            self.cur.execute('''INSERT INTO Medics (username, name, lastname, birthday, specialization, mail, phone)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', (self.username, self.name, self.lastname, self.birthday, self.specialization, self.mail, self.phone))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE Medics SET username =?, name=?, lastname=?, birthday=?, specialization=?, mail=?, phone=? WHERE id_medic=?''',
                             (self.username, self.name, self.lastname, self.birthday, self.specialization, self.mail, self.phone, self.id_medic))
        self.conn.commit()
        self.id_medic = self.cur.lastrowid

    def delete(self):
        if self.id_medic is not None:
            self.cur.execute('DELETE FROM Medics WHERE id_medic=?', (self.id_medic))
            self.conn.commit()
