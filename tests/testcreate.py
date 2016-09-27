import unittest
from engine import models

from . import sampledata

class TestCreate(unittest.TestCase):

    def setUp(self):
        self.sm = self.sm = models.ScheduleManager()

    def test_add_locations(self):

        candidate1 = models.Employee(sampledata.e1av)
        candidate2 = models.Employee(sampledata.e2av)
        candidate3 = models.Employee(sampledata.e3av)
        candidate4 = models.Employee(sampledata.e4av)

        location1 = models.Location()
        location1.timeslots = sampledata.loc1

        location1.add_possible_candidate(candidate1)
        location1.add_possible_candidate(candidate2)
        location1.add_possible_candidate(candidate3)
        location1.add_possible_candidate(candidate4)

        self.sm.add_location(location1)

    def test_run_algorithm(self):
        """
        Testcase will be run
        """


if __name__ == "__main__":
    unittest.main()