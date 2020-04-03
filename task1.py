# !/usr/bin/env python3.7
import random
import time

class Plane:
    error = 30

    def __init__(self,name):
        self.plane_name = name
        self.tilt_angle = 0
        self.correction_rate = 50
    
    def data(self, count = 'After correction'):
        print(f"{count}: Plane {self.plane_name} is flying with roll angle: {self.tilt_angle}")

    def correct(self):
        print("Correcting...")
        faulty_correction = abs(self.tilt_angle)*random.randint(0,Plane.error)/100
        faulty_correction = faulty_correction if self.tilt_angle > 0 else -faulty_correction
        self.tilt_angle = 0
        self.tilt_angle += faulty_correction 
        self.data()

    def error_decrease():
        ans = input("Would you like to decrease error of correction for additional payment? (y/n)")
        Plane.error -= random.randint(0,5) if ans == 'y' and (Plane.error > 5) else 0
        print(f"Error is now at {Plane.error} percent")

    def flight(self):
        self.tilt_angle = random.gauss(0,2*self.correction_rate)

    def set_correction_rate(corr):
        self.correction_rate = corr if corr < 350 else self.correction_rate

if __name__ == "__main__":
    n = int(input("Insert number of planes in your company (max. 10): "))
    n = n if n<=10 else 10
    names = [input(f"Insert the name of the plane {i+1}: ") for i in range(n)]

    planes = [Plane(name) for name in names]

    checkouts_count = 0

    print("The planes are setting off...")
    print("..."*10)
    print("Click ESC to land")

    try:
        while True:
            checkouts_count += 1
            print()
            print(time.ctime())
            
            for plane in planes:
                print()
                print(f"***{plane.plane_name}***")
                plane.flight()
                plane.data(checkouts_count)
                plane.correct()
                time.sleep(1)

            if not checkouts_count%5:
                print()
                Plane.error_decrease()
                print()

            time.sleep(5)
    except KeyboardInterrupt:
        print("Landing... Oh no.. CRASH!!!")
        print("Oops")
        print(f"Seems like {names} crashed on an unknown island...")
        print("What's gonna happen next?")
