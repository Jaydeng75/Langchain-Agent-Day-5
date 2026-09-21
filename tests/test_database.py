import unittest

from database import get_student, initialize_database


class DatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialize_database()

    def test_student_22cs045(self):
        student = get_student("22cs045")
        self.assertIsNotNone(student)
        self.assertEqual(student["name"], "Dhanushya")
        self.assertEqual(student["department"], "Computer Science")
        self.assertEqual(student["python"], 85)
        self.assertEqual(student["database"], 72)
        self.assertEqual(student["ai"], 90)
        self.assertEqual(student["web"], 78)

    def test_unknown_student(self):
        self.assertIsNone(get_student("99XX999"))


if __name__ == "__main__":
    unittest.main()
