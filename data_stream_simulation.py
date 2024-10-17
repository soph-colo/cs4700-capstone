array_of_commands = ["/com/neutral", "/com/push", "/com/pull", "/com/left","/com/right", "/com/lift"]

import time
import random


# start_time = time.time()
# end_time = start_time + 60

# while time.time() < end_time:

#     print(array_of_commands[random.randint(0, len(array_of_commands)-1)])

# one that will move things forward for a couple of seconds
for i in range(0,30):
    print("/com/neutral")
    time.sleep(0.05)

for i in range(0,80):
    print("/com/push")
    time.sleep(0.05)

for i in range(0,80):
    print("/com/neutral")
    time.sleep(0.05)



