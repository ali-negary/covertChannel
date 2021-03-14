"""
Implementation of Covert Channel using RWX modifications.
Receiver Side
This code belongs to Ali Negary.
GitLab: gitlab.com/alinegary   --  Linkedin: linkedin.com/in/alinegary
To use this method you need to monitor changes in the attributes of a file with oschmod package or os package.
"""

# Required packages (some of them may not be used)
from __future__ import print_function
import time
import math
import os
import sys
from pip._vendor.distlib.compat import raw_input
import oschmod

# Choose a directory of your choice . It is wise to choose somewhere quiet.
filename = r"/home/ali/Desktop/Projects/Covert_Channel/test.txt"


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


# Get the secret message from the user and put it between { and }
message = "{" + raw_input("Enter your secret message: ") + '}'
print("Your message is : " + message)
msg_bit = (word2bit(message))
print("Your message will turn into ==> " + (''.join(str(x) for x in msg_bit)))
time.sleep(1)

print('\nTransfer begins now...')
for i in msg_bit:
    if i:
        oschmod.set_mode(filename, 0o777)  # Hex for -rwxrwxrwx access mode
        # os.chmod(filename, 0o777)  # in case oschmod does not work
    else:
        oschmod.set_mode(filename, 0o444)  # Hex for -r--r--r-- access mode
        # os.chmod(filename, 0o444)  # in case oschmod does not work
    time.sleep(0.1)
    sys.stdout.flush()  # You did not see anything, did you?!
    print(i, end='')
print('\n')
