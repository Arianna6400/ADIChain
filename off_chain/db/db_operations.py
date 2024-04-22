import sqlite3
import os
import hashlib

from config import config
from models.medics import Medics
from models.patients import Patients
from models.caregivers import Caregivers
from models.credentials import Credentials

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

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Credentials(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL, 
            hash_password TEXT NOT NULL,
            role TEXT CHECK(UPPER(role) IN ('MEDIC', 'PATIENT', 'CAREGIVER')) NOT NULL,
            public_key TEXT NOT NULL,
            private_key TEXT NOT NULL
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Medics(
            id_medic INTEGER NOT NULL,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            specialization TEXT NOT NULL,
            mail TEXT,
            phone TEXT,
            FOREIGN KEY(username) REFERENCES Credentials(username)
            FOREIGN KEY(id_medic) REFERENCES Credentials(id)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Patients(
            id_patient INTEGER NOT NULL,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            birth_place TEXT NOT NULL,
            residence TEXT NOT NULL,
            autonomous INTEGER CHECK(autonomous IN (0,1)) NOT NULL,
            phone TEXT, 
            FOREIGN KEY(username) REFERENCES Credentials(username)
            FOREIGN KEY(id_patient) REFERENCES Credentials(id)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Caregivers(
            id_caregiver INTEGER NOT NULL,
            username_patient TEXT NOT NULL,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            relationship TEXT NOT NULL,
            phone TEXT,
            FOREIGN KEY(username) REFERENCES Credentials(username)
            FOREIGN KEY(id_caregiver) REFERENCES Credentials(id),
            FOREIGN KEY(username_patient) REFERENCES Patients(username)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Reports(
            id_report INTEGER PRIMARY KEY AUTOINCREMENT,
            id_patient INTEGER NOT NULL,
            id_medic INTEGER NOT NULL,
            analyses TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            FOREIGN KEY(id_patient) REFERENCES Patients(id_patient),
            FOREIGN KEY(id_medic) REFERENCES Medics(id_medic)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS TreatmentPlans(
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
        self.cur.execute('''CREATE TABLE IF NOT EXISTS AccessLog(
            id_access INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utente INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(id_utente) REFERENCES Credentials(id)
            );''')
        self.conn.commit()
    

    def register_creds(self, username, hash_password, role, public_key, private_key):
        try:
            # Check if the username already exists in the Credentials table
            if self.check_username(username) == 0:
            #if existing_username_count == 0:
                # Username doesn't exist, proceed with insertion
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
            else:
                return -1  # Username already exists
        except sqlite3.IntegrityError:
            return -1

    def check_username(self, username):
        self.cur.execute("SELECT COUNT(*) FROM Credentials WHERE username = ?", (username,))
        if self.cur.fetchone()[0] == 0: return 0
        else: return -1
        
    def insert_patient(self, username, name, lastname, birthday, birth_place, residence, autonomous, phone):
        try:
            self.cur.execute("""
                            INSERT INTO Patients
                            (id_patient, username, name, lastname, birthday, birth_place, residence, autonomous, phone)
                            SELECT last_insert_rowid(), ?, ?, ?, ?, ?, ?, ?, ?
                            FROM Credentials""",
                            (
                                username,
                                name, 
                                lastname,
                                birthday,
                                birth_place,
                                residence,
                                autonomous,
                                phone
                            ))
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            return -1
        
    def insert_medic(self, username, name, lastname, birthday, specialization, mail, phone):
        try:
            self.cur.execute("""
                            INSERT INTO Medics
                            (id_medic, username, name, lastname, birthday, specialization, mail, phone) SELECT last_insert_rowid(), ?, ?, ?, ?, ?, ?, ?
                            FROM Credentials""",
                            (
                                username,
                                name,
                                lastname,
                                birthday,
                                specialization,
                                mail,
                                phone
                            ))
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            return -1

    def insert_caregiver(self, username, name, lastname, username_patient, relationship, phone):
        try:
            self.cur.execute("""
                            INSERT INTO Caregivers
                            (id_caregiver, username, name, lastname, username_patient, relationship, phone) SELECT last_insert_rowid(), ?, ?, ?, ?, ?, ?
                            FROM Credentials""",
                            (
                                username,
                                name, 
                                lastname,
                                username_patient,
                                relationship,
                                phone
                            ))
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            return -1

    def check_patient_by_username(self, username):
            self.cur.execute("SELECT COUNT(*) FROM Patients WHERE username = ?", (username,))
            if self.cur.fetchone()[0] == 0: return 0
            else: return -1

    def get_creds_by_username(self, username):
        creds = self.cur.execute("""
                                SELECT *
                                FROM Credentials
                                WHERE username=?""", (username,))
        user_attr = creds.fetchone()
        if user_attr is not None:
                creds = Credentials(user_attr[0], user_attr[1], user_attr[2], user_attr[3], user_attr[4], user_attr[5])
                return creds
        return None

    def get_user_by_username(self, username, role):
        if role == 'medic':
            user = self.cur.execute("""
                                    SELECT *
                                    FROM Medics
                                    WHERE Medics.username = ?""", (username,))
            user_attr = user.fetchone()
            if user_attr is not None:
                medic = Medics(user_attr[0], user_attr[1], user_attr[2], user_attr[3], user_attr[4], user_attr[5], user_attr[6], user_attr[7])
                return medic
        elif role == 'patient':
            user = self.cur.execute("""
                                    SELECT *
                                    FROM Patients
                                    WHERE Patients.username = ?""", (username,))
            user_attr = user.fetchone()
            if user_attr is not None: 
                patient = Patients(user_attr[0], user_attr[1], user_attr[2], user_attr[3], user_attr[4], user_attr[5], user_attr[6], user_attr[7], user_attr[8])
                return patient
        elif role == 'caregiver':
            user = self.cur.execute("""
                                     SELECT *
                                     FROM Caregivers
                                     WHERE Caregivers.username = ?""", (username,))
            user_attr = user.fetchone()
            #if user_attr is not None:
            #    caregiver = Caregivers(user_attr[0], user_attr[1], user_attr[2], user_attr[3], user_attr[4], user_attr[5], user_attr[6])
            #    return caregiver
            #return user
            return user_attr
        return None

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

    
    def check_credentials(self, username, password, public_key, private_key):
        creds = self.get_creds_by_username(username)
        if(creds is not None and self.check_passwd(username, password) and creds.get_public_key() == public_key and private_key == creds.get_private_key()):
            return True
        else:
            return False
    

    def check_passwd(self, username, password):

        result = self.cur.execute("""
                                SELECT hash_password
                                FROM Credentials
                                WHERE username =?""", (username,))
        hash = result.fetchone()
        if hash:
            saved_hash = hash[0]
            params = saved_hash.split('$')
            hashed_passwd = hashlib.scrypt(
                password.encode('utf-8'),
                salt=bytes.fromhex(params[1]),
                n = int(params[2]),
                r = int(params[3]),
                p = int(params[4]),
                dklen= int(params[5])
            )
        return hashed_passwd.hex() == params[0]
    
