import numpy as np
import datetime

class ScheduleManager:

    def __init__(self, 
        shifts_per_day=48, 
        shift_length_minutes=30, 
        shift_start_time="08:00"):
        """
        :param shifts_per_day: the numebr of shifts in a given day.
        :param shift_length_minutes: the length of a shift in minutes.
        :param shift_start_time: A 24hour time when all shifts start.  
            HH:MM (00:00 through 23:59)
        """
        self.locations = []
        self.shifts_per_day = shifts_per_day
        self.shift_length_minutes = shift_length_minutes
        self.shift_start_time = shift_start_time

    def add_location(loc):
        """
        Adds a location to the list of locations
        """
        
        # TODO: VERIFY that the location's timeslots and need align with...
        #   shifts per day, shift_length_minutes, shift_start_time

        self.locations.append(loc)

    def run_schedule():
        """
        The main part of the algorithm.
        """
        schedule_optimal = False

        while not schedule_optimal:

            for location in self.locations:

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
        self.timeslots = {}  # A Dictionary
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

    def __init__(self, 
        name="User",
        pid=0,
        email="unknown",
        onyen="unknown",
        typecode="000"):
    
        self.name = name
        self.pid = pid
        self.email = email
        self.onyen = onyen
        self.typecode = typecode # An N digit number.
            # (0/1)XXXX... determines not admin/admin
            # X(0/1)XXX... determines new/returning
            # XX(0/1)XX... determines something else...?

    @property
    def is_admin(self):
        return self.typecode[0] == "1"

    @property 
    def is_returner(self):
        return self.typecode[1] == "1"


class Employee(User):

    def __init__(self, availibility):
        self.availibility = availibility # A numpy array
        Super(Employee, self).__init__()