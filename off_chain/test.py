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

if __name__ == '__main__':
    unittest.main()