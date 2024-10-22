import asyncio
from itertools import count
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

from codrone_edu.drone import *

drone = Drone()

data_all = [] #collects live data
flight_history = [] #collects executed drone commands
'''
Drone Commands:
    * 0: neutral
    * 1: push (forward)
    * -1: pull (backward)
'''


def process_data(address, *args):
    print(f"Received OSC message: {address}, {args}")
    data_all.append(address)


async def run_script():
    neutral_count = 0  # 10 or more consecutive neutrals end the program
    # pair it
    drone.pair()
    drone.takeoff()

    n = 'y'

    while n == 'y':

        print("Running script")
        print("data here", data_all)

        if len(data_all) > 1:

            data_filtered = data_all.copy() #pulls the most recent headset outputs

            #Identifies the most frequent output as the drone command
            drone_command = max(set(data_filtered), key=data_filtered.count)

            # Sends the command to the drone
            if (drone_command == "/com/neutral"):
                neutral_count += 1  # update the consecutive neutral count
                flight_history.append(0)  # 0 being neutral
                print("Remain at neutral")
            elif (drone_command == "/com/push"):
                neutral_count = 0  # resetting neutral count
                flight_history.append(1)  # 1 being push
                print("Move forward")
                # Instigating flight
                drone.set_pitch(30)
                drone.move(1)
                drone.set_pitch(0)
                drone.move(1)
            elif (drone_command == "/com/pull"):
                neutral_count = 0  # resetting neutral count
                flight_history.append(-1)  # -1 being pull
                print("Move backward")
                # Instigating flight
                drone.set_pitch(-30)
                drone.move(1)
                drone.set_pitch(0)
                drone.move(1)
            else:
                neutral_count = 0  # resetting neutral count
                print("Data unclear, more input required")

            endpoint = len(data_filtered) - 2 #sets the closing index for removing the processed data

            # deleting handled data from the live stream
            # leaves two elements so the list is not empty
            del data_all[0:endpoint]

            #Ending the flight
            if (neutral_count >= 10):
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
