from codrone_edu.drone import *
drone = Drone()
drone.pair()

drone.takeoff()

drone.set_pitch(30)  # setting forward pitch

drone.move(1)  # moving forward!

drone.set_pitch(0)  # resetting pitch to 0

drone.set_roll(30)  # setting roll to the right

drone.move(1)  # moving right!

drone.set_roll(0)  # resetting roll to 0

drone.set_pitch(-30)  # setting backwards pitch

drone.move(1)  # moving backwards!

drone.set_pitch(0)  # resetting pitch to 0

drone.set_roll(-30)  # setting roll to the left

drone.move(1)  # moving left!

drone.land()

drone.close()