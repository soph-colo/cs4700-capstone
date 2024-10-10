# imports
import asyncio
from itertools import count 
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from codrone_edu.drone import *
drone = Drone()

# storage of all data
data_all = []


# processing all of the data
def process_data(address, *args):
    print(f"Received OSC message: {address}, {args}")
    data_all.append(address)


# running the async script
async def run_script():

    # pair it 
    drone.pair()

    # could potentially play around with takeoff
    drone.takeoff()

    n = 'y'
    while n == 'y':

        print("Running script")
        print("data here",data_all)

        if len(data_all) > 15:

            # checks from the last fiften if there is a common occurance
            if(data_all[:-15].count("/com/push") > 10):
                print("pushing")
                drone.set_throttle(15)
                drone.move(1)
                drone.set_throttle(0)
                drone.move(1)
            elif(data_all[:-15].count("/com/pull") >10):
                print("pulling")
                drone.set_throttle(15)
                drone.move(1)
                drone.set_throttle(0)
                drone.move(1) 
            elif(data_all[:-15].count("/com/left") > 10):
                print("lefting")
                drone.set_throttle(15)
                drone.move(1)
                drone.set_throttle(0)
                drone.move(1)
            elif(data_all[:-15].count("/com/right") > 10):
                print("righting")
                drone.set_throttle(15)
                drone.move(1)
                drone.set_throttle(0)
                drone.move(1)
            elif(data_all[:-15].count("/com/neutral") > 10):
                print("staying")
            else:
                print("too confused, must land")
                drone.land()
                drone.close()
                
            
                 
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
