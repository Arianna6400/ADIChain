from models.model_base import Model
from colorama import Fore, Style, init

class Patients(Model):
    """
    This class represents the Patients model that stores personal and medical information about patients,
    extending the functionality provided by the Model class.
    """

    init(convert=True)

    def __init__(self, username, name, lastname, birthday, birth_place, residence, autonomous, phone):
        """
        Initializes a new instance of the Patients class with the provided details about the patient.

        Parameters:
        - username: Unique identifier for the patient
        - name: First name of the patient
        - lastname: Last name of the patient
        - birthday: Date of birth of the patient
        - birth_place: Birth place of the patient
        - residence: Current residence of the patient
        - autonomous: Boolean indicating if the patient is autonomous
        - phone: Contact phone number of the patient
        """
        super().__init__()
        self.username = username
        self.name = name
        self.lastname = lastname
        self.birthday = birthday
        self.birth_place = birth_place
        self.residence = residence
        self.autonomous = autonomous
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
    
    def get_birth_place(self):
        return self.birth_place
    
    def get_residence(self):
        return self.residence
    
    def get_autonomous(self):
        return self.autonomous
    
    def get_phone(self):
        return self.phone
    
    # Setter methods for each attribute
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

    def save(self):
        """
        Saves a new or updates an existing Patient record in the database.
        Implements SQL queries to insert or update details based on the presence of a username.
        """
        try:
            if self.username is None:
                # Insert new patient record
                self.cur.execute('''INSERT INTO Patients (username, name, lastname, birthday, birth_place, residence, autonomous, phone)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                (self.username, self.name, self.lastname, self.birthday, self.birth_place, self.residence, self.autonomous, self.phone))
            else:
                # Update existing patient details
                self.cur.execute(""" UPDATE Patients SET name = ?, lastname = ?, birthday = ?, birth_place = ?, residence = ?, phone = ? WHERE username = ? """,
                                (self.name, self.lastname, self.birthday, self.birth_place, self.residence, self.phone, self.username))
            self.conn.commit()
            self.username = self.cur.lastrowid # Update the username with the last inserted row ID if new record
            print(Fore.GREEN + 'Information saved correctly!\n' + Style.RESET_ALL)
        except Exception as e: 
            print(Fore.RED + 'Internal error!' + Style.RESET_ALL, e)

    def delete(self):
        """
        Deletes a Patient record from the database based on its username.
        """
        if self.username is not None:
            self.cur.execute('DELETE FROM Patients WHERE username=?', (self.username,))
            self.conn.commit()
