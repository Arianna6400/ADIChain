from models.model_base import Model

class Caregivers(Model):
    """
    This class represents a Caregiver model inheriting from the base Model class.
    It handles the interaction with the Caregivers table in the database.
    """

    def __init__(self, username_patient, username, name, lastname, relationship, phone):
        """
        Initializes a new instance of the Caregivers class with details about the caregiver.

        Parameters:
        - username_patient: the username of the patient whom the caregiver looks after
        - username: the username for the caregiver
        - name: the first name of the caregiver
        - lastname: the last name of the caregiver
        - relationship: the relationship of the caregiver to the patient
        - phone: the phone number of the caregiver
        """
        super().__init__()
        self.username_patient = username_patient
        self.username = username
        self.name = name
        self.lastname = lastname
        self.relationship = relationship
        self.phone = phone

    # Getter methods for each attribute
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

    # Setter methods for each attribute
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

    def save(self):
        """
        Saves or updates a Caregiver record in the database. Implements the ORM pattern.
        """
        try: 
            if self.username is None:
                # Inserts new caregiver if no username is set
                self.cur.execute(
                    '''INSERT INTO Caregivers (username_patient, username, name, lastname, relationship, phone)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (self.username_patient, self.username, self.name, self.lastname, self.relationship, self.phone))
            else:
                # Updates existing caregiver details based on username
                self.cur.execute(
                    '''UPDATE Caregivers SET username_patient=?, name=?, lastname=?, relationship=?, phone=? WHERE username=?''',
                    (self.username_patient, self.name, self.lastname, self.relationship, self.phone, self.username))
            self.conn.commit()
            self.username = self.cur.lastrowid  # Updating the username with last inserted row id
            print('Information saved correctly!\n')
        except Exception as e: 
            print('Internal error!', str(e))

    def delete(self):
        """
        Deletes a Caregiver record from the database based on the username.
        """
        if self.username is not None:
            self.cur.execute('DELETE FROM Caregivers WHERE username=?', (self.username,))
            self.conn.commit()
