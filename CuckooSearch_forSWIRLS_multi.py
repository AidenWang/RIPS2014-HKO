#!C:\Python27\ScriptDump 
#Cuckoo Search Algorithm 
  
#Convert string to a number 
def num(s): 
    import exceptions 
    try: 
        return int(s) 
    except exceptions.ValueError: 
        return float(s) 
  
  
#input is a list of 6 parameters and outputs the fitness of the solution 
 
def get_fitness(a_nest,settings): 
    import math 
    import get_score 
    a_nest[0] = int(round(a_nest[0])) 
    a_nest[1] = int(round(a_nest[1]))
    a_nest[5] = int(round(a_nest[5]/float(6))*6) 
    #Calls SWIRLS and scoring function 
    a_nest[6] = get_score.get_score(a_nest,settings) 
    print 'fitness of'
    print a_nest
    print 'is'
    print a_nest[6]
    return a_nest[6] 
  
#input new and old solutions with new and old scores and replaces old if new has higher score 
def replace_nests(nests, new_nests): 
    from operator import itemgetter 
    nests = nests + new_nests
    sorted(nests, key = itemgetter(6), reverse = true)
    for i in range(new_nest): 
        nests.pop()
        
    return nests
    
#obtains new solutions from old via random walk sampling from a Levy Distribution (Levy Flight) 
#Levy Distribution is sampled by Mantegna's Algorithm 
def get_new_nests(nests, best_nest, Lb, Ub, nest_number, stepsize, percentage): 
    import math 
    import scipy.special 
    import random 
    #Mantegna's Algorithm 
    alpha = 1.5 #flexible parameter but this works well. Also need to plug in decimal form 
    sigma=(scipy.special.gamma(1+alpha)*math.sin(math.pi*alpha/2)/(scipy.special.gamma((1+alpha)/2)*alpha*2**((alpha-1)/2)))**(1/alpha) 
    
    random.shuffle(nests)
    frac = range(int(round(nest_number*percentage)))
    new_nests = [[0 for i in range(7)] in range(frac)]
    for i in range(frac): 
        temp = nests[i][:] 
        step = [0]*len(temp) 
        for j in range(len(temp)): 
            sign = 1
            a = random.gauss(0,1)*sigma 
            b = random.gauss(0,1) 
            if a < 0: 
                sign = -1
            step[j] = sign*stepsize[j]*((abs(a)/abs(b))**(1/alpha))*(temp[j]-best_nest[j]) 
            temp[j] = round(temp[j]+step[j]*random.gauss(0,1),3) 
            #check to see if new solution is within bounds 
            if temp[j] <= Lb[j]: 
                temp[j] = Lb[j] 
            elif temp[j] >= Ub[j]: 
                temp[j] = Ub[j] 
            #!!!we need second parameter to be larger than first. If conditions like these are necessary, change this section to 
            #!!!needed conditions. Otherwise remove or comment out.  
            if j == 1 and temp[j] < temp[0]: 
                coin = random.randint(0,1) 
                if coin == 0: 
                    temp[0] = round(random.uniform(Lb[0],temp[j]),3) 
                else: 
                    temp[j] = round(random.uniform(temp[0],Ub[j]),3) 
        new_nests[i][:] = temp 
    return new_nests 
  
#Worst Fraction of solutions take another random step 
def empty_nest(nests,Lb,Ub,pa,nest_number,nd,fitness,settings): 
    import math 
    import random 
    import numpy, multiprocessing 
    #Opens parallel processing since we need to call scoring function multiple times 
    pool = multiprocessing.Pool() 
      
    frac = int(round(pa*nest_number)) 
    #find the worst "frac" nests 
    mins = [0]*frac 
    mark = 0
    #temp_fit = fitness[:] 
    for i in range(frac): 
        mins[i] = fitness.index(min(fitness)) #if trying to find min, get rid of max 
        fitness.remove(min(fitness))
      
    
    perm_nests1 = nests[:][:] 
    perm_nests2 = nests[:][:] 
    #mins is the indices of solutions in nests that we are going to replace 
    numpy.random.shuffle(perm_nests1) 
    numpy.random.shuffle(perm_nests2) 
    temp = [0]*len(mins) 
    for k in range(len(mins)): 
        l = mins[k] 
        temp[k] = [0]*nd 
        for j in range(nd): 
            temp[k][j] = nests[l][j] + round(random.random()*(perm_nests1[l][j] - perm_nests2[l][j]),3) 
            if temp[k][j] <= Lb[j]: 
                temp[k][j] = Lb[j] 
            elif temp[k][j] >= Ub[j]: 
                temp[k][j] = Ub[j] 
            #!!!we need second parameter to be larger than first. If conditions like these are necessary, change this section to 
            #!!!needed conditions. Otherwise remove or comment out.  
            if j == 1 and temp[k][j] < temp[k][0]: 
                coin = random.randint(0,1) 
                if coin == 0: 
                    temp[k][0] = random.uniform(Lb[0],temp[k][j]) 
                else: 
                    temp[k][j] = random.uniform(temp[k][0],Ub[j]) 
    score_nests = [0]*len(temp) 
    for i in range(len(temp)): 
        score_nests[i] = add_settings(temp[i],settings) 
    #sends jobs to processors in parallel 
    temp_fitness = pool.map(get_fitness,score_nests) 
    for i in range(len(mins)): 
        if fitness[mins[i]] < temp_fitness[i]: 
            nests[mins[i]] = temp[i][:] 
            fitness[mins[i]] = temp_fitness[i] 
    return nests, fitness 
  
#The function that calls other functions for cuckoo search. 
def cuckoo_search(Iterations, nest_number, settings): 
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
    N_inter = 0
    while N_inter < Iterations: 
        replace_nests(nests, get_new_nest(nest, Lb, Ub, nest_number, stepsize))
      
      
    #    new_nests = get_cuckoo(nests,best_nest,Lb,Ub, nest_number,nd,stepsize) 
    #    N_inter = N_inter+1
  
  #      score_new_nests = [0]*nest_number 
   #     for j in range(nest_number): 
    
    #        score_new_nests[j] = add_settings(new_nests[j], settings) 
    #    new_fitness = pool.map(get_fitness,score_new_nests) 
          
    #    data_dump = replace_nests(nests,new_nests,nest_number,nd,fitness,new_fitness) 
    #    nests = data_dump[0] 
    #    fitness = data_dump[1] 
          
        #and therefore should follow any new_nest function 
    #    data_dump = empty_nest(nests,Lb,Ub,pa,nest_number,nd,fitness,settings) 
    #    nests = data_dump[0] 
    #    fitness = data_dump[1] 
    #    index = fitness.index(max(fitness)) 
    #    best_nest = nests[index][:] 
    #    best_nest_print = best_nest[:] 
        
    #    for j in range(nd): 
    #        if j == 0 or j == 1: 
    #            best_nest_print[j] = int(round(best_nest_print[j])) 
    #        elif j == 5: 
    #            best_nest_print[j] = int(round((best_nest_print[j]/6))*6) 
          
        #percent = float(N_inter)/Iterations 
        #print 'The Percent Done = ' + str(percent) 
        #int(N_inter) 
        #print 'The Best Solution is ' + str(best_nest_print) 
    #return best_nest[:] 

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
    
    for i in range(nest_number)
        nests[i][6] = fitness[i]
      
    return nests
