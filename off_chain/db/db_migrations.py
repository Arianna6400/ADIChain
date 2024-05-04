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
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            birthday TEXT NOT NULL,
            specialization TEXT NOT NULL,
            mail TEXT,
            phone TEXT,
            FOREIGN KEY(username) REFERENCES Credentials(username)
            );''')
cur.execute('''CREATE TABLE Patients(
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
cur.execute('''CREATE TABLE Caregivers(
            username_patient TEXT NOT NULL,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            relationship TEXT NOT NULL,
            phone TEXT,
            FOREIGN KEY(username) REFERENCES Credentials(username)
            FOREIGN KEY(username_patient) REFERENCES Patients(username)
            );''')
cur.execute('''CREATE TABLE Reports(
            id_report INTEGER PRIMARY KEY AUTOINCREMENT,
            username_patient TEXT NOT NULL,
            username_medic TEXT NOT NULL,
            analyses TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            FOREIGN KEY(username_patient) REFERENCES Patients(username),
            FOREIGN KEY(username_medic) REFERENCES Medics(username)
            );''')
cur.execute('''CREATE TABLE TreatmentPlans(
            id_treament_plan INTEGER PRIMARY KEY AUTOINCREMENT,
            username_patient TEXT NOT NULL,
            username_medic TEXT NOT NULL,
            username_caregiver TEXT,
            description TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY(username_patient) REFERENCES Patients(username),
            FOREIGN KEY(username_medic) REFERENCES Medics(username),
            FOREIGN KEY(username_caregiver) REFERENCES Caregivers(username)
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