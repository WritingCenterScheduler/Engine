import unittest
from engine import models

class TestCreate(unittest.TestCase):

    def test_make(self):
        self.sm = models.ScheduleManager()
        self.assertTrue(isinstance(self.sm, models.ScheduleManager))

if __name__ == "__main__":
    unittest.main()