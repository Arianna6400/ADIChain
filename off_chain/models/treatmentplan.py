import datetime
from models.model_base import Model

class TreatmentPlans(Model):
    """
    This class represents the TreatmentPlans model, storing detailed information about patients' treatment plans,
    extending the functionality provided by the Model class.
    """

    def __init__(self, id_treatment_plan, date, username_patient, username_medic, description, start_date, end_date):
        """
        Initializes a new instance of the TreatmentPlans class with the provided details about the treatment plan.

        Parameters:
        - id_treatment_plan: Unique identifier for the treatment plan
        - date: Date the treatment plan was created
        - username_patient: Username of the patient for whom the treatment plan is designed
        - username_medic: Username of the medic who designed the treatment plan
        - description: Detailed description of the treatment plan
        - start_date: Start date of the treatment plan
        - end_date: End date of the treatment plan
        """
        super().__init__()
        self.id_treatment_plan = id_treatment_plan
        self.date = date
        self.username_patient = username_patient
        self.username_medic = username_medic
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    # Getter methods for each attribute
    def get_id_treatment_plan(self):
        return self.id_treatment_plan
    
    def get_date(self):
        return self.date
    
    def get_username_patient(self):
        return self.username_patient
    
    def get_username_medic(self):
        return self.username_medic
    
    def get_description(self):
        return self.description
    
    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date
    
    def save(self):
        """
        Saves a new or updates an existing Treatment Plan record in the database.
        Implements SQL queries to insert or update details based on the presence of an id_treatment_plan.
        """
        today_date = datetime.date.today()

        if self.id_treatment_plan is None:
            # Insert new treatment plan record
            self.cur.execute('''INSERT INTO TreatmentPlans (date, username_patient, username_medic, description, start_date, end_date)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (today_date, self.username_patient, self.username_medic, self.description, self.start_date, self.end_date))
        else:
            # Update existing treatment plan details
            self.cur.execute('''UPDATE TreatmentPlans SET date=? username_patient=?, username_medic=?, description=?, start_date=?, end_date=? WHERE id_treatment_plan=?''',
                             (self.date, self.username_patient, self.username_medic, self.description, self.start_date, self.end_date, self.id_treatment_plan))
        self.conn.commit()
        self.id_treatment_plan = self.cur.lastrowid # Update the id_treatment_plan with the last inserted row ID if new record

    def delete(self):
        """
        Deletes a Treatment Plan record from the database based on its id_treatment_plan.
        """
        if self.id_treatment_plan is not None:
            self.cur.execute('DELETE FROM TreatmentPlans WHERE id_treatment_plan=?', (self.id_treatment_plan,))
            self.conn.commit()
