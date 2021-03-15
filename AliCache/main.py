"""
Build a simple cache
This code is implemented as a class assignment for Advanced Multiprocessor Architecture.
Copyright belongs to Ali Negary.
GitLab: gitlab.com/alinegary   --  Linkedin: linkedin.com/in/alinegary
"""
import math
import time

""""
Please enter the input arguments as follows:
1. path to the files containing list of addresses. (currently the program only works with the file that ends with "i")
2. block_size in byte. (default is 64 bytes)
3. cache_size in Kb. (default is 32 kilobytes)
4. cache_associativity. 1: direct mapping, 0: fully-associative, (2,4,8,16): set-associative. (default is 2-way)
5. replacement_policy. (default is LRU)
"""


# step 1 - define the main method:
def chooseCache(input_path, block_size=64, cache_size=32, cache_associativity=2, replacement_policy="lru"):
    input_file = open(input_path, 'r')
    hex_address_list = input_file.readlines()
    binary_address_list = [bin(int(hex_num, 16))[2:] for hex_num in hex_address_list]  # convert hex to binary
    # DEBUG_AREA
    # print("First trace:\nHEX = {}Binary = {}\n".format(hex_address_list[0], binary_address_list[0]))

    if cache_associativity == 1:
        print("\nYour choice is Direct Mapping\n")
        number_of_blocks = int(cache_size / block_size * 1024)
        print("Sorry. I have not worked on this part yet.")
        # print("You have a cache of size {} kilobytes with {} blocks.".format(cache_size, number_of_blocks))
        hit, miss = direct_mapping(binary_address_list, block_size, number_of_blocks)

    elif cache_associativity > 1 & cache_associativity % 2 == 0 & cache_associativity <= 16:
        print("Your choice is Set Associative\n")
        number_of_sets = int(cache_size / (cache_associativity * block_size) * 1024)
        print("You have a {}-way cache of size {} kilobytes with {} set.".format(cache_associativity, cache_size, number_of_sets))
        hit, miss = set_associative(binary_address_list, cache_associativity, block_size, number_of_sets, replacement_policy)

    elif cache_associativity == 0:
        print("Your choice is Fully Associative\n")
        print("Sorry. I have not worked on this part yet.")
        number_of_blocks = 1
        hit, miss = fully_associative(binary_address_list, number_of_blocks, block_size, replacement_policy)
    else:
        miss = hit = 'NAN'
        print("Invalid Associativity.")

    print("Results for {} records in L1{} file:".format(len(binary_address_list), input_path[-1]))
    print("Cache hit = ", hit)
    print("Cache miss = ", miss)
    print("So hit rate is equal to {}%".format(round(hit / (hit + miss) * 100, 2)))


# step 2 - cache structures:

def set_associative(address_list, ways, block_size, num_of_sets, policy):
    bo = int(math.log(block_size, 2))  # block offset
    st = int(math.log(num_of_sets, 2))  # set index
    # DEBUG_AREA
    # print("For first address, tag is {} , set index is {} , and block offset is {} .".format(address_list[0][:-(bo + st)],
    #                                                                                          address_list[0][-(st + bo):-bo],
    #                                                                                          address_list[0][-bo:]))
    # next address list will be converted into a list of tuples for separation and faster process
    processed_address_list = [(address[-(st + bo):-bo], address[:-(bo + st)], address[-bo:]) for address in address_list]
    global pre_process_time  # this parameter is temporarily defined global.
    pre_process_time = time.time()
    # DEBUG_AREA
    # print("First address will be like: ", processed_address_list[0])
    hit_count = 0
    miss_count = 0
    if policy == "lru":
        cache = dict()
        # cache is going to look like {"index1": {"tag1": lru_bit1, "tag2":lru_bit2}, "index2": {"tag1": lru_bit1, "tag2":lru_bit2}}
        for address in processed_address_list:  # address sample [set_index, tag, block_offset]
            is_index_cached = lookup(address[0], list(cache.keys()))  # is the requested index in cache or not?
            if is_index_cached:
                is_tag_cached = lookup(address[1], list(cache[address[0]].keys()))  # is the requested tag is that cache index or not?
                # DEBUG_AREA
                # print(cache[address[0]].keys())
                if is_tag_cached:
                    hit_count += 1
                    # DEBUG_AREA
                    # print("hit-hit")
                    # print(len(cache[address[0]]))
                    if cache[address[0]][address[1]] < (ways - 1):
                        cache[address[0]][address[1]] += 1
                        # here I have another job which is decreasing number of others by one.
                else:
                    miss_count += 1
                    # DEBUG_AREA
                    # print("hit-miss")
                    if len(cache[address[0]]) < ways:  # if ways is 2, len can be 1, or 2.
                        # DEBUG_AREA
                        # print("Now we have these: ", cache[address[0]])
                        # print("This is going to be added: ", [address[1], 0])
                        cache[address[0]][address[1]] = 0
                        # break
                    else:
                        # DEBUG_AREA
                        # print("An item is going to be removed now:")
                        lru_key = list(cache[address[0]].keys())[0]
                        # DEBUG_AREA
                        # print("This one: ", lru_key)
                        del cache[address[0]][lru_key]
                        # DEBUG_AREA
                        # print(cache[address[0]])
                        # break

                        # here I need to remove the least recently used.
                        # for i in range(len(cache[address[0]])):
                        #     if cache[address[0]][i] == 0:
                        #         cache[address[0]][i] = address[1]
                        # print(cache[address[0]])
            else:
                miss_count += 1
                # print("miss")
                if len(cache) < num_of_sets:
                    cache[address[0]] = {address[1]: 0}
            # DEBUG_AREA
            # print(cache)
            # time.sleep(0.25)

    elif policy == "belady":
        print("Belady cache policy has not been implemented yet.")
        pass
    else:
        print("Requested policy will not be supported in my code")

    return hit_count, miss_count


def direct_mapping(address_list, block_size, num_of_blocks):
    hit = miss = 0
    return hit, miss


def fully_associative(address_list, num_of_blocks, block_size, policy):
    hit = miss = 0
    return hit, miss


# step 3 - lookup method:
def lookup(address, list_of_indices):
    return True if address in list_of_indices else False
    # must return True (hit) or False (miss).


# begin timing the code
start_time = time.time()
path_to_instructions_file = '/home/ali/Desktop/Projects/AliCache/00-L1i'
chooseCache(path_to_instructions_file, block_size=64, cache_size=32, cache_associativity=8, replacement_policy="lru")
end_time = time.time()
print("Preprocessing the data took {} seconds".format(round(pre_process_time - start_time, 5)))
print("Runtime for this set of traces was {} seconds".format(round(end_time - pre_process_time, 5)))
