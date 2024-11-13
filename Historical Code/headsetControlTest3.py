#Importing packages
import asyncio
import statistics
from itertools import count
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

from codrone_edu.drone import *

drone = Drone()

data_all = [] #collects live data
data_filtered = [] #documents executed drone commands
'''
Drone Commands:
    * 0: neutral
    * 1: push (forward)
    * -1: pull (backward)
'''

#Receives live data
def process_data(address, *args):
    print(f"Received OSC message: {address}, {args}")
    data_all.append(address)

#Consolidating live data and converting to drone command
async def run_script():
    # Pair the drone and code
    drone.pair()
    drone.takeoff()

    n = 'y'

    while n == 'y':

        print("Running script")
        print("data here", data_all)

        #Data cleaning: returns the most common element
        drone_command = statistics.mode(data_all)

        #Sends the command to the drone
        if (drone_command == "/com/neutral"):
            neutral_count = 1 #update the consecutive neutral count
            data_filtered.append(0)  # 0 being neutral
            print("Remain at neutral")
        elif (drone_command == "/com/push"):
            data_filtered.append(1)  #1 being push
            neutral_count = 0  #resetting neutral count
            print("Move forward")
            #Instigating flight
            drone.set_pitch(30)
            drone.move(1)
            drone.set_pitch(0)
            drone.move(1)
        elif (drone_command == "/com/pull"):
            data_filtered.append(-1)  #-1 being pull
            neutral_count = 0  #resetting neutral count
            print("Move backward")
            #Instigating flight
            drone.set_pitch(-30)
            drone.move(1)
            drone.set_pitch(0)
            drone.move(1)
        else:
            neutral_count = 0 #resetting neutral count
            print("Data unclear, more input required")

        data_all.clear()  #Clearing the list

        #Ending the flight
        if (neutral_count >= 3):
            drone.land()
            drone.close()
            n = 'n'

        # drone flight here
        await asyncio.sleep(1)


async def main():
    dispatcher = Dispatcher()
    dispatcher.map("/com/neutral", process_data)
    dispatcher.map("/com/push", process_data)
    dispatcher.map("/com/pull", process_data)
    dispatcher.map("/com/left", process_data)
    dispatcher.map("/com/right", process_data)
    dispatcher.map("/com/lift", process_data)

    server = AsyncIOOSCUDPServer(("127.0.0.1", 8000), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    script_task = asyncio.create_task(run_script())

    try:
        await asyncio.gather(script_task)
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
