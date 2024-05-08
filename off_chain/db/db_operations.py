"""
This module handles all database operations for various user roles and their associated data within the system.
It manages the creation, update, and retrieval of user data through a series of defined methods.
"""

import datetime
import sqlite3
import os
import hashlib

from config import config
from models.medics import Medics
from models.patients import Patients
from models.caregivers import Caregivers
from models.credentials import Credentials
from models.treatmentplan import TreatmentPlans
from models.reports import Reports

class DatabaseOperations:
    """
    Handles all interactions with the database for user data manipulation and retrieval.
    This class manages the connection to the database and executes SQL queries to manage the data.
    """

    def __init__(self):
        """
        Initializes the database connection and cursor, and creates new tables if they do not exist.
        """
        self.conn = sqlite3.connect(config.config["db_path"])
        self.cur = self.conn.cursor()
        self._create_new_table()

        self.n_param = 2
        self.r_param = 8
        self.p_param = 1
        self.dklen_param = 64

        self.today_date = datetime.date.today().strftime('%Y-%m-%d')

    def _create_new_table(self):
        """
        Creates necessary tables in the database if they are not already present.
        This ensures that the database schema is prepared before any operations are performed.
        """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Credentials(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL, 
            hash_password TEXT NOT NULL,
            role TEXT CHECK(UPPER(role) IN ('MEDIC', 'PATIENT', 'CAREGIVER')) NOT NULL,
            public_key TEXT NOT NULL,
            private_key TEXT NOT NULL
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Medics(
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            specialization TEXT NOT NULL,
            mail TEXT,
            phone TEXT,
            FOREIGN KEY(username) REFERENCES Credentials(username)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Patients(
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            birth_place TEXT NOT NULL,
            residence TEXT NOT NULL,
            autonomous INTEGER CHECK(autonomous IN (0,1)) NOT NULL,
            phone TEXT, 
            FOREIGN KEY(username) REFERENCES Credentials(username)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Caregivers(
            username_patient TEXT NOT NULL,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            relationship TEXT NOT NULL,
            phone TEXT,
            FOREIGN KEY(username) REFERENCES Credentials(username)
            FOREIGN KEY(username_patient) REFERENCES Patients(username)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Reports(
            id_report INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            username_patient TEXT NOT NULL,
            username_medic TEXT NOT NULL,
            analyses TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            FOREIGN KEY(username_patient) REFERENCES Patients(username),
            FOREIGN KEY(username_medic) REFERENCES Medics(username)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS TreatmentPlans(
            id_treament_plan INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            username_patient TEXT NOT NULL,
            username_medic TEXT NOT NULL,
            description TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY(username_patient) REFERENCES Patients(username),
            FOREIGN KEY(username_medic) REFERENCES Medics(username)
            );''')
        self.conn.commit()
    
    def register_creds(self, username, hash_password, role, public_key, private_key):
        """
        Registers new user credentials in the database.
        
        Args:
            username (str): Username of the user.
            hash_password (str): Password to be hashed and stored.
            role (str): Role of the user (e.g., MEDIC, PATIENT, CAREGIVER).
            public_key (str): Public key for user encryption.
            private_key (str): Private key for user encryption.
        Returns:
            int: 0 if registration is successful, -1 if username already exists.
        """
        try:
            if self.check_username(username) == 0:
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
        """
        Check if a username exists in the Credentials table.

        Args:
            username (str): Username to check in the database.
        Returns:
            int: 0 if username does not exist, -1 if it does.
        """
        self.cur.execute("SELECT COUNT(*) FROM Credentials WHERE username = ? UNION ALL SELECT COUNT(*) FROM Patients WHERE username = ?", (username, username,))
        if self.cur.fetchone()[0] == 0: return 0
        else: return -1

    def check_unique_phone_number(self, phone):
        """
        Checks if a phone number is unique across multiple tables in the database.

        Args:
            phone (str): The phone number to check for uniqueness.

        Returns:
            int: 0 if the phone number is not found in any records (unique), -1 if it is found (not unique).
        """
        query_patients = "SELECT COUNT(*) FROM Patients WHERE phone = ?"
        self.cur.execute(query_patients, (phone,))
        count_patients = self.cur.fetchone()[0]

        query_medics = "SELECT COUNT(*) FROM Medics WHERE phone = ?"
        self.cur.execute(query_medics, (phone,))
        count_medics = self.cur.fetchone()[0]

        query_caregivers = "SELECT COUNT(*) FROM Caregivers WHERE phone = ?"
        self.cur.execute(query_caregivers, (phone,))
        count_caregivers = self.cur.fetchone()[0]

        if count_patients == 0 and count_medics == 0 and count_caregivers == 0:
            return 0 
        else:
            return -1  
        
    def check_unique_email(self, mail):
        """
        Checks if an email address is unique within the Medics table in the database.

        Args:
            mail (str): The email address to check for uniqueness.

        Returns:
            int: 0 if the email address is not found in the Medics records (unique), -1 if it is found (not unique).
        """
        query_medics = "SELECT COUNT(*) FROM Medics WHERE mail = ?"
        self.cur.execute(query_medics, (mail,))
        count_medics = self.cur.fetchone()[0]

        if count_medics == 0:
            return 0 
        else:
            return -1

    def key_exists(self, public_key, private_key):
        """
        Checks if either a public key or a private key already exists in the Credentials table.

        Args:
            public_key (str): The public key to check against existing entries in the database.
            private_key (str): The private key to check against existing entries in the database.

        Returns:
            bool: True if either the public or private key is found in the database (indicating they are not unique),
                  False if neither key is found (indicating they are unique) or an exception occurs during the query.
        
        Exceptions:
            Exception: Catches and prints any exception that occurs during the database operation, returning False.
        """
        try:
            query = "SELECT public_key, private_key FROM Credentials WHERE public_key=? OR private_key=?"
            existing_users = self.cur.execute(query, (public_key, private_key)).fetchall()
            return len(existing_users) > 0
        except Exception as e:
            print("An error occurred:", e)
            return False 
        
    def insert_patient(self, username, name, lastname, birthday, birth_place, residence, autonomous, phone):
        """
        Inserts a new patient record into the Patients table in the database.

        Args:
            username (str): The unique username for the patient.
            name (str): The first name of the patient.
            lastname (str): The last name of the patient.
            birthday (str): The birth date of the patient in YYYY-MM-DD format.
            birth_place (str): The birthplace of the patient.
            residence (str): The current residence address of the patient.
            autonomous (int): An integer (0 or 1) indicating whether the patient is autonomous.
            phone (str): The phone number of the patient.

        Returns:
            int: 0 if the insertion was successful, -1 if an integrity error occurred (e.g., duplicate username).

        Exceptions:
            sqlite3.IntegrityError: Catches and handles integrity errors from the database if, for instance, the
                                    username is not unique, preventing the patient's data from being inserted.
        """
        try:
            self.cur.execute("""
                            INSERT INTO Patients
                            (username, name, lastname, birthday, birth_place, residence, autonomous, phone)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?) """,
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
        
    def insert_report(self, username_patient, username_medic, analyses, diagnosis):
        """
        Inserts a new medical report into the Reports table in the database.

        Args:
            username_patient (str): The username of the patient to whom the report pertains.
            username_medic (str): The username of the medic who is creating the report.
            analyses (str): Descriptions of any analyses that were performed as part of the medical evaluation.
            diagnosis (str): The diagnosis given to the patient based on the analyses.

        Returns:
            int: 0 if the insertion was successful, -1 if an integrity error occurred, such as duplicate entries
                or reference integrity issues.

        Exceptions:
            sqlite3.IntegrityError: Handles integrity errors that occur during the insertion process, typically
                                    related to database constraints like unique keys or foreign key constraints.
        """
        try:
            self.cur.execute("""
                            INSERT INTO Reports
                            (date, username_patient, username_medic, analyses, diagnosis)
                            VALUES (?, ?, ?, ?, ?) """,
                            (
                                self.today_date,
                                username_patient, 
                                username_medic,
                                analyses,
                                diagnosis
                            ))
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            return -1
        
    def insert_treatment_plan(self, username_patient, username_medic, description, start_date, end_date):
        """
        Inserts a new treatment plan into the TreatmentPlans table in the database.

        Args:
            username_patient (str): The username of the patient for whom the treatment plan is created.
            username_medic (str): The username of the medic responsible for the treatment plan.
            description (str): A detailed description of the treatment plan.
            start_date (datetime.date or str): The start date of the treatment plan. If provided as a datetime.date
                                            object, it will be formatted to a string.
            end_date (datetime.date or str): The end date of the treatment plan. If provided as a datetime.date
                                            object, it will be formatted to a string.

        Returns:
            int: 0 if the insertion was successful, -1 if an integrity error occurred, which might be due to issues
                like duplicate entries or database constraints.

        Exceptions:
            sqlite3.IntegrityError: Handles integrity errors from the database, such as violations of primary key
                                    constraints or foreign key constraints, ensuring that the database integrity is maintained.
        """
        try:
            start_date_str = start_date.strftime('%Y-%m-%d') if isinstance(start_date, datetime.date) else start_date
            end_date_str = end_date.strftime('%Y-%m-%d') if isinstance(end_date, datetime.date) else end_date
            self.cur.execute("""
                            INSERT INTO TreatmentPlans
                            (date, username_patient, username_medic, description, start_date, end_date)
                            VALUES (?, ?, ?, ?, ?, ?) """,
                            (
                                self.today_date,
                                username_patient, 
                                username_medic,
                                description,
                                start_date_str,
                                end_date_str
                            ))
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            return -1
        
    def insert_medic(self, username, name, lastname, birthday, specialization, mail, phone):
        """
        Inserts a new medic record into the Medics table in the database.

        Args:
            username (str): The unique identifier for the medic.
            name (str): The first name of the medic.
            lastname (str): The last name of the medic.
            birthday (str): The birth date of the medic in YYYY-MM-DD format.
            specialization (str): The medical specialization or department of the medic.
            mail (str): The email address of the medic.
            phone (str): The contact phone number of the medic.

        Returns:
            int: 0 if the insertion was successful, -1 if an integrity error occurred, such as violating unique constraints
                or foreign key references.

        Exceptions:
            sqlite3.IntegrityError: Catches and handles any integrity errors during the insertion process, which typically occur
                                    due to violation of database constraints like unique keys or foreign key constraints.
        """
        try:
            self.cur.execute("""
                            INSERT INTO Medics
                            (username, name, lastname, birthday, specialization, mail, phone) 
                            VALUES (?, ?, ?, ?, ?, ?, ?) """,
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
        """
        Inserts a new caregiver record into the Caregivers table in the database.

        Args:
            username (str): The unique identifier for the caregiver.
            name (str): The first name of the caregiver.
            lastname (str): The last name of the caregiver.
            username_patient (str): The username of the patient to whom the caregiver is linked.
            relationship (str): The nature of the relationship between the caregiver and the patient (e.g., parent, sibling).
            phone (str): The contact phone number of the caregiver.

        Returns:
            int: 0 if the insertion was successful, -1 if an integrity error occurred, such as duplicate entries or 
                issues with foreign key constraints.

        Exceptions:
            sqlite3.IntegrityError: Catches and handles any integrity errors that occur during the database operation. 
                                    This includes problems like violating unique constraints or foreign key violations.
        """
        try:
            self.cur.execute("""
                            INSERT INTO Caregivers
                            (username, name, lastname, username_patient, relationship, phone) 
                            VALUES (?, ?, ?, ?, ?, ?) """,
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
        """
        Checks if a patient with the given username exists in the Patients table in the database.

        Args:
            username (str): The username of the patient to be checked.

        Returns:
            int: 0 if the username is not found in the database (indicating no such patient exists), 
                -1 if the username is found (indicating the patient exists).
        """
        self.cur.execute("SELECT COUNT(*) FROM Patients WHERE username = ?", (username,))
        if self.cur.fetchone()[0] == 0: return 0
        else: return -1

    def get_creds_by_username(self, username):
        """
        Retrieves a user's credentials from the Credentials table based on their username.

        Args:
            username (str): The username of the user whose credentials are to be retrieved.

        Returns:
            Credentials: A Credentials object containing the user's credentials if found.
            None: If no credentials are found for the given username.
        """
        creds = self.cur.execute("""
                                SELECT *
                                FROM Credentials
                                WHERE username=?""", (username,)).fetchone()
        if creds is not None:
            return Credentials(*creds)
        return None

    def get_user_by_username(self, username):
        """
        Retrieves a user's detailed information based on their role from the appropriate table in the database.

        Args:
            username (str): The username of the user whose detailed information is being requested.

        Returns:
            Medics|Patients|Caregivers|None: An instance of the Medics, Patients, or Caregivers class if the user exists,
                                         otherwise, None.
        """
        role = self.get_role_by_username(username)
        if role == 'MEDIC':
            user = self.cur.execute("""
                                    SELECT *
                                    FROM Medics
                                    WHERE Medics.username = ?""", (username,)).fetchone()
            if user is not None:
                return Medics(*user)
        elif role == 'PATIENT':
            user = self.cur.execute("""
                                    SELECT *
                                    FROM Patients
                                    WHERE Patients.username = ?""", (username,)).fetchone()
            if user is not None: 
                return Patients(*user)
        elif role == 'CAREGIVER':
            user = self.cur.execute("""
                                     SELECT *
                                     FROM Caregivers
                                     WHERE Caregivers.username = ?""", (username,)).fetchone()
            if user is not None:
                return Caregivers(*user)
        return None
    
    def get_role_by_username(self, username):
        role = self.cur.execute("""
                                SELECT role
                                FROM Credentials
                                WHERE username = ?""", (username,))
        role = self.cur.fetchone()  
        if role:
            return role[0]
        else:
            pat = self.check_patient_by_username(username)
            if pat:
                 return "PATIENT"
            else:
                return None
            
    def get_public_key_by_username(self, username):
        """
        Retrieve the public key for a given username from the Credentials table.

        Args:
            username (str): The username of the user whose public key is to be retrieved.

        Returns:
            str: The public key of the user if found, None otherwise.
        """
        try:
            self.cur.execute("SELECT public_key FROM Credentials WHERE username = ?", (username,))
            result = self.cur.fetchone()
            if result:
                return result[0]  # Return the public key
            else:
                return None  # Public key not found
        except Exception as e:
            print("An error occurred while retrieving public key:", e)
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
    

    def change_passwd(self, username, old_pass, new_pass):
        creds = self.get_creds_by_username(username)
        if creds is not None:
            new_hash = self.hash_function(new_pass)
            try:
                self.cur.execute("""
                                UPDATE Credentials
                                SET hash_password = ?
                                WHERE username = ?""", (new_hash, username))
                self.conn.commit()
                return 0
            except Exception as ex:
                raise ex
        else:
            return -1
    
    def get_treatmentplan_by_username(self, username):
        treatmentplan = self.cur.execute("""
                                    SELECT *
                                    FROM TreatmentPlans
                                    WHERE username_patient =?""", (username,)).fetchone()
        return TreatmentPlans(*treatmentplan)

    def get_medic_by_username(self, username):
        medic = self.cur.execute("""
                                    SELECT *
                                    FROM Medics
                                    WHERE username =?""", (username,)).fetchone()
        return Medics(*medic)
    
    def get_reports_list_by_username(self, username):
        reportslist = self.cur.execute("""
                                    SELECT *
                                    FROM Reports
                                    WHERE username_patient =?""", (username,))       
        return [Reports(*report) for report in reportslist]
    
    def get_treatplan_list_by_username(self, username):
        treatmentplanslist = self.cur.execute("""
                                    SELECT *
                                    FROM TreatmentPlans
                                    WHERE username_patient =?""", (username,))       
        return [TreatmentPlans(*treatmentplan) for treatmentplan in treatmentplanslist]
    
    def get_patients_for_doctor(self, username):
            query = """
                SELECT Patients.username, Patients.name, Patients.lastname
                FROM Patients
                INNER JOIN DoctorPatientRelationships ON Patients.username = DoctorPatientRelationships.patient_username
                WHERE DoctorPatientRelationships.username = ?
            """
            # OPPURE
            query2 = """
                SELECT Patients.username, Patients.name, Patients.lastname
                FROM Patients
            
                WHERE Patients.medic_id = ?
            """
            self.cur.execute(query2, (username,))
            return self.cur.fetchall()
    
    def get_patients(self):
            query = """
                SELECT *
                FROM Patients
            """
            self.cur.execute(query)
            return self.cur.fetchall()

