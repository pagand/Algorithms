#!/usr/bin/python3
# This code is written by Pedram Agand (pagand@sfu.ca)
import numpy as np

def max_subarray(in_list, LEN):
    # Base case
    if (LEN == 1):
        if (np.asarray(in_list)>0):
            return in_list*np.ones(4)
        else:
            return np.array([0, 0, 0, np.asarray(in_list)])

    mid = int(LEN/2)
    DB1 = max_subarray(in_list[0:mid], mid)
    DB2 = max_subarray(in_list[mid:], LEN-mid)
    DB = np.zeros(4)
    DB[0] = np.amax([DB1[0], DB1[3]+DB2[0]])
    DB[1] = np.amax([DB1[1], DB2[1]])
    DB[2] = np.amax([DB2[2], DB1[2] + DB2[3]])
    DB[3] = DB1[3] + DB2[3]
    return DB

def main():
    in_list = [float(x) for x in raw_input("Enter numbers (separated by space):").split()]
    LEN = len(in_list)
    MaxSumArray = max_subarray(in_list, LEN)
    print("max sub array is:", np.max(MaxSumArray))

if __name__=='__main__':
    main()
