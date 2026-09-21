import json
import unittest

from tools import calculator, get_passing_rules, get_student_info, get_student_marks


class ToolTests(unittest.TestCase):
    def test_student_info_tool(self):
        data = json.loads(get_student_info.invoke({"student_id": "22CS045"}))
        self.assertTrue(data["found"])
        self.assertEqual(data["name"], "Dhanushya")
        self.assertEqual(data["department"], "Computer Science")

    def test_marks_tool(self):
        data = json.loads(get_student_marks.invoke({"student_id": "22CS047"}))
        self.assertEqual(data["python"], 92)
        self.assertEqual(data["database"], 88)
        self.assertEqual(data["ai"], 95)
        self.assertEqual(data["web"], 90)

    def test_calculator_total_and_average(self):
        total = json.loads(calculator.invoke({"expression": "85+72+90+78"}))
        average = json.loads(calculator.invoke({"expression": "(85+72+90+78)/4"}))
        self.assertEqual(total["result"], 325)
        self.assertEqual(average["result"], 81.25)

    def test_calculator_rejects_code(self):
        data = json.loads(calculator.invoke({"expression": "__import__('os').system('echo bad')"}))
        self.assertIn("error", data)

    def test_passing_rules(self):
        data = json.loads(get_passing_rules.invoke({}))
        self.assertEqual(data["minimum_overall_average_percent"], 40)
        self.assertEqual(data["minimum_mark_each_subject"], 35)


if __name__ == "__main__":
    unittest.main()
