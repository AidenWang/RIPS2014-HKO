#!C:\Python27\ScriptDump 
#Cuckoo Search Algorithm 
  #kjdhgdksdjkjasdkfjsfdlk#
#insert SWIRLS program here (input 6 parameters) that outputs a score. just a number 
  
def get_fitness(a_nest,nd,i,fitness): # need to change this for the case of more than 2 components in solutions 
    import math 
    import get_score 
    temp_nest = a_nest 
    for j in range(nd): 
        if j == 1 or j == 0: 
            temp_nest[j] = int(round(temp_nest[j])) 
        elif j == 5: 
            temp_nest[j] = int(round(temp_nest[j]/float(6))*6) 
    fitness[i] = get_score.get_score(temp_nest) 
    return fitness 
  
def replace_nests(nests,new_nests,nest_number,nd,fitness,new_fitness): 
    for i in range(nest_number): 
        if fitness[i] < new_fitness[i]: #in SWIRLS we want max but for now we say min for our fitness function 
            for j in range(nd): 
                nests[i][j] = new_nests[i][j] 
            fitness[i] = new_fitness[i] 
    return nests, fitness 
  
def get_cuckoo(nests, best_nest, Lb, Ub, nest_number,nd,stepsize): 
    import math 
    from scipy.special import gamma #gamma(decimal) not fraction 
    import random 
    alpha = 1.5 #flexible parameter but this works well. Also need to plug in decimal form 
    sigma=(gamma(1+alpha)*math.sin(math.pi*alpha/2)/(gamma((1+alpha)/2)*alpha*2**((alpha-1)/2)))**(1/alpha) #everything here and below is algorithm for levy flights 
    for i in range(nest_number): 
        temp = nests[i][:] 
        step = [0]*len(temp) 
        for j in range(len(temp)): 
            sign = 1
            a = random.gauss(0,1)*sigma 
            b = random.gauss(0,1) 
            if a < 0: 
                sign = -1
            step[j] = sign*stepsize[j]*((abs(a)/abs(b))**(1/alpha))*(temp[j]-best_nest[j]) #problem is when a<= and we take a/abs(b) ^ 1/alpha. look up mantegna's algorithm 
            temp[j] = round(temp[j]+step[j]*random.gauss(0,1),3) 
            if temp[j] <= Lb[j]: 
                temp[j] = Lb[j] 
            elif temp[j] >= Ub[j]: 
                temp[j] = Ub[j] 
            if j == 1 and temp[j] < temp[0]: 
                coin = random.randint(0,1) 
                if coin == 0: 
                    temp[0] = round(random.uniform(Lb[0],temp[j]),3) 
                else: 
                    temp[j] = round(random.uniform(temp[0],Ub[j]),3) 
        nests[i][:] = temp 
    return nests 
  
def empty_nest(nests,Lb,Ub,pa,nest_number,nd,fitness): 
    import math 
    import random #want random.randint(a,b) for a<=N<=b 
    import numpy 
    frac = int(round(pa*nest_number)) #need to change this into type int because it will be used as an index 
    #find the worst "frac" nests 
    mins = [0]*frac 
    mark = 0
    temp_fit = fitness[:] 
    for i in range(frac): 
        mins[i] = fitness.index(min(temp_fit)) #if trying to find min, get rid of max 
        temp_fit.remove(min(temp_fit)) 
    perm_nests1 = nests[:][:] 
    perm_nests2 = nests[:][:] 
    #mins is the indices of solutions in nests that we are going to replace 
    numpy.random.shuffle(perm_nests1) 
    numpy.random.shuffle(perm_nests2) 
    new_nests = nests[:][:] 
    temp_fitness = [0] 
    for l in mins: 
        temp = [0]*nd 
        for j in range(nd): 
            temp[j] = nests[l][j] + round(random.random()*(perm_nests1[l][j] - perm_nests2[l][j]),3) 
            if temp[j] <= Lb[j]: 
                temp[j] = Lb[j] 
            elif temp[j] >= Ub[j]: 
                temp[j] = Ub[j] 
            if j == 1 and temp[j] < temp[0]: 
                coin = random.randint(0,1) 
                if coin == 0: 
                    temp[0] = random.uniform(Lb[0],temp[j]) 
                else: 
                    temp[j] = random.uniform(temp[0],Ub[j]) 
        temp_fitness = get_fitness(temp,nd,0,temp_fitness) 
        if fitness[l] < temp_fitness[0]: 
            nests[l][:] = temp 
            fitness[l] = temp_fitness[0] 
    return nests, fitness 
  
def cuckoo_search(Iterations): #enter details for cuckoo search in this section 
    import random 
    nest_number = 25 #the number of held solutions 
    pa = 0.2 #the percent of nests(solutions) that are replaced per step 
    nd = 6 #dimension of solutions 
    #the middle 3 cannot be 0 
    Lb = [0,0,1,1,1,6]  #lower bound to search domain. Same dimension of solutions 
    Ub = [7,7,24,50000,9,60]  #upper bound to search domain. Same dimension of solutions 
    stepsize = [1,1,0.75,0.75,0.75,3] #new addition 7/22 
    date = 'yyyymmddhhminmin' #date input 
    nests = [[0] for i in range(nest_number)] 
    for i in range(nest_number): 
        a_nest = [0]*nd 
        for j in range(nd): 
            if j == 1: 
                a_nest[j] = round((Ub[j]-a_nest[0])*random.random() + a_nest[0],3) 
            else: 
                a_nest[j] = round(((Ub[j]-Lb[j])*random.random()) + Lb[j],3) 
        nests[i] = a_nest 
      
    fitness = [0]*nest_number     
    for k in range(nest_number): 
        fitness = get_fitness(nests[k],nd,k,fitness) 
    index = fitness.index(max(fitness)) #min since we want to minimize our fitness function 
    best_nest = nests[index][:] 
      
    N_inter = 0
    while N_inter <= Iterations: 
        new_nests = get_cuckoo(nests,best_nest,Lb,Ub, nest_number,nd,stepsize) 
        N_inter = N_inter+1
          
        new_fitness = [0]*nest_number 
        for k in range(nest_number): 
            new_fitness = get_fitness(new_nests[k],nd,k,new_fitness) 
          
        #the following 3 functions replaces the nests with the new nests, calculates the fitness of each nest 
        #and finds the best of all nests 
        data_dump = replace_nests(nests,new_nests,nest_number,nd,fitness,new_fitness) 
        nests = data_dump[0] 
        fitness = data_dump[1] 
          
        #and therefore should follow any new_nest function 
        data_dump = empty_nest(nests,Lb,Ub,pa,nest_number,nd,fitness) 
        nests = data_dump[0] 
        fitness = data_dump[1] 
          
        index = fitness.index(max(fitness)) #min since we want to minimize our fitness function 
        best_nest = nests[index][:] 
          
        percent = float(N_inter)/Iterations 
        print 'The Percent Done = ' + str(percent) 
        int(N_inter) 
        print 'The Best Solution is ' + str(best_nest) 
    return best_nest, max(fitness) 
