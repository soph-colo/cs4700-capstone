import asyncio
from itertools import count
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

from codrone_edu.drone import *

drone = Drone()

data_all = [] #collects live data
data_filtered = [] #collects executed drone commands
'''
Drone Commands:
    * 0: neutral
    * 1: push (forward)
    * -1: pull (backward)
'''
neutral_count = 0 #3 or more consecutive neutrals end the program


def process_data(address, *args):
    print(f"Received OSC message: {address}, {args}")
    data_all.append(address)


async def run_script():
    # pair it
    drone.pair()
    drone.takeoff()
    #raising the height
    #drone.set_throttle(15)
    #drone.move(1)
    #drone.set_throttle(0)
    #drone.move(1)

    n = 'y'

    while n == 'y':

        print("Running script")
        print("data here", data_all)

        if len(data_all) > 15:
            if (data_all.count("/com/neutral") > 10):
                data_filtered.append(0)  # 0 being neutral
                neutral_count = 1
                print("Remain at neutral")
            elif (data_all.count("/com/push") > 10):
                data_filtered.append(1)  # 1 being push
                neutral_count = 0  # resetting neutral count
                print("Move forward")
                # instigating flight
                drone.set_pitch(30)
                drone.move(1)
                drone.set_pitch(0)
                drone.move(1)
            elif (data_all.count("/com/pull") > 10):
                data_filtered.append(-1)  # -1 being pull
                neutral_count = 0  # resetting neutral count
                print("Move backward")
                # instigating flight
                drone.set_pitch(-30)
                drone.move(1)
                drone.set_pitch(0)
                drone.move(1)
            else:
                print("Data unclear, waiting for more input")

            del data_all[0:5]  # deleting handled data from the live stream

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
