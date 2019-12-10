from time import time
import random

# Building a class for the elevator
class Elevator():
    def __init__(self, capacity=20, current_floor=0, next_floor=1):
        self.capacity = capacity  # max capacity
        self.load = 0  # current load
        self.current_floor = current_floor
        self.next_floor = next_floor
        self.requests = [] # unique
        self.destinations = []  # unique
        self.passengers = []
        self.wait_times = []
        self.steps = 0
        self.direction = True  # true for up, false for down


    # termination definition
    def done(self):
        """end the ride when all request and destination floors are reached"""
        if len(self.requests) == 0 and len(self.destinations) == 0:
            # print("All the passengers have successfully been dropped at their destinations after " + str(self.steps) + " steps." )
            # print("The average time spent in dropping each rider is " + str(self.return_wait_time_avg()) + " seconds in computer time.")
            return True
        # else continue
        else:
            return False


    def filled(self):
        """check whether the number of passengers has reached the elevator capacity"""
        if self.load == self.capacity:
            return True
        else:
            return False


    def add_request(self, floor):
        """Add requests to elevator. Only accept unique requests"""
        if floor not in self.requests:
            self.requests.append(floor)


    def load_passengers(self, passengers):
        """Take passengers in until the elevator is full, and update requests list accordingly"""
        added = 0
        for person in passengers:
            if self.filled():
                break

            # Add new destination only if it is not already in the list
            if person.destination not in self.destinations:
                self.destinations.append(person.destination)
            self.passengers.append(person)
            self.load += 1
            added += 1
        # remove a floor from the requrests list if the elevator has reached it
        if self.current_floor in self.requests:
            # if all passengers on the floor enter elevator, remove floor
            if added == len(passengers):
                self.requests.remove(self.current_floor)
            # if not all enter (which means elevator is full), add a new request for the same floor to the end of list
            else:
                self.requests.append(self.requests.pop(0))
        # if added != 0:
        #     print("Picking up " + str(added) + " people. Now there are " + str(self.load) + " people in the elevator.")
        return added


    def unload_passengers(self):
        """Unload passengers when they reach their destination"""

        # Remove current floor from destination only if it is in destination
        if self.current_floor in self.destinations:
            self.destinations.remove(self.current_floor)
        dropped = 0
        for person in self.passengers:
            if person.destination == self.current_floor:
                # Calculate wait time for this one person, add to the memory of the elevator. This is a metric
                self.wait_times.append(person.calc_wait_time())
                dropped += 1
        # Remove passengers that got off on this floor
        self.passengers = list(filter(lambda a: a.destination != self.current_floor, self.passengers))
        self.load = self.load - (self.load - len(self.passengers))  # Update the load
        # if dropped != 0:
        #     print("Currently at floor " + str(self.current_floor)+ ". Dropping off " + str(dropped) + " people." )


    # Three strategies for the elevator
    # All strategies are based in terms of choosing the next floor to go to

    def next_floor_sequential(self):
        """Strategy 1: Take care of the destinations first before going to the requests"""
        if len(self.destinations) != 0:
            self.next_floor = self.destinations[0]
        elif len(self.requests) != 0:
            self.next_floor = self.requests[0]


    def next_floor_simple(self, building):
        """# Strategy 2: Going all the way up and down"""
        if self.current_floor == 1:
            self.direction = True
        elif self.current_floor == len(building.floors):
            self.direction = False

        if self.direction:
            self.next_floor = self.current_floor + 1
        else:
            self.next_floor = self.current_floor - 1


    def elevator_algorithm(self, building):
        """Strategy 3: Going up only when someone in the elevator wants to go up or there is a request on upper floors, then switch directions"""
        if not self.filled():
            # If going up, change direction when no one in the elevator wants to go up and there is no request up
            if self.direction:
                if (all([x < self.current_floor for x in self.requests]) and all([y < self.current_floor for y in self.destinations])):
                    self.direction = False
            # If going down, change direction when no one in the elevator wants to go down and there is no request down
            else:
                if (all([x > self.current_floor for x in self.requests]) and all([y > self.current_floor for y in self.destinations])):
                    self.direction = True

        # If elevator goes up to the top floor and is full, switch direction
        # If elevator goes down to the bottom floor and is full, switch direction
        elif (self.current_floor == len(building.floors) and self.direction) or (self.current_floor == 1 and not self.direction):
            self.direction = not self.direction

        if self.direction:
            self.next_floor = self.current_floor + 1
        else:
            self.next_floor = self.current_floor - 1


    # Efficiency measurement 1: counting number of step
    def move_to_next_floor(self, building):
        """Go to the next floor one by one, dropping off and picking up passengers as needed"""
        num_steps = abs(self.next_floor - self.current_floor)
        self.steps = self.steps + num_steps
        for _ in range(num_steps):
            if self.current_floor < self.next_floor:
                self.current_floor += 1
            else:
                self.current_floor -= 1
            self.unload_passengers()
            added = self.load_passengers(building.get_passengers(self.current_floor))
            building.update_passengers(self.current_floor, added)  # Update number of people in the floor of the building

    # Efficiency measurement 2: average wait time of the passengers
    def return_wait_time_avg(self):
        return sum(self.wait_times)/len(self.wait_times)


class Building():
    def __init__(self, elevator, floors=10):
        self.floors = [[] for x in range(floors)]
        self.elevator = elevator


    def get_passengers(self, floor):
        return self.floors[floor - 1]


    def add_passenger(self, passenger):
        """Add a single passenger and add request"""
        self.floors[passenger.current_floor - 1].append(passenger)
        self.elevator.add_request(passenger.current_floor)


    def update_passengers(self, floor, gone):
        """Take away people from the floor"""
        current_passengers = self.floors[floor - 1]
        if len(current_passengers) > gone:
            current_passengers = current_passengers[gone - 1 : len(current_passengers)]
        else:
            current_passengers = []
        self.floors[floor - 1] = current_passengers


class Passenger():
    def __init__(self, current_floor, destination):
        self.current_floor = current_floor
        self.destination = destination
        self.wait_start = time()
        self.time_waited = 0


    def calc_wait_time(self):
        "Calculate time waited. Used in conjunction with Elevator.unload_passenger()"
        self.time_waited = time() - self.wait_start
        return self.time_waited

def test_run():
    # Set up objects
    elevator = Elevator(capacity=30)
    building = Building(floors=10, elevator=elevator)

    # Distribute passengers in the building
    for i in range(5):
        current_floor = random.randint(1, 10)
        destination = random.randint(1, 10)
        while destination == current_floor:
            destination = random.randint(1, 10)
        passenger = Passenger(current_floor, destination)
        building.add_passenger(passenger)

    # Each while loop is a different strategy. Uncomment only one while loop to use

    # while elevator.done() == False:
    #     elevator.move_to_next_floor(building)
    #     elevator.next_floor_sequential()

    # while elevator.done() == False:
    #     elevator.move_to_next_floor(building)
    #     elevator.next_floor_simple(building)

    while elevator.done() == False:
        elevator.move_to_next_floor(building)
        elevator.elevator_algorithm(building)

test_run()

import math
import matplotlib.pyplot as plt

# Functions to simulate a strategy multiple times

def run_simulation1(number_of_floors, number_of_people, trials):
    trial_steps, trial_waittimes = [], []
    for i in range(0, trials):
        # Setting up objects
        elevator = Elevator(capacity=30)
        building = Building(floors=number_of_floors, elevator=elevator)

        # Distribute passengers in the building
        for j in range(number_of_people):
            current_floor = random.randint(1, number_of_floors)
            destination = random.randint(1, number_of_floors)
            while destination == current_floor:
                destination = random.randint(1, number_of_floors)
            passenger = Passenger(current_floor, destination)
            building.add_passenger(passenger)

        # Run the first strategy
        while elevator.done() == False:
            elevator.move_to_next_floor(building)
            elevator.next_floor_sequential()

        # Store the measures for the metric
        trial_steps.append(elevator.steps)
        trial_waittimes.append(elevator.return_wait_time_avg())
        # print('here',trial_steps,trial_waittimes)

    # Return the average result of all the trials for two metrics
    return sum(trial_steps)/len(trial_steps), sum(trial_waittimes)/len(trial_waittimes)


def run_simulation2(number_of_floors, number_of_people, trials):
    trial_steps, trial_waittimes = [], []
    for i in range(0, trials):
        # Setting up objects
        elevator = Elevator(capacity=30)
        building = Building(floors=number_of_floors, elevator=elevator)

        # Distribute passengers in the building
        for i in range(number_of_people):
            current_floor = random.randint(1, number_of_floors)
            destination = random.randint(1, number_of_floors)
            while destination == current_floor:
                destination = random.randint(1, number_of_floors)
            passenger = Passenger(current_floor, destination)
            building.add_passenger(passenger)

        while elevator.done() == False:
            elevator.move_to_next_floor(building)
            elevator.next_floor_simple(building)

        trial_steps.append(elevator.steps)
        trial_waittimes.append(elevator.return_wait_time_avg())
        # print('here',trial_steps,trial_waittimes)

    return sum(trial_steps)/len(trial_steps), sum(trial_waittimes)/len(trial_waittimes)


def run_simulation3(number_of_floors, number_of_people, trials):
    trial_steps, trial_waittimes = [], []
    for i in range(0, trials):
        # Setting up objects
        elevator = Elevator(capacity=30)
        building = Building(floors=number_of_floors, elevator=elevator)

        # Distribute passengers in the building
        for i in range(number_of_people):
            current_floor = random.randint(1, number_of_floors)
            destination = random.randint(1, number_of_floors)
            while destination == current_floor:
                destination = random.randint(1, number_of_floors)
            passenger = Passenger(current_floor, destination)
            building.add_passenger(passenger)

        while elevator.done() == False:
            elevator.move_to_next_floor(building)
            elevator.elevator_algorithm(building)

        trial_steps.append(elevator.steps)
        trial_waittimes.append(elevator.return_wait_time_avg())
        # print('here',trial_steps,trial_waittimes)

    return sum(trial_steps)/len(trial_steps), sum(trial_waittimes)/len(trial_waittimes)


def plot_strategy_people(strategy1, strategy2, strategy3, trials, floors, n):
    '''
    Plotting steps for strategies with increasing number of people
    '''
    #storing data for plotting
    steps1, steps2, steps3=[], [], []
    number_of_people = []
    for i in range(1, n):
        steps1.append(strategy1(floors,i,trials)[0])
        steps2.append(strategy2(floors,i,trials)[0])
        steps3.append(strategy3(floors,i,trials)[0])
        number_of_people.append(i)

    # plotting
    plt.ylabel("Average of elevator steps until everyone delivered")
    plt.xlabel("Number of people using the elevator")
    plt.title("Average # of steps for different number of passengers.")
    plt.plot(number_of_people, steps1)
    plt.plot(number_of_people, steps2)
    plt.plot(number_of_people, steps3)
    plt.legend(["Strategy 1","Strategy 2","Strategy 3"])
    plt.savefig("average_steps_people.png",dpi=300)

# plot_strategy_people(run_simulation1, run_simulation2, run_simulation3, 20, 50, 100)


def plot_strategy_wait(strategy1, strategy2, strategy3, trials, floors, n):
    '''
    Plotting average wait-time for strategies with increasing number of people
    '''
    # storing data for plotting
    steps1, steps2, steps3=[], [], []
    number_of_people = []
    for i in range(1, n):
        steps1.append(strategy1(floors,i,trials)[1])
        steps2.append(strategy2(floors,i,trials)[1])
        steps3.append(strategy3(floors,i,trials)[1])
        number_of_people.append(i)

    # plotting
    plt.ylabel("Average wait-time until everyone delivered (steps)")
    plt.xlabel("Number of people using the elevator")
    plt.title("Average wait-time for different number of passengers.")
    plt.plot(number_of_people, steps1)
    plt.plot(number_of_people, steps2)
    plt.plot(number_of_people, steps3)
    plt.legend(["Strategy 1","Strategy 2","Strategy 3"])
    plt.savefig("average_wait_time_people.png",dpi=300)

# plot_strategy_wait(run_simulation1, run_simulation2, run_simulation3, 20, 50, 100)


def plot_strategy_wait_floor(strategy1, strategy2, strategy3, trials, floors, n):
    '''
    Plotting average wait-time for increasing number of floors, people count kept at 50
    '''
    # storing data for plotting
    steps1, steps2, steps3=[], [], []
    number_of_people = []
    for i in range(2, floors):
        steps1.append(strategy1(i,n,trials)[1])
        steps2.append(strategy2(i,n,trials)[1])
        steps3.append(strategy3(i,n,trials)[1])
        number_of_people.append(i)

    # plotting
    plt.ylabel("Average wait-time until everyone delivered (steps)")
    plt.xlabel("# of floors in the building")
    plt.title("Average wait-time for different building sizes for 50 passengers")
    plt.plot(number_of_people, steps1)
    plt.plot(number_of_people, steps2)
    plt.plot(number_of_people, steps3)
    plt.legend(["Strategy 1","Strategy 2","Strategy 3"])
    plt.savefig("average_wait_time_floors.png",dpi=300)

# plot_strategy_wait_floor(run_simulation1, run_simulation2, run_simulation3, 20, 50, 50)


def plot_strategy_people_floor(strategy1, strategy2, strategy3, trials, floors, n):
    '''
    Plotting average wait-time for increasing number of floors, n kept at 50
    '''
    # storing data for plotting
    steps1, steps2, steps3=[], [], []
    number_of_people = []
    for i in range(2, floors):
        steps1.append(strategy1(i,n,trials)[0])
        steps2.append(strategy2(i,n,trials)[0])
        steps3.append(strategy3(i,n,trials)[0])
        number_of_people.append(i)

    # plotting
    plt.ylabel("# of steps until everyone delivered")
    plt.xlabel("Number of floors in the building")
    plt.title("Average # of elevator steps for different building sizes for 50 passengers")
    plt.plot(number_of_people, steps1)
    plt.plot(number_of_people, steps2)
    plt.plot(number_of_people, steps3)
    plt.legend(["Strategy 1","Strategy 2","Strategy 3"])
    plt.savefig("average_steps_floors.png",dpi=300)

# plot_strategy_people_floor(run_simulation1, run_simulation2, run_simulation3, 20, 50, 50)
