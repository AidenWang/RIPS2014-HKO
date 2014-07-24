#This program's purpose is to generate a list of 32 initial parameters by customizing the values for the six parameters.
#For initial setting, set custom = [[1, 2], [7], [9], [2000, 10000], [1.5, 2.5, 3], [6, 12, 30]]. 
#This automatically generates the following intial parameters:
"""nests = [[0 for i in range(7)] for i in range(32)]
nests[0] = [1, 7, 9, 2000, 1.5, 12, 0]
nests[1] = [1, 7, 9, 2000, 1.5, 30, 0]
nests[2] = [1, 7, 9, 2000, 2.5, 12, 0]
nests[3] = [1, 7, 9, 2000, 2.5, 30, 0]
nests[4] = [1, 7, 9, 2000, 3, 6, 0]
nests[5] = [1, 7, 9, 2000, 3, 12, 0]
nests[6] = [1, 7, 9, 2000, 3, 30, 0]
nests[7] = [1, 7, 9, 10000, 1.5, 6, 0]
nests[8] = [1, 7, 9, 10000, 1.5, 12, 0]
nests[9] = [1, 7, 9, 10000, 1.5, 30, 0]
nests[10] = [1, 7, 9, 10000, 2.5, 6, 0]
nests[11] = [1, 7, 9, 10000, 2.5, 12, 0]
nests[12] = [1, 7, 9, 10000, 2.5, 30, 0]
nests[13] = [1, 7, 9, 10000, 3, 6, 0]
nests[14] = [1, 7, 9, 10000, 3, 12, 0]
nests[15] = [1, 7, 9, 10000, 3, 30, 0]
nests[16] = [2, 7, 9, 2000, 1.5, 6, 0]
nests[17] = [2, 7, 9, 2000, 1.5, 12, 0]
nests[18] = [2, 7, 9, 2000, 1.5, 30, 0]
nests[19] = [2, 7, 9, 2000, 2.5, 30, 0]
nests[20] = [2, 7, 9, 2000, 3, 6, 0]
nests[21] = [2, 7, 9, 2000, 3, 12, 0]
nests[22] = [2, 7, 9, 2000, 3, 30, 0]
nests[23] = [2, 7, 9, 10000, 1.5, 6, 0]
nests[24] = [2, 7, 9, 10000, 1.5, 12, 0]
nests[25] = [2, 7, 9, 10000, 1.5, 30, 0]
nests[26] = [2, 7, 9, 10000, 2.5, 6, 0]
nests[27] = [2, 7, 9, 10000, 2.5, 12, 0]
nests[28] = [2, 7, 9, 10000, 2.5, 30, 0]
nests[29] = [2, 7, 9, 10000, 3, 6, 0]
nests[30] = [2, 7, 9, 10000, 3, 12, 0]
nests[31] = [2, 7, 9, 10000, 3, 30, 0]"""

#To make changes, simply replace the value that you wish to replace in CuckooSearch_forSWIRLS_multi.py

def generate(custom):

    nests = [[0 for i in range(7)] for i in range(32)]

    for i in range(32):

        if i < 16: #first parameter
            nests[i][0] = custom[0][0]
        else:
            nests[i][0] = custom[0][1]

        nests[i][1] = custom[1][0] #second parameter
        nests[i][2] = custom[2][0] #third parameter

        if i in range(7) + range(16, 23): #fourth parameter
            nests[i][3] = custom[3][0]
        else:
            nests[i][3] = custom[3][1]

        if i in [0, 1, 7, 8, 9, 16, 17, 18, 23, 24, 25]: #fifth parameter
            nests[i][4] = custom[4][0]
        elif i in [2, 3, 10, 11, 12, 19, 26, 27, 28]:
            nests[i][4] = custom[4][1]
        else:
            nests[i][4] = custom[4][2]
    
        if i in [4, 7, 10, 13, 16, 20, 23, 26, 29]: #sixth parameter
            nests[i][5] = custom[5][0]
        elif i in [0, 2, 5, 8, 11, 14, 17, 21, 24, 27, 30]:
            nests[i][5] = custom[5][1]
        else:
            nests[i][5] = custom[5][2]

    return nests



#just in case you want to make individual changes, here is a function for you to do so:


def generate_your_own():

    nests = [[0 for i in range(7)] for i in range(32)]
    nests[0] = [1, 7, 9, 2000, 1.5, 12, 0]
    nests[1] = [1, 7, 9, 2000, 1.5, 30, 0]
    nests[2] = [1, 7, 9, 2000, 2.5, 12, 0]
    nests[3] = [1, 7, 9, 2000, 2.5, 30, 0]
    nests[4] = [1, 7, 9, 2000, 3, 6, 0]
    nests[5] = [1, 7, 9, 2000, 3, 12, 0]
    nests[6] = [1, 7, 9, 2000, 3, 30, 0]
    nests[7] = [1, 7, 9, 10000, 1.5, 6, 0]
    nests[8] = [1, 7, 9, 10000, 1.5, 12, 0]
    nests[9] = [1, 7, 9, 10000, 1.5, 30, 0]
    nests[10] = [1, 7, 9, 10000, 2.5, 6, 0]
    nests[11] = [1, 7, 9, 10000, 2.5, 12, 0]
    nests[12] = [1, 7, 9, 10000, 2.5, 30, 0]
    nests[13] = [1, 7, 9, 10000, 3, 6, 0]
    nests[14] = [1, 7, 9, 10000, 3, 12, 0]
    nests[15] = [1, 7, 9, 10000, 3, 30, 0]
    nests[16] = [2, 7, 9, 2000, 1.5, 6, 0]
    nests[17] = [2, 7, 9, 2000, 1.5, 12, 0]
    nests[18] = [2, 7, 9, 2000, 1.5, 30, 0]
    nests[19] = [2, 7, 9, 2000, 2.5, 30, 0]
    nests[20] = [2, 7, 9, 2000, 3, 6, 0]
    nests[21] = [2, 7, 9, 2000, 3, 12, 0]
    nests[22] = [2, 7, 9, 2000, 3, 30, 0]
    nests[23] = [2, 7, 9, 10000, 1.5, 6, 0]
    nests[24] = [2, 7, 9, 10000, 1.5, 12, 0]
    nests[25] = [2, 7, 9, 10000, 1.5, 30, 0]
    nests[26] = [2, 7, 9, 10000, 2.5, 6, 0]
    nests[27] = [2, 7, 9, 10000, 2.5, 12, 0]
    nests[28] = [2, 7, 9, 10000, 2.5, 30, 0]
    nests[29] = [2, 7, 9, 10000, 3, 6, 0]
    nests[30] = [2, 7, 9, 10000, 3, 12, 0]
    nests[31] = [2, 7, 9, 10000, 3, 30, 0]

    return nests

