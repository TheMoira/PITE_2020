# !/usr/bin/env python3.7
import random
import time
from abc import ABC, abstractmethod
import logging
import multiprocessing as mp

file = "./plane_stats.log"

class Event(ABC):
    def event_description(self):
        return "General event"

    def execute(self,plane):
        pass

class Plane:
    def __init__(self,name):
        self.checkpoint = 1
        self.plane_name = name
        self.tilt_angle = 0
        self.error = 30
        self.correction_rate = 50
    
    def __str__(self):
        self.checkpoint += 0.5
        return "{}: Plane {name} is flying with roll angle: {angle}".format(int(self.checkpoint),name=self.plane_name,angle=self.tilt_angle)

    def write_data(self):
        logging.info(str(self))

    def error_decrease(self):
        ans = input("Would you like to decrease error of correction for additional payment? (y/n) ")
        self.error -= random.randint(0,5) if ans == 'y' and (self.error > 5) else 0
        logging.info("Error is now at {error} percent".format(error = self.error))

    def control(self):
        if not self.checkpoint%5:
            logging.info(self.error_decrease())
        else:
            logging.info("Keep the course!\n")
    
    def set_correction_rate(rate):
        self.correction_rate = rate


class Turbulence(Event):
    def event_description(self):
        return "Turbulence...\n"

    def execute(self,plane):
        plane.tilt_angle = random.gauss(0,2*plane.correction_rate)
        logging.info(self.event_description())

class Correction(Event):
    def event_description(self):
        return "Correcting...\n"

    def execute(self,plane):
        faulty_correction = abs(plane.tilt_angle)*random.randint(0,plane.error)/100
        faulty_correction = faulty_correction if plane.tilt_angle > 0 else -faulty_correction
        plane.tilt_angle = 0
        plane.tilt_angle += faulty_correction 
        logging.info(self.event_description() + str(plane))

def set_data_output(to_file = False):
    if to_file:
        global file
        file_name = input("""Insert the path of a file to keep information about flight: 
        (insert # if you want to use default file)
        """)
        file = file_name if file_name != '#' else file
        open(file, 'w').close()
        logging.basicConfig(filename=file,level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)


def fly(plane, allowing_error_control):
    t = Turbulence()
    c = Correction()

    while True:
        yield time.ctime()
        t.execute(plane)
        plane.write_data()
        c.execute(plane)
        if allowing_error_control:
            plane.control()
        time.sleep(2)

def fly_plane(plane, allowing_error_control = False):
    flight = fly(plane, allowing_error_control)
    for f in flight:
        logging.info(f)


if __name__ == "__main__":
    n = int(input("Insert number of planes in your company (max. 10): "))
    n = n if n<=10 else 10
    names = [input(f"Insert the name of the plane {i+1}: ") for i in range(n)]
    planes = [Plane(name) for name in names]

    to_file = input("Would you like to write data to a file? (y/n) ")
    to_file = True if to_file == 'y' else False

    set_data_output(to_file)
    flights = []
    
    try:
        if n == 1:
            plane = planes[0]
            fly_plane(plane,True)
        else:
            for plane in planes:
                p = mp.Process(target=fly_plane, args=(plane,))
                flights.append(p)

            for flight in flights:
                flight.start()

    except KeyboardInterrupt:
        logging.info("Landing... Oh no.. CRASH!!!")
        logging.info("Oops")
        logging.info(f"Seems like {names} crashed on an unknown island...")
        logging.info("What's gonna happen next?")

