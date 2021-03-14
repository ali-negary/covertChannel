"""let's do this"""
import math
import time

# step 1 - define the main method:

""""
Enter the input arguments as follows:
1. path to the files containing list of addresses.
2. block_size in byte. (default is 64 bytes)
3. cache_size in Kb. (default is 32 kilobytes)
4. cache_associativity. 1: direct mapping, 0: fully-associative, (2,4,8,16): set-associative. (default is 2-way)
5. replacement_policy. (default is LRU)
"""


def chooseCache(input_path, block_size=64, cache_size=32, cache_associativity=2, replacement_policy="lru"):
    input_file = open(input_path, 'r')
    hex_address_list = input_file.readlines()
    binary_address_list = [bin(int(hex_num, 16))[2:] for hex_num in hex_address_list]  # convert hex to binary
    # print samples for debug
    print("HEX address: ", hex_address_list[0])
    print("Binary address: ", binary_address_list[0])

    if cache_associativity == 1:
        print("\nYou have chosen Direct Mapping\n")
        number_of_blocks = int(cache_size / block_size * 1024)
        print("You have a cache of size {} kilobytes with {} blocks.".format(cache_size, number_of_blocks))
        hit, miss = direct_mapping(binary_address_list, block_size, number_of_blocks)

    elif cache_associativity > 1 & cache_associativity % 2 == 0 & cache_associativity <= 16:
        print("You have chosen Set Associative\n")
        number_of_sets = int(cache_size / (cache_associativity * block_size) * 1024)
        print("You have a {}-way cache of size {} kilobytes with {} set.".format(cache_associativity, cache_size, number_of_sets))
        hit, miss = set_associative(binary_address_list, cache_associativity, block_size, number_of_sets, replacement_policy)

    # elif cache_associativity == 0:
    #     print("You have chosen Fully Associative\n")
    #     hit, miss = fully_associative()
    else:
        miss = hit = 'NAN'
        print("Invalid Associativity.")

    print("Results for {} records in L1{} file:".format(len(binary_address_list), input_path[-1]))
    print("Cache hit = ", hit)
    print("Cache miss = ", miss)
    print("So hit rate is equal to {}".format(hit/(hit+miss)))


# step 2 - cache structures:

def direct_mapping(address_list, block_size, num_of_blocks):
    hit = miss = 'NAN'
    return hit, miss


def set_associative(address_list, ways, block_size, num_of_sets, policy):
    bo = int(math.log(block_size, 2))  # block offset
    st = int(math.log(num_of_sets, 2))  # set index
    print("For first address, tag is {} , set index is {} , and block offset is {} .".format(address_list[0][:-(bo + st)],
                                                                                             address_list[0][-(st + bo):-bo],
                                                                                             address_list[0][-bo:]))
    # next address list will be converted into a list of tuples for separation and faster process
    processed_address_list = [(address[-(st + bo):-bo], address[:-(bo + st)], address[-bo:]) for address in address_list]
    print("First address will be like: ", processed_address_list[0])
    hit_count = 0
    miss_count = 0
    if policy == "lru":
        cache = dict()
        # cache = {"index1": [["tag1", 0], ["tag2", 1], "lru_for_index1"], "index2": [["tag3", 0], ["tag4", 1], "lru_for_index1"]}
        # cache is going to look like {"index1": [["tag1", 0], ["tag2", 1], "lru_for_index1"], "index2": [["tag3", 0], ["tag4", 1], "lru_for_index1"]}
        for address in processed_address_list:
            is_index_cached = lookup(address[0], list(cache.keys()))  # is the requested index in cache or not?
            if is_index_cached:
                is_tag_cached = lookup(address[1], cache[address[0]])  # is the requested tag is that cache index or not?
                if is_tag_cached:
                    hit_count += 1
                    # now I must set the LRU_count of that tag to 1 and set the LRU_count of the other tag (if available) in the set to 0.
                else:
                    miss_count += 1
                    if len(cache[address[0]]) < ways:  # if ways is 2, len can be 0, 1, or 2.
                        cache[address[0]].append([address[1], 1])
                    else:
                        for i in range(len(cache[address[0]])):
                            if cache[address[0]][i] == 0:
                                cache[address[0]][i] = address[1]
            else:
                miss_count += 1
                if len(cache) < num_of_sets:
                    cache[address[0]] = [address[1], 0]
        print("Number of items in cache  is : ", len(cache.keys()))

    elif policy == "belady":
        print("Belady cache policy has not been implemented yet.")
        pass
    else:
        print("Requested policy will not be supported in my code")

    return hit_count, miss_count


def fully_associative(address_list, num_of_blocks, block_size, policy):
    pass


# step 3 - lookup method:
def lookup(address, list_of_indices):
    return True if address in list_of_indices else False
    # must return hit (True) or miss (False).


# begin timing the code
start_time = time.time()
path_to_instructions_file = '/home/ali/Desktop/Projects/Simple_Cache/PythonApproach/00-L1i'
chooseCache(path_to_instructions_file, block_size=64, cache_size=32, cache_associativity=4, replacement_policy="lru")
end_time = time.time()
print("Runtime for this set of traces was {} seconds".format(end_time - start_time))
