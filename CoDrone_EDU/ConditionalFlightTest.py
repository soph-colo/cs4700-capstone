from codrone_edu.drone import *
drone = Drone()
drone.pair()

drone.takeoff()

n = 'y'

while n == 'y':
    command = int(input("Enter a number"))
    #Up
    if (command == 1):
        drone.set_throttle(15)
        drone.move(1)
        drone.set_throttle(0)
        drone.move(1)
    #Down
    elif command == -1:
        drone.set_throttle(-15)
        drone.move(1)
        drone.set_throttle(0)
        drone.move(1)
    #Right
    elif command == 2:
        drone.set_roll(15)
        drone.move(1)
        drone.set_roll(0)
        drone.move(1)
    #Left
    elif command == -2:
        drone.set_roll(-15)
        drone.move(1)
        drone.set_roll(0)
        drone.move(1)
    n = input('Enter y to continue, n to stop')

drone.land()

drone.close()
