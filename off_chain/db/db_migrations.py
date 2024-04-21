import sqlite3

con = sqlite3.connect("ADIChain")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS Credentials")
cur.execute("DROP TABLE IF EXISTS Medics")
cur.execute("DROP TABLE IF EXISTS Patients")
cur.execute("DROP TABLE IF EXISTS Caregivers")
cur.execute("DROP TABLE IF EXISTS Reports")
cur.execute("DROP TABLE IF EXISTS TreatmentPlans")
cur.execute("DROP TABLE IF EXISTS AccessLog")
cur.execute('''CREATE TABLE Credentials(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            hash_password TEXT NOT NULL,
            role TEXT CHECK(role IN ('MEDIC', 'PATIENT', 'CAREGIVER')) NOT NULL,
            public_key TEXT NOT NULL,
            private_key TEXT NOT NULL
            );''')
cur.execute('''CREATE TABLE Medics(
            id_medic INTEGER NOT NULL,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            specialization TEXT NOT NULL,
            mail TEXT,
            phone TEXT,
            FOREIGN KEY(id_medic) REFERENCES Credentials(id)
            FOREIGN KEY(username) REFERENCES Credentials(username)
            );''')
cur.execute('''CREATE TABLE Patients(
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
cur.execute('''CREATE TABLE Caregivers(
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
cur.execute('''CREATE TABLE Reports(
            id_report INTEGER PRIMARY KEY AUTOINCREMENT,
            id_patient INTEGER NOT NULL,
            id_medic INTEGER NOT NULL,
            analyses TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            FOREIGN KEY(id_patient) REFERENCES Patients(id_patient),
            FOREIGN KEY(id_medic) REFERENCES Medics(id_medic)
            );''')
cur.execute('''CREATE TABLE TreatmentPlans(
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
cur.execute('''CREATE TABLE AccessLog(
            id_access INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utente INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(id_utente) REFERENCES Credentials(id)
            );''')
con.commit()
con.close()