"""
Implementation of Covert Channel using frequency of CPU
Transmitter Side
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
from pip._vendor.distlib.compat import raw_input


# This function is designed to turn words into 8-bit codes - copyright belongs to @manmoleculo
def word2bit(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


# This function is designed to turn 8-bit codes into words - copyright belongs to @manmoleculo
def bit2word(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


# This function is a time-conditioned True loop that keeps the CPU busy for 5 seconds (Signalling 1s)
def makeBusy():
    start = int(time.time())
    while int(time.time()) - start < 5:   # 5 seconds is just to make sure nothing goes wrong.
        1


# This function keeps the cpu quiet for 5 seconds in each call (Signalling 0s)
def keepCalm():
    time.sleep(5)   # 5 seconds is just to make sure nothing goes wrong.


# In here you can choose how to send your message.
input_message = 'secret'
# input_message = raw_input("Enter your secret message (you can say hi) : ")
msg = "{" + input_message + '}'
print("Your message is : " + msg)
print("Your message will turn into : " + (''.join(str(x) for x in word2bit(input_message))))

# call word2bit function
msg_bit = (word2bit(msg))
print("Your message will be send in this frame ==>  " + ''.join(str(x) for x in msg_bit))
time.sleep(2)   # There is no necessary need for this stall. just to make sure.

# For each bit 'zero' we stall the cpu and for each bit 'one' we keep it almost 100% busy.
print("Transmit begin now \n")
for i in msg_bit:
    if i:
        makeBusy()
    else:
        keepCalm()
    print(i, end='')
print("\n")
