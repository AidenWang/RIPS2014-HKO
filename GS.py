# rang stand for range , we have to input the boundaries 
# typ stand for type , which is used to record the type say,0 is continuous type, 
# 1 is interger type ,2 is even number,3 is the multiple of 3,...... 
# ndim record the number of dimension of the search space 
  
global rang,typ,ndim 
# enter the bound here 
rang=[0,7,0,7,1,24,1,50000,1,9,6,60] 
if len(rang)%2!=0: 
    print'Error!!!!!!!! the enter list should be a list with length of even number'
    #exit() 
if len(rang)<=3: 
    print'Error!! it must be 2 dimension or above'
    #exit() 
# enter the type here 
typ=[1,1,0,0,0,6] 
if len(typ)!=(len(rang)/2): 
    print'Error!!!!!!the entered number of type must be equal the number of paramter'
    #exit() 
# check if entered boundaries is of indicated type  
for i in range(0,len(typ)): 
        if (typ[i]!=0)and ((rang[2*i]%typ[i]!=0) or (rang[2*i+1]%typ[i]!=0)): 
            print'Error!!your',i+1, 'th parameter bounndary should be a multiple of ',typ[i] 
            #exit() 
ndim=len(rang)/2
  
import  multiprocessing 
from math import *
from random import *
################## 
# the function is used to generate a list of a point in search space 
# the output is a point in suitable dimension 
  
def ran_sam(): 
    p=[] 
    for i in range(0,ndim): 
        # append a suitable random value into the list 
        if typ[i]==0: 
            p.append(round(uniform(rang[i*2],rang[i*2+1]),3)) 
        if typ[i]!=0: 
            mutl=typ[i] 
            p.append(randint(rang[i*2]/mutl,rang[i*2+1]/mutl)*mutl) 
        #the following is for swirls only 
        if i==1: 
            p[1]=randint(p[0],rang[3]) 
    return p 
  
  
################## 
# the follwoing function is called random machine  
# it will generate some random numbers 
# the input is n and it generate n sample (n must be a multiple of 4!!) 
# the output is a list containing n vectors in suitable dimensions 
  
def ran_mach(n): 
    if n%4!=0: 
        print 'Error!!the input must be a multiple of 4,otherwise it cause some problems'
    x=[] 
    for i in range(0,n): 
        x.append(ran_sam()) 
    return x 
      
  
  
################## 
#the following function is called cross 
# it is used to crossover the chromosome of the vectors 
# the input is a list with 2 vectors,whose first entry is its score 
# it will exchange half of the gene 
# first half and other half elements will be cut and then be exchanged with other chromosome 
# if the dimension of vector is of odd number,(n+1)/2 regarded as first part,the 
# remaining part regarded as second part 
# the output is a list with 2 crossed vectors without scores 
  
def cross(x): 
    p=[] 
    #copy x into p 
    for i in range(0,len(x)): 
        p.append(x[i][:]) 
    #remove the scores 
    p[0].pop(0) 
    p[1].pop(0) 
    #copying first vector and second vector  
    p_1=p[0][:] 
    p_2=p[1][:] 
    # if you want to change the cutting point or crossover point, change index 
    for i in range(int(ceil(len(p[0])/2)),len(p[0])-1): 
        p[0][i]=p_2[i] 
        p[1][i]=p_1[i] 
    return p 
################## 
# the following function is mutation 
# the input is a list with 2 vectors 
# if mutation occurs, 
# one the first half parameters will be chosen and mutate,replaced by random number ,and  
# one of the latter half parameters will be chosen and mutate,replaced by random number 
# the output is the mutated vectors(2 mutated child) 
  
  
  
def mutat(q): 
    # choose 2 parameters 
    i_1=randint(0,ceil(ndim/2)-1) 
    i_2=randint(ceil(ndim/2),ndim-1) 
    p=[int(i_1),int(i_2)] 
    # mutate these 2 parameters 
    for i in p: 
        if typ[i]==0: 
            q[0][i]=round(uniform(rang[i*2],rang[i*2+1]),3) 
            q[1][i]=round(uniform(rang[i*2],rang[i*2+1]),3) 
        if typ[i]!=0: 
            mutl=typ[i] 
            q[0][i]=randint(rang[i*2]/mutl,rang[i*2+1]/mutl)*mutl 
            q[1][i]=randint(rang[i*2]/mutl,rang[i*2+1]/mutl)*mutl 
    return q 
  
################## 
# the following is the fitness functions 
# def get_score(y): 
  
  
################## 
# the input x is a list containing lots of vectors,scores is a list containing corespongding socres 
# the function is called the add_score,which add a score in front of the vector 
# the purpose of this is to make the vector become much easier for sorting 
# the output is a list containing vectors with coresponding scores in first entry 
# of the vector 
  
def add_score(x,scores): 
    for i in range(0,len(x)): 
        x[i].insert(0,scores[i]) 
    return x 
  
################## 
# the input is a list of vectors with score as a first entre in each vector 
# the function is used to record the best_score within x (the whole list containg all the vectors) 
# the return is the best vector with highest score 
   
def best_score(x): 
    p=[] 
    p=sorted(x) 
    p.reverse() 
    y=[] 
    y=p[0][:] 
    return y 
  
################## 
# the following function is genetic algorithm 
# import x is a list with a couple of date( i.e. the chromosome that we used 
# to find the optimun solution with its scores as first element) 
# say,there are 3 chromosome in 6 dimension, we import x =[[10,3,3,2,5,6,1],[12,8,8,2,9,6,1],[11,8,5,2,8,6,3]] 
# note that the each chromosome has 7 entries 
# since the first entry stands for the scores of that data, 
# others stand for the six parameters 
  
# y is probability of crossover (0-100) 
# z is the probability of mutation (0-100) 
  
# the output is a list containing all vectors with scores as first entry 
  
  
  
def GS(x,y,z, settings): 
    import get_score 
    g=sorted(x) 
    g.reverse() 
    # b is used to store best parents and offspring 
    # temp store the mutated children 
    b=[] 
    temp=[] 
    # b initially is used to store best half of population 
    for i in range(0,len(g)/2): 
        b.append(g[i]) 
    for i in range(0,len(x)/2,2): 
        p,c=[],[] 
        p=[g[i],g[i+1]] 
        # take parents carry out crossover and mutation 
        if randint(0,100)<=y: 
            c=cross(p) 
        else: 
          c.append(p[0][1:len(p[0])]) 
          c.append(p[1][1:len(p[1])]) 
        if randint(0,100)<=z: 
          c=mutat(c) 
        temp.append(c[0]) 
        temp.append(c[1]) 
    n=len(temp) 
    #scores=[0]*n 
    #for i in range(0,n): 
    #    find_score(temp[i],scores,i) 
    #  for parallel computing 
    input_list = [] 
    for temptemp in temp: 
        temp_list = [0]*2
        temp_list[0] = temptemp 
        temp_list[1] = settings 
        input_list.append(temp_list) 
    pool=multiprocessing.Pool() 
    scores=pool.map(get_score.get_score, input_list)  
    temp=add_score(temp,scores) 
    # b stores the offsprings 
    for i in range(0,n): 
        b.append(temp[i]) 
    return b 
  
################## 
def imp_GS(m, n, settings): 
     import get_score 
     #n is the number of initial vectors,it must be a multiple of 4 
     #n=60 
     x=ran_mach(n) 
     # y is the crossover probability.You may change it 
     y=80
     # z is the mutation probability.You may change it 
     z =70
     # the best vector is used to record the best vector through the whole searching 
     #process.It have a score 0.If the scores of the searched best vectors is greater 
     # than 0,the best_vector will store that 
     best_vector=[0]+[0]*(len(rang)/2) 
     #scores=[0]*n 
     #for i in range(0,n): 
     #    find_score(x[i],scores,i)  
     #  for parallel computing 
     input_list = [] 
     for temp in x: 
        temp_list = [0]*2
        temp_list[0] = temp 
        temp_list[1] = settings 
        input_list.append(temp_list) 
     pool=multiprocessing.Pool() 
     scores=pool.map(get_score.get_score,input_list) 
     x=add_score(x,scores) 
     for i in range(0,m): 
        x=GS(x,y,z, settings) 
        mark=best_score(x) 
        # the mark is used to recode the best vector appearing throught this itearations 
        if mark[0]>best_vector[0]: 
            best_vector=mark[:] 
     hi_ma=best_vector.pop(0) 
     print'the highest score attiained is: ',hi_ma 
     print'the best parameter set is: ',best_vector 
     return [best_vector, hi_ma] 
       
#m=input('please enter the number of iterations: ') 
#n=input('please enter a number of particle ( a muitiple of 4): ') 
#imp_GS(n,m) 
