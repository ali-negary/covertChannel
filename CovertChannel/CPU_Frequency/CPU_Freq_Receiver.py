"""
Implementation of Covert Channel using frequency of CPU
Receiver Side
This code belongs to Ali Negary.
GitLab: gitlab.com/alinegary   --  Linkedin: linkedin.com/in/alinegary
To use this method you need to monitor your cpu frequency. My code benefits from Pypsutil package.
You can find more about this package at their page: https://pypsutil.readthedocs.io/en/latest/
"""

# Required packages (some of them may not be used)
from __future__ import print_function
import time
import pypsutil
import math


# This function is designed to turn 8-bit codes into words - copyright belongs to @manmoleculo
def bit2word(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


# Just an indication before commencing the process
print("Monitoring CPU and receiving the message begins in 3 seconds...")
time.sleep(3)
message_bit = []

"""
The transmit unit is pretty easy to understand. However, here needs more explanation.
We monitor the CPU frequency 9-10 time in each 5-second interval and add the signals to frequency list.
At the end of 5 seconds, we calculate of average of the frequency list to make sure the signal is 1 or 0.
Feel free the to modify the timing and let me know if you find a better tweak.
Note: in the tested device, CPU frequency is 2800Mhz under load and 1000 when ideal. So, I chose a threshold of 2000.
"""
busy_threshold = 2000
number_of_bits = 80
for i in range(number_of_bits):
    frequency = []
    start = int(time.time())
    while int(time.time()) - start < 5:
        if pypsutil.cpu_freq().current > busy_threshold:
            frequency.append(1)
        else:
            frequency.append(0)
        time.sleep(0.5)
    signal = sum(frequency) / len(frequency)
    if signal > 0.5:
        message_bit.append(1)
    else:
        message_bit.append(0)
    print(message_bit)

print(message_bit)
message_bit = ''.join(str(x) for x in message_bit)

"""
We added { to the beginning of the message and } to the end of it.
Now, we can extract the message by its location between { and }. 
To be clear 01111011 is { and 01111101 is }
"""
start = message_bit.find('01111011')  # index of the first bit of {
end = message_bit.rfind('01111101')  # index of the first bit of }
print(message_bit)
message_bit = message_bit[start:end + 8]
print(message_bit)
message_bit = [i for i in message_bit]

print(message_bit)
message = (bit2word(message_bit))
print(message)
