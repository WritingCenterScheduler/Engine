import numpy as np

class ScheduleManager:

    def __init__(self):
        self.locations

    def add_location(loc):
        """
        Adds a location to the list of locations
        """
        self.locations.append(loc)

    def run_schedule():
        """
        The main part of the algorithm.
        """
        schedule_optimal = False

        while not schedule_optimal:

            for location in self.location:

                location.calculate_need()

            need, highest_need_location = min([location.greatest_need() for location in self.locations])

            highest_need_location.schedule_highest_need()

        # Finally...

        self.compute_schedule_optimailty()


    def compute_schedule_optimailty(self): 
        """
        Using self.locations, decide how optimal the schedule is
        """
        pass


class Location:

    def __init__(self):
        self.timeslots = None  # A numpy array
        self.schedule = None  # A 3D array 
        self.need = None  # A numpy array
        self.possible_candidates = []

    def add_possible_candidate(self, candidate):
        self.possible_candidates.append(candidate)

    def calculate_need(self):
        """
        Function based on timeslots and availibility of possible candidtates
        need (at each timeslot) = SUM(candidate availibility * scalar) - (timeslot_need_# * scalar)
        """
        pass

    def greatest_need(self):
        """
        returns the value of the timeslot with the greatest need (LOWEST NUMBER)

        Return tuple: need value, self
        """
        pass

    def schedule_highest_need(self):
        """
        Schedules a candidate at the higest need spot,
        then modifies the candidate availibility to remove the availibility at the time scheduled...
        """
        pass


class User:

    def __init__(self):
        self.name = None
        self.pid = None
        self.email = None
        self.onyen = None
        self.typecode = None


class Employee(User):

    def __init__(self):
        self.availibility = None # A numpy array
        Super(Employee, self).__init__()