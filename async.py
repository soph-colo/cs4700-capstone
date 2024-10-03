import asyncio
from itertools import count 
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer


data_all = []

def process_data(address, *args):
    print(f"Received OSC message: {address}, {args}")
    data_all.append(address)
    
async def run_script():
    while True:

        print("Running script")
        print("data here",data_all)

        if data_all.count("/com/neutral") > 10:
            print("now we go neutral")  # assign the prompt for the drone to go neutral

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
