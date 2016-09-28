import unittest
from engine import models

from . import sampledata

class TestCreate(unittest.TestCase):

    def setUp(self):
        self.sm = self.sm = models.ScheduleManager()

    def test_add_locations(self):

        tc1 = "010"

        candidate1 = models.Employee(sampledata.e1av, typecode=tc1)
        candidate2 = models.Employee(sampledata.e2av, typecode=tc1)
        candidate3 = models.Employee(sampledata.e3av, typecode=tc1)
        candidate4 = models.Employee(sampledata.e4av, typecode=tc1)

        self.assertTrue(candidate1.typecode == tc1)

        location1 = models.Location()
        location1.timeslots = sampledata.loc1

        location1.add_possible_candidate(candidate1)
        location1.add_possible_candidate(candidate2)
        location1.add_possible_candidate(candidate3)
        location1.add_possible_candidate(candidate4)

        self.sm.add_location(location1)

        self.assertTrue(len(self.sm.locations) >= 1)

        for l in self.sm.locations:
            l.calculate_need()
            # print(l.need)
            print( l.greatest_need() )
            # print(l.need)


if __name__ == "__main__":
    unittest.main()