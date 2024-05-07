import datetime
from models.model_base import Model

class Reports(Model):
    """
    This class represents the Reports model, which stores medical reports,
    extending the functionality provided by the Model class.
    """
    def __init__(self, id_report, date, username_patient, username_medic, analyses, diagnosis):
        """
        Initializes a new instance of the Reports class with details about the medical report.

        Parameters:
        - id_report: Unique identifier for the report
        - date: Date the report was created or filed
        - username_patient: Username of the patient the report is about
        - username_medic: Username of the medic who created the report
        - analyses: Details of any analyses conducted
        - diagnosis: Diagnosis information from the medic
        """
        super().__init__()
        self.id_report = id_report
        self.date = date
        self.username_patient = username_patient
        self.username_medic = username_medic
        self.analyses = analyses
        self.diagnosis = diagnosis

    # Getter methods for each attribute
    def get_id_report(self):
        return self.id_report
    
    def get_date(self):
        return self.date
    
    def get_username_patient(self):
        return self.username_patient
    
    def get_username_medic(self):
        return self.username_medic
    
    def get_analyses(self):
        return self.analyses
    
    def get_diagnosis(self):
        return self.diagnosis
    
    def save(self):
        """
        Saves a new or updates an existing Report record in the database.
        Implements SQL queries to insert or update details based on the presence of an id_report.
        """
        today_date = datetime.date.today()
        if self.id_report is None:
            # Insert new report record, using today's date by default
            self.cur.execute('''INSERT INTO Reports (date, username_patient, username_medic, analyses, diagnosis)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (today_date, self.username_patient, self.username_medic, self.analyses, self.diagnosis))
        else:
            # Update existing report details
            self.cur.execute('''UPDATE Reports SET date=?, username_patient=?, username_medic=?, analyses=?, diagnosis=? WHERE id_report=?''',
                             (self.date, self.username_patient, self.username_medic, self.analyses, self.diagnosis, self.id_report))
        self.conn.commit()
        self.id_report = self.cur.lastrowid # Update the id_report with the last inserted row ID if new record

    def delete(self):
        """
        Deletes a Report record from the database based on its id_report.
        """
        if self.id_report is not None:
            self.cur.execute('DELETE FROM Reports WHERE id_report=?', (self.id_report,))
            self.conn.commit()
