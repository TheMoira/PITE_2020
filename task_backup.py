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

    def error_decrease(self):
        ans = input("Would you like to decrease error of correction for additional payment? (y/n)")
        self.error -= random.randint(0,5) if ans == 'y' and (self.error > 5) else 0
        return "Error is now at {error} percent".format(error = self.error)

    def control(self):
        if not self.checkpoint%5:
            return self.error_decrease()
        else:
            return "Keep the course!\n"
    
    def set_correction_rate(rate):
        self.correction_rate = rate


class Turbulence(Event):
    def event_description(self):
        return "Turbulence...\n"

    def execute(self,plane):
        plane.tilt_angle = random.gauss(0,2*plane.correction_rate)
        return self.event_description()

class Correction(Event):
    def event_description(self):
        return "Correcting...\n"

    def execute(self,plane):
        faulty_correction = abs(plane.tilt_angle)*random.randint(0,plane.error)/100
        faulty_correction = faulty_correction if plane.tilt_angle > 0 else -faulty_correction
        plane.tilt_angle = 0
        plane.tilt_angle += faulty_correction 
        return self.event_description() + str(plane)

def set_data_output(logger,to_file = False):
    if to_file:
        global file
        file_name = input("""Insert the path of a file to keep information about flight: 
        (insert # if you want to use default file)
        """)
        file = file_name if file_name != '#' else file
        logging.basicConfig(filename=file,level=logging.DEBUG)
        # logger.setLevel(logging.INFO)
        # handler = logging.FileHandler(file)
        # handler.setLevel(logging.INFO)
        # logger.addHandler(handler)
    else:
        logging.basicConfig(level=logging.INFO)

def fly(plane):
    t = Turbulence()
    c = Correction()

    while True:
        yield time.ctime()
        yield t.execute(plane)
        yield plane
        yield c.execute(plane)
        yield plane.control()
        yield 'wait'

if __name__ == "__main__":
    name = input("Insert the name of the plane: ")

    to_file = input("Would you like to write data to a file? (y/n) ")
    to_file = True if to_file == 'y' else False

    logger = mp.get_logger()
    set_data_output(logger,to_file)

    my_plane = Plane(name)
    flight = fly(my_plane)
    
    try:
        for f in flight:
            if f == 'wait':
                time.sleep(2)
            else:
                if to_file:
                    logger.info(f)
                else:
                    logging.info(f)


    except KeyboardInterrupt:
        logger.warning("Landing... Oh no.. CRASH!!!")
        logger.warning("Oops")
        logger.warning(f"Seems like {name} crashed on an unknown island...")

