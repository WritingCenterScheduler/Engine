import numpy as np
import datetime

from . import config

class ScheduleManager:

    def __init__(self,
        shifts_per_day=48,
        shift_length_minutes=30,
        shift_start_time="08:00"):
        """
        :param shifts_per_day: the number of shifts in a given day.
        :param shift_length_minutes: the length of a shift in minutes.
        :param shift_start_time: A 24hour time when all shifts start.
            HH:MM (00:00 through 23:59)
        """
        self.locations = []
        self.shifts_per_day = shifts_per_day
        self.shift_length_minutes = shift_length_minutes
        self.shift_start_time = shift_start_time

    def add_location(self, loc):
        """
        Adds a location to the list of locations
        """

        # TODO: VERIFY that the location's timeslots and need align with...
        #   shifts per day, shift_length_minutes, shift_start_time

        self.locations.append(loc)

    def run_schedule(self):
        """
        The main part of the algorithm.
        """
        schedule_optimal = False

        while not schedule_optimal:

            for location in self.locations:

                location.calculate_need()

            ## Oh god fix this
            need, coords, highest_need_location = min([location.greatest_need() for location in self.locations])

            highest_need_location.schedule_highest_need()

            ## Need to determine if schedule is optimal again...

        # Finally...

        self.compute_schedule_optimailty()


    def compute_schedule_optimailty(self):
        """
        Using self.locations, decide how optimal the schedule is
        """
        pass


class Location:

    def __init__(self):
        """
        Contains the description of all the location's worker requirements.
        """
        self.timeslots = []  # A list of requirements
        # ex. [
        #     {
        #         "type": "1",          # "returners"
        #         "scalar_weight": 2,   # This type is 2x as important to schedule as 1.
        #         "requirements" : <a numpy array>
        #     },
        #     {
        #         "type": "0",
        #         "scalar_weight": 1,
        #         "requirements": <a numpy array>
        #     }
        # ]
        self.schedule = None  # A 3D array

        # A numpy array
        self.need = None
        self.possible_candidates = []

        # A list of locations that this location can swap with.
        # This means a candidate can start a shift at location a, then swap to b without any time gaps
        self.can_swap_with = []

    def add_possible_candidate(self, candidate):
        self.possible_candidates.append(candidate)

    def sort_candidates_by_total_availability(self):
        """
        Sorts the possible_candidates in place by total availability in reverse order.
        :return: None
        """
        self.possible_candidates.sort(key=lambda x: x.total_availability, reverse=True)

    def sort_candidates_by_return_status(self, candidates):
        """
        Sorts the possible candidates in place by returning status.
        :return: None
        """
        self.possible_candidates.sort(key=lambda x: x.is_returner())

    def initialize_dimensions(width, height, depth):
        self.schedule = np.zeros(width, height, depth)

    def calculate_need(self):
        """
        Function based on timeslots and availability of possible candidtates
        need (at each timeslot) = Sigma(candidate availability * scalar) - timeslot_need
        timeslot need = Sigma(timeslot.requirements * timeslot.scalar_weight)
        """

        all_candidate_availability = self.timeslots[0]["requirements"] * 0

        for c in self.possible_candidates:

            c_available = c.availability
            c_available[c_available>0] = 1
            c_available[c_available<0] = 0

            # print(c.scalar_type)
            all_candidate_availability += c_available * config.scalars[c.scalar_type]

        timeslot_need = self.timeslots[0]["requirements"] * 0

        for t in self.timeslots:

            timeslot_need += t["requirements"] * t["scalar_weight"]

        # print(all_candidate_availability)
        # print(timeslot_need)

        self.need = all_candidate_availability - timeslot_need

    def greatest_need(self):
        """
        returns the value of the timeslot with the greatest need (LOWEST NUMBER)

        Return tuple: (need value, coordinates, self)
        """

        if (self.need is None):
            raise TypeError("self.need is None, did you calculate_need()?")
        else:
            # print(self.need)
            # print("ARGMIN: " + str(np.argmin(self.need)))
            coord = np.argmin(self.need)
            need_value = self.need.flatten()[coord]
            return need_value, coord, self

    def schedule_highest_need(self):
        """
        Schedules a candidate at the higest need spot,
        then modifies the candidate availability to remove the availability at the time scheduled...
        """
        sort_candidates_by_total_availability()
        sort_candidates_by_return_status()
        # We need the coord of the timeslot with the greatest need
        need_val, coord, loc = self.greatest_need()
        # Unpack coord to separate variables
        x, y = coord
        # This is definitely still broken so don't yell at me plz
        for t in timeslots:
            if t["type"] is "1" and t["requirements"][x][y] > 0:
                for i in range(len(self.possible_candidates)):
                    if possible_candidates[i].is_returner() and possible_candidates[i].is_available_at(coord):
                        possible_candidates[i].schedule(coord)
                        break
            elif t["type"] is not "1" and t["requiremnts"][x][y] > 0:
                for i in range(len(self.possible_candidates)):
                    if possible_candidates[i].is_available_at(coord):
                        possible_candidates[i].schedule(coord)
                        break

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

    @property
    def scalar_type(self):
        return self.typecode[1]


class Employee(User):

    def __init__(self, availability, **kwargs):
        self.availability = availability # A numpy array
        super(Employee, self).__init__(**kwargs)
        self.schedule = np.zeros(self.availability.shape)
        self.total_availability = self.calculate_total_availability()

    def calculate_total_availability(self):
        """
        Updates the total availability of an employee.
        The total availability is defined as the value indicating an employee's
        overall availability to work. An employee who can work at many different
        times throughout the week will have a higher total availability than an
        employee who has limited availability throughout the week.

        :return: Integer representing total availability
        """

        # A 1-D array of employee preferences of each scalar type
        availability_frequencies = np.bincount(self.availability)
        return (availability_frequencies[2] * 2) + availability_frequencies[1]

    def is_available_at(self, timeslot):
        """
        Returns true or false depending on whether employee is available to be scheduled at a specific timeslot

        :return: Boolean
        """
        x, y = timeslot
        return self.availability[x][y] > 0

    def schedule(self, timeslot):
        """
        Tells the employee to consider itself scheduled at the timeslot.
        Should update any internal state necessary, especially it's availability

        :param timeslot: Consider itself scheduled at timeslot
        :return: none
        """
        # unpack timeslot
        x, y = timeslot
        self.schedule[x][y] = 1;
        self.total_availability -= self.availability[x][y]
        self.availability[x][y] = 0;
