from db.db_operations import DatabaseOperations
from session.session import Session


class Controller:

    def __init__(self, session: Session):
        self.db_ops = DatabaseOperations()
        self.session = session
        self.__n_attempts_limit = 5
        self.__timeout_timer = 180        


    def registration(self, username: str, password: str, role: str, public_key: str, private_key: str):
        registration_code = self.db_ops.register_creds(username, password, role, public_key, private_key)

        if registration_code == 0:
           print("Done") 

        return registration_code
    
    def insert_patient_info(self, name: str, lastname: str, birthday: str, birth_place: str, residence: str, autonomous: bool, phone: str):
        insertion_code = self.db_ops.insert_patient(name, lastname, birthday, birth_place, residence, autonomous, phone)

        if insertion_code == 0:
            print("Done")

        return insertion_code
    
    def insert_medic_info(self, name: str, lastname: str, birthday: str, specialization: str, mail: str, phone: str):
        insertion_code = self.db_ops.insert_medic(name, lastname, birthday, specialization, mail, phone)

        if insertion_code == 0:
            print("Done")

        return insertion_code
    
    def insert_caregiver_info(self, name: str, lastname: str, id_patient: int, relationship: str, phone: str):
        insertion_code = self.db_ops.insert_caregiver(name, lastname, id_patient, relationship, phone)

        if insertion_code == 0:
            print("Done")

    