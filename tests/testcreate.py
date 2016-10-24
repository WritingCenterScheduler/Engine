import unittest
from engine import models

from . import sampledata

class TestCreate(unittest.TestCase):

    def setUp(self):
        self.sm = models.ScheduleManager()

    def tearDown(self):
        del self.sm

    def test_add_locations(self):
        """
        Tests the creation of a location and adding it to the schedule manager.
        Pass conditions:
            (1) location successfully added to schedule manager
            (2) schedule manager contains the correct location object
        """

        location1 = models.Location()
        location1.timeslots = sampledata.loc1

        self.sm.add_location(location1)

        self.assertTrue(len(self.sm.locations) >= 1)
        # assertIs() to test that both arguments evaluate to same object
        self.assertIs(self.sm.locations[0], location1)

    def test_add_candidates(self):
        """
        Tests creation of employees and adding them to a location,
        which is then added to the schedule manager.
        Pass conditions:
            (1) the created employees have the correct attributes
            (2) the employee is successfully added to the location
            (3) the location is successfully added to the schedule manager,
            and contains the correct employees
        """

        tc1 = "010"
        tc2 = "000"
        candidate1 = models.Employee(sampledata.e1av, typecode=tc1, pid=1)
        candidate2 = models.Employee(sampledata.e2av, typecode=tc2, pid=2)

        self.assertEqual(candidate1.typecode, tc1)
        self.assertEqual(candidate1.pid, 1)
        self.assertEqual(candidate2.typecode, tc2)
        self.assertEqual(candidate2.pid, 2)

        location1 = models.Location()
        location1.timeslots = sampledata.loc1

        location1.add_possible_candidate(candidate1)
        location1.add_possible_candidate(candidate2)
        self.sm.add_location(location1)

        self.assertIs(self.sm.locations[0].possible_candidates[0], candidate1)
        self.assertEqual(self.sm.locations[0].possible_candidates[0].pid, 1)
        self.assertIs(self.sm.locations[0].possible_candidates[1], candidate2)
        self.assertEqual(self.sm.locations[0].possible_candidates[1].pid, 2)
        self.assertEqual(len(self.sm.locations[0].possible_candidates), 2)

    def test_add_requirements(self):
        """
        Tests the creation of a location and adding timeslot requirements in the
        form
            ex. [
                {
                    "type": "1",          # "returners"
                    "scalar_weight": 2,   # This type is 2x as important to schedule as 1.
                    "requirements" : <a numpy array>
                },
                {
                    "type": "0",
                    "scalar_weight": 1,
                    "requirements": <a numpy array>
                }
            ]
        """
        location1 = models.Location()
        location1.timeslots = sampledata.loc1
        self.sm.add_location(location1)

        self.assertEqual(self.sm.locations[0].timeslots, location1.timeslots)
        for i in range(len(sampledata.loc1[0]["requirements"])):
            for j in range(len(sampledata.loc1[0]["requirements"][0])):
                self.assertEqual(self.sm.locations[0].timeslots[0]["requirements"][i][j], sampledata.loc1[0]["requirements"][i][j])

if __name__ == "__main__":
    unittest.main()
