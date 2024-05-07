import unittest
from faker import Faker
from db.db_operations import DatabaseOperations

class testADI (unittest.TestCase):
    def setUp(self):
        """Setup for test."""
        self.db_ops = DatabaseOperations()
        self.faker = Faker()

    def tearDown(self):
        """Cleaning after test."""
        self.db_ops.conn.close()

    def test_register_user(self):
        for role in ['PATIENT', 'CAREGIVER', 'MEDIC']:
            with self.subTest(role=role):
                self.register_user_helper(role)

    def register_user_helper(self, role):
        """Helper function to test user registration with different roles."""
        username = self.faker.user_name()
        password = self.faker.password()
        public_key = self.faker.pystr(min_chars=10, max_chars=10)
        private_key = self.faker.pystr(min_chars=10, max_chars=10)

        result = self.db_ops.register_creds(username, password, role, public_key, private_key)
        self.assertEqual(result, 0, f"Registration for user {username} with role {role} didn't succeed.")

    def test_insert_report(self):
        """Test function for new report"""
        username_patient = self.faker.user_name()
        username_medic = self.faker.user_name()
        analyses = "Blood Test, X-Ray"
        diagnosis = "Flu"
        result = self.db_ops.insert_report(username_patient, username_medic, analyses, diagnosis)
        self.assertEqual(result, 0, "Failed to insert medical report")

    def test_insert_treatment_plan(self):
        """Test function for new treatment plan"""
        username_patient = self.faker.user_name()
        username_medic = self.faker.user_name()
        description = "Physical Therapy sessions twice a week"
        start_date = self.faker.date_between(start_date='-1y', end_date='today')
        end_date = self.faker.date_between(start_date='today', end_date='+1y')
        result = self.db_ops.insert_treatment_plan(username_patient, username_medic, description, start_date, end_date)
        self.assertEqual(result, 0, "Failed to insert treatment plan")

if __name__ == '__main__':
    unittest.main()