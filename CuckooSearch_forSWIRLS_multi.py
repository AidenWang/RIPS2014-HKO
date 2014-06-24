
#The function that calls other functions for cuckoo search. 
def initialize(Iterations, nest_number, settings): 
    import random 
    import math, multiprocessing 
    import os 
    import exceptions 
    import string 
    #These are all changable parameters 
    nd = 7 #dimension of solutions 
    Lb = [0,0,1,1,1,6,0]  #lower bound to search domain. Same dimension of solutions 
    Ub = [7,7,24,50000,9,60,1]  #upper bound to search domain. Same dimension of solutions 
    stepsize = [1,1,0.75,0.75,0.75,1.5,0] #new addition 7/22 
    pa = 0.2 #the percent of nests(solutions) that are replaced per step 
    nests = [[0 for i in range(7)] for i in range(32)]
    nests[0] = [1,7,9,2000,1.5,12,0]
    nests[1] = [1,7,9,2000,1.5,30,0]
    nests[2] = [1,7,9,2000,2.5,12,0]
    nests[3] = [1,7,9,2000,2.5,30,0]
    nests[4] = [1,7,9,2000,3,6,0]
    nests[5] = [1,7,9,2000,3,12,0]
    nests[6] = [1,7,9,2000,3,30,0]
    nests[7] = [1,7,9,10000,1.5,6,0]
    nests[8] = [1,7,9,10000,1.5,12,0]
    nests[9] = [1,7,9,10000,1.5,30,0]
    nests[10] = [1,7,9,10000,2.5,6,0]
    nests[11] = [1,7,9,10000,2.5,12,0]
    nests[12] = [1,7,9,10000,2.5,30,0]
    nests[13] = [1,7,9,10000,3,6,0]
    nests[14] = [1,7,9,10000,3,12,0]
    nests[15] = [1,7,9,10000,3,30,0]
    nests[16] = [2,7,9,2000,1.5,6,0]
    nests[17] = [2,7,9,2000,1.5,12,0]
    nests[18] = [2,7,9,2000,1.5,30,0]
    nests[19] = [2,7,9,2000,2.5,30,0]
    nests[20] = [2,7,9,2000,3,6,0]
    nests[21] = [2,7,9,2000,3,12,0]
    nests[22] = [2,7,9,2000,3,30,0]
    nests[23] = [2,7,9,10000,1.5,6,0]
    nests[24] = [2,7,9,10000,1.5,12,0]
    nests[25] = [2,7,9,10000,1.5,30,0]
    nests[26] = [2,7,9,10000,2.5,6,0]
    nests[27] = [2,7,9,10000,2.5,12,0]
    nests[28] = [2,7,9,10000,2.5,30,0]
    nests[29] = [2,7,9,10000,1.5,6,0]
    nests[30] = [2,7,9,10000,1.5,12,0]
    nests[31] = [2,7,9,10000,1.5,30,0]
    
    #initiates number by parameters in the sort file 
    #Initates nest_number of solutions by randomly picking points in parameter space 
    #for i in range(nest_number): 
    #    a_nest = [0]*nd 
    #   for j in range(nd): 
    #        #!!!The second parameter must be >= first parameter so the following line guarantees this. 
    #            #!!!Change or comment out if different conditions are necessary 
    #        if j == 1: 
    #                a_nest[j] = round((Ub[j]-a_nest[0])*random.random() + a_nest[0],3) 
    #            else: 
    #                #Picks random points in parameter space 
    #                a_nest[j] = round(((Ub[j]-Lb[j])*random.random()) + Lb[j],3) 
    #    nests[i] = a_nest 
    #Opens parallel processing 
    pool = multiprocessing.Pool() 
    score_nests = [0]*nest_number 
    for j in range(nest_number): 
        score_nests[j] = add_settings(nests[j],settings) 
    #sends jobs to get_fitness in parallel 
    fitness = pool.map(get_fitness,score_nests) 
    
    for i in range(fitness)
        nests[i][6] = fitness[i]
      
    return nests
