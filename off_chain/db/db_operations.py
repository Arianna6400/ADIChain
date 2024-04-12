import sqlite3
import os
import hashlib

from config import config

class DatabaseOperations:

    def __init__(self):
        self.conn = sqlite3.connect(config.config["db_path"])
        self.cur = self.conn.cursor()
        self._create_new_table()

        self.n_param = 2
        self.r_param = 8
        self.p_param = 1
        self.dklen_param = 64

    def _create_new_table(self):
        self.cur.execute('''CREATE TABLE Credentials(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash_password TEXT NOT NULL,
            role TEXT CHECK(role IN ('MEDIC', 'PATIENT', 'CAREGIVER')) NOT NULL,
            public_key TEXT NOT NULL,
            private_key TEXT NOT NULL
            );''')
        self.cur.execute('''CREATE TABLE Medics(
            id_medic INTEGER NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            specialization TEXT NOT NULL,
            mail TEXT,
            phone TEXT,
            FOREIGN KEY(id_medic) REFERENCES Credentials(id)
            );''')
        self.cur.execute('''CREATE TABLE Patients(
            id_patient INTEGER NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            birth_place TEXT NOT NULL,
            residence TEXT NOT NULL,
            autonomous INTEGER CHECK(autonomous IN (0,1)) NOT NULL,
            phone TEXT, 
            FOREIGN KEY(id_patient) REFERENCES Credentials(id)
            );''')
        self.cur.execute('''CREATE TABLE Caregivers(
            id_caregiver INTEGER NOT NULL,
            id_patient INTEGER NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            patient_relationship TEXT NOT NULL,
            phone TEXT,
            FOREIGN KEY(id_caregiver) REFERENCES Credentials(id),
            FOREIGN KEY(id_patient) REFERENCES Patients(id_patient)
            );''')
        self.cur.execute('''CREATE TABLE Reports(
            id_report INTEGER PRIMARY KEY AUTOINCREMENT,
            id_patient INTEGER NOT NULL,
            id_medic INTEGER NOT NULL,
            analyses TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            FOREIGN KEY(id_patient) REFERENCES Patients(id_patient),
            FOREIGN KEY(id_medic) REFERENCES Medics(id_medic)
            );''')
        self.cur.execute('''CREATE TABLE TreatmentPlans(
            id_treament_plan INTEGER PRIMARY KEY AUTOINCREMENT,
            id_patient INTEGER NOT NULL,
            id_medic INTEGER NOT NULL,
            id_caregiver INTGER,
            description TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY(id_patient) REFERENCES Patients(id_patient),
            FOREIGN KEY(id_medic) REFERENCES Medics(id_medic),
            FOREIGN KEY(id_caregiver) REFERENCES Caregivers(id_caregiver)
            );''')
        self.cur.execute('''CREATE TABLE AccessLog(
            id_access INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utente INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(id_utente) REFERENCES Credentials(id)
            );''')
        self.cur.execute('''
            INSERT INTO Credentials VALUES
            ('1','carlo', '123456', 'MEDIC', 'aaaaa', 'bbbbbbb')
            ''')
        self.conn.commit()
    

    def register(self, username, hash_password, role, public_key, private_key):
        try:
            hashed_passwd = self.hash_function(hash_password)
            self.cur.execute("""
                             INSERT INTO Credentials
                             (username, hash_password, role, public_key, private_key) VALUES (?, ?, ?, ?, ?)""",
                             (
                                 username,
                                 hashed_passwd,
                                 role,
                                 public_key,
                                 private_key
                             ))
            self.conn.commit()
            return 0
        except sqlite3.DatabaseError:
            return -1
        except sqlite3.IntegrityError:
            return -2
        

    def hash_function(self, password: str):

        """Hashes the supplied password using the scrypt algorithm.
    
        Args:
            password: The password to hash.
            n: CPU/Memory cost factor.
            r: Block size.
            p: Parallelization factor.
            dklen: Length of the derived key.
    
        Returns:
            A string containing the hashed password and the parameters used for hashing.
        """

        salt = os.urandom(16)
        digest = hashlib.scrypt(
            password.encode(), 
            salt = salt,
            n = self.n_param,
            r = self.r_param,
            p = self.p_param,
            dklen = self.dklen_param
        )
        hashed_passwd = f"{digest.hex()}${salt.hex()}${self.n_param}${self.r_param}${self.p_param}${self.dklen_param}"
        return hashed_passwd

