"""
Implementation of Covert Channel using RWX modifications.
Receiver Side
This code belongs to Ali Negary.
GitLab: gitlab.com/alinegary   --  Linkedin: linkedin.com/in/alinegary
To use this method you need to monitor changes in the attributes of a file.
"""

# Required packages
import time
import os

# Choose a directory of your choice . It must match the directory that you have set in transmitter.
filename = r"/home/ali/Desktop/Projects/Covert_Channel/test.txt"


# This function is designed to turn 8-bit codes into words - copyright belongs to @manmoleculo
def bit2word(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


"""
In this method, status of chosen file is constantly under monitoring within tenth-of-second intervals.
output of os.stat(chosen_file) is a list of attributes, where st_mode is access control mode in decimal:
(st_mode=33279, st_ino=674819, st_dev=2053, st_nlink=1, st_uid=1000, st_gid=1000, st_size=16, etc)
Message is received by monitoring the alteration from read-only to full-access mode and vice versa.
"""

print('Monitoring commenced...')
bin_char = ''  # In this method we store the incoming message in string format.
number_of_bits = 1000   # depending on the number of characters in the message, this number can change.
for i in range(number_of_bits):
    info = os.stat(filename)
    if info.st_mode == 33279:  # 33279 is decimal value of 100777 which is octal for -rwxrwxrwx access mode.
        bin_char = str(bin_char) + str(1)
    elif info.st_mode == 33060:  # 33060 is decimal value of 100444 which is octal for -r--r--r-- access mode.
        bin_char = str(bin_char) + str(0)
    if bin_char.rfind('01111101') != -1:   # this is the end signal of the message.
        break
    # print(info)
    time.sleep(0.1)

start = bin_char.find('01111011')  # index of the first bit of {
end = bin_char.rfind('01111101')  # index of the first bit of }
bin_char = bin_char[start:end + 8]
message = (bit2word(bin_char))
print("\nDelivered message is:")
print(message)
