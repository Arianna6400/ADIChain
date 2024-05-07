from models.model_base import Model

class Medics(Model):
    """
    This class represents the Medics model that stores medical professional details,
    extending the functionality provided by the Model class.
    """

    def __init__(self, username, name, lastname, birthday, specialization, mail, phone):
        """
        Initializes a new instance of the Medics class with the provided medical professional details.

        Parameters:
        - username: Unique identifier for the medic
        - name: First name of the medic
        - lastname: Last name of the medic
        - birthday: Date of birth of the medic
        - specialization: Medical specialization of the medic
        - mail: Email address of the medic
        - phone: Contact phone number of the medic
        """
        super().__init__()
        self.username = username
        self.name = name
        self.lastname = lastname
        self.birthday = birthday
        self.specialization = specialization
        self.mail = mail
        self.phone = phone
    
    # Getter methods for each attribute
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
    
    # Setter methods for each attribute
    def set_username(self, username):
        self.username = username

    def set_name(self, name):
        self.name = name
    
    def set_lastname(self, lastname):
        self.lastname = lastname
    
    def set_birthday(self, birthday):
        self.birthday = birthday
    
    def set_specialization(self, specialization):
        self.specialization = specialization
    
    def set_mail(self, mail):
        self.mail = mail
    
    def set_phone(self, phone):
        self.phone = phone

    def save(self):
        """
        Saves a new or updates an existing Medic record in the database.
        Implements SQL queries to insert or update details based on the presence of a username.
        """
        try:
            if self.username is None:
                # Insert new medic record
                self.cur.execute('''INSERT INTO Medics (username, name, lastname, birthday, specialization, mail, phone)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (self.username, self.name, self.lastname, self.birthday, self.specialization, self.mail, self.phone))
            else:
                # Update existing medic details
                self.cur.execute('''UPDATE Medics SET name=?, lastname=?, birthday=?, specialization=?, mail=?, phone=? WHERE username=?''',
                                (self.name, self.lastname, self.birthday, self.specialization, self.mail, self.phone, self.username))
            self.conn.commit()
            self.username = self.cur.lastrowid
            print('Information saved correctly!\n')
        except: 
            print('Internal error!')

    def delete(self):
        """
        Deletes a Medic record from the database based on its username.
        """
        if self.username is not None:
            self.cur.execute('DELETE FROM Medics WHERE username=?', (self.username))
            self.conn.commit()
