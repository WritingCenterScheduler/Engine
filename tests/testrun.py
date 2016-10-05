import unittest
import numpy as np
from engine import models

from . import sampledata

class TestRun(unittest.TestCase):

    def setUp(self):
        self.sm = models.ScheduleManager()

        # Create Test Employee
        self.tc1 = "010"
        self.candidate1 = models.Employee(sampledata.e1av, typecode=self.tc1, pid=1)
        self.candidate2 = models.Employee(sampledata.e2av, typecode=self.tc1, pid=2)
        self.candidate3 = models.Employee(sampledata.e3av, typecode=self.tc1, pid=3)
        self.candidate4 = models.Employee(sampledata.e4av, typecode=self.tc1, pid=4)
        # Create Test Location
        self.location1 = models.Location()
        self.location1.timeslots = sampledata.loc1

        # Add employee to location and location to schedule manager
        self.location1.add_possible_candidate(self.candidate1)
        self.location1.add_possible_candidate(self.candidate2)
        self.location1.add_possible_candidate(self.candidate3)
        self.location1.add_possible_candidate(self.candidate4)
        self.sm.add_location(self.location1)

    def tearDown(self):
        del self.sm
        del self.candidate1
        del self.location1
        del self.tc1

    def test_make(self):
        self.assertTrue(isinstance(self.sm, models.ScheduleManager))

    def test_calculate_need(self):
        """
        Tests the population of a Location object's need array, which contains
        the weighted "need" value of each timeslot. The weighted "need" value of
        a timeslot denotes the priority that it will be given while scheduling.
        """

        # Call the calculate_need() function for a location in schedule_manager
        # This should populate the need array for the Location object
        self.location1.calculate_need()
        self.assertIsNotNone(self.location1.need)

    def test_initialize_location_schedule(self):
        """
        Tests the initialization of the dimensions of the Location object's
        schedule array.
        """

        # Call the initialize_dimensions() function for the location
        # This should initialize the dimensions of the schedule to match the
        # dimensions of the timeslot requirements
        width = len(self.sm.locations[0].timeslots[0]["requirements"])
        height = len(self.sm.locations[0].timeslots[0]["requirements"][0])
        self.sm.locations[0].initialize_dimensions(width, height, 2)

        self.assertEqual(len(self.sm.locations[0].schedule), width)
        self.assertEqual(len(self.sm.locations[0].schedule[0]), height)
        self.assertEqual(len(self.sm.locations[0].schedule[0][0]), 2)

    def test_schedule_employee(self):
        """
        Tests an Employee object's schedule_at(timeslot) function where timeslot
        is a tuple containing a timeslot's coordinates to be scheduled. Should
        remove the scheduled timeslot from the employee's availability array and
        add that timeslot to their schedule array
        """
        timeslot1 = (0,0) # A time when the employee is unavailable
        timeslot2 = (1,1) # A time when the employee is available

        pre_schedule = np.copy(self.candidate1.schedule)
        pre_availability = np.copy(self.candidate1.availability)

        # Attempt to schedule where employee is unavailable
        self.candidate1.schedule_at(timeslot1)
        self.assertNotEqual(self.candidate1.schedule[0][0], 1)

        # Attempt to schedule where employee is available
        self.candidate1.schedule_at(timeslot2)
        self.assertEqual(self.candidate1.schedule[1][1], 1)

        self.assertEqual(self.candidate1.schedule[0][0], pre_schedule[0][0])
        # Different as result of successful scheduling, employee schedule modified
        self.assertNotEqual(self.candidate1.schedule[1][1], pre_schedule[1][1])

        self.assertEqual(self.candidate1.availability[0][0], pre_availability[0][0])
        # Different as result of successful scheduling, employee availability modified
        self.assertNotEqual(self.candidate1.availability[1][1], pre_availability[1][1])

    def test_greatest_need(self):
        """
        Tests Location object's greatest_need() function for correct return type
        """
        # Call the calculate_need() function for a location in schedule_manager
        # This should populate the need array for the Location object
        self.location1.calculate_need()

        # Call the greatest_need() function, which returns integer, tuple, self
        timeslots, loc = self.location1.greatest_need()

        # Test whether locations evaluate to same object
        self.assertIs(self.location1, loc)

        # Test that timeslot is a list of tuples tuple, and not a list of flattned coordinates
        self.assertTrue(isinstance(timeslots, list))
        self.assertTrue(isinstance(timeslots[0], tuple))

    def test_schedule_greatest_need(self):
        """
        Tests that the function schedule_greatest_need() correctly assigns a User
        to the calendar and adjusts requirements accordingly.
        """

        width = len(self.sm.locations[0].timeslots[0]["requirements"])
        height = len(self.sm.locations[0].timeslots[0]["requirements"][0])
        self.sm.locations[0].initialize_dimensions(width, height, 2)

        # Call the calculate_need() function for a location in schedule_manager
        # This should populate the need array for the Location object
        self.location1.calculate_need()
        timeslots, loc = self.location1.greatest_need()
        self.location1.schedule_greatest_need()
        self.location1.schedule_greatest_need()
        for x in range(self.location1.schedule.shape[0]) :
            for y in range(self.location1.schedule.shape[1]) :
                for z in range(self.location1.schedule.shape[2]) :
                    candidate = self.location1.search_PID(self.location1.schedule[x][y][z])
                    if(candidate != None ) :
                        self.assertFalse(candidate.is_available_at((x,y)))
                        self.assertTrue(candidate.schedule[x][y] == 1)
        #print(self.location1.schedule)
        a = np.zeros((self.location1.schedule.shape[0],self.location1.schedule.shape[1]))
        b = np.zeros(a.shape)
        for x in range(a.shape[0]) :
            for y in range(a.shape[1]) :
                a[x][y] = self.location1.schedule[x][y][0]
                b[x][y] = self.location1.schedule[x][y][1]
        print("\n")
        print(a)
        print(b)

if __name__ == "__main__":
    unittest.main()
