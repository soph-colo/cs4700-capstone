
# imports
import asyncio
from itertools import count
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from codrone_edu.drone import *


# initialize drone object
drone = Drone()

# global variables to store live data and record the history of the flight
data_all = [] #collects live data
flight_history = [] #collects executed drone commands


'''
Drone Commands:
    * 0: neutral
    * 1: push (forward)
    * -1: pull (backward)
    * 2: right
    * -2: left
'''

# the function that takes the data from headset and adds it to our live data array
def process_data(address, *args):
    print(f"Received OSC message: {address}, {args}")
    data_all.append(address)

# async method that handles the flight of the drone while also still receiving data
async def fly_drone():

    # variables
    neutral_count = 0  # 10 or more consecutive neutrals end the program
    n = True

    # using drone object, pair and have drone take off
    drone.pair()
    drone.takeoff()

    # while loop to keep drone flying until 10 or more consecutive neutrals end the program
    while n:

        # TODO: remove these eventually
        print("Running script")
        print("data here", data_all)

        # only filter the data if the length of our raw data is greater than one
        if len(data_all) > 1:

            # pull the most recent headset output and filter
            data_filtered = data_all.copy() 

            # identifies the most frequent output as the drone command
            drone_command = max(set(data_filtered), key=data_filtered.count)

            # sends the command to the drone
            match drone_command:
                case "/com/neutral":
                    # update consecutive neutral count
                    neutral_count += 1  
                    flight_history.append(0)  # 0 being neutral
                    print("Remain at neutral")  # TODO: remove these prints eventually
                
                case "/com/push":
                    neutral_count = 0  # resetting neutral count
                    flight_history.append(1)  # 1 being push
                    print("Move forward")

                    # moving the drone forward one unit (30 pitch per second)
                    drone.set_pitch(30)
                    drone.move(1)
                    drone.set_pitch(0)
                    drone.move(1)
                
                case "/com/pull":
                    neutral_count = 0  # resetting neutral count
                    flight_history.append(-1)  # -1 being pull
                    print("Move backward")

                    # moving the drone backward one unit (30 pitch per second)
                    drone.set_pitch(-30)
                    drone.move(1)
                    drone.set_pitch(0)
                    drone.move(1)
                
                case "/com/left":
                    neutral_count = 0 # resetting neutral count
                    flight_history.append(-2) # -2 being left

                    # moving drone left one unit (30 pitch per second)
                    drone.set_roll(-30)
                    drone.move(1)
                    drone.set_roll(0)
                    drone.move(1)
                
                case "/com/right":
                    neutral_count = 0 # resetting neutral count
                    flight_history.append(2) # 2 being right

                    # moving drone right one unit (30 pitch per second)
                    drone.set_roll(30)
                    drone.move(1)
                    drone.set_roll(0)
                    drone.move(1)
                    
                case "/com/lift":
                    neutral_count = 0 # resetting neutral count
                    flight_history.append() # 

                    # moving drone up one unit (30 pitch per second)
                    drone.set_throttle(30)
                    drone.move(1)
                    drone.set_roll(0)
                    drone.move(1)

                case "/com/drop":
                    neutral_count = 0 # resetting neutral count
                    flight_history.append() # 

                    # moving drone down one unit (30 pitch per second)
                    drone.set_roll(-30)
                    drone.move(1)
                    drone.set_roll(0)
                    drone.move(1)

                case _:
                    neutral_count = 0  # resetting neutral count
                    print("Data unclear, more input required")

            # sets the closing index for removing the processed data
            endpoint = len(data_filtered) - 2 

            # deleting handled data from the live stream (leaves two elements so the list is not empty)
            del data_all[0:endpoint]

            # end the flight
            if (neutral_count >= 10):
                drone.land()
                drone.close()
                n = False

        # pause execution of while loop for one second so more data can be collected
        await asyncio.sleep(1)


# main method that initializes the communication between the headset and computer
async def main():

    # dispatcher object to handle OSC communication
    dispatcher = Dispatcher()
    dispatcher.map("/com/neutral", process_data)
    dispatcher.map("/com/push", process_data)
    dispatcher.map("/com/pull", process_data)
    dispatcher.map("/com/left", process_data)
    dispatcher.map("/com/right", process_data)
    dispatcher.map("/com/lift", process_data)

    # server initialization with parameters to received OSC to this device
    server = AsyncIOOSCUDPServer(("127.0.0.1", 8000), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    # create task that needs completed asynchronously
    script_task = asyncio.create_task(fly_drone())

    # try to perform this action until it is exited
    try:
        await asyncio.gather(script_task)
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
