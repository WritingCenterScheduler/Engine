import unittest
from engine import models

class TestRun(unittest.TestCase):

    def test_make(self):
        self.sm = models.ScheduleManager()
        self.assertTrue(isinstance(self.sm, models.ScheduleManager))

    def test_add_locations_from_file(self):
        pass

if __name__ == "__main__":
    unittest.main()