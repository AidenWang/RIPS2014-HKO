from numpy import *
from sobol_lib import *
import random as random
import get_score
import multiprocessing
 
#
#For the "parameter" of the pso() function, input a list with bounds of the 
#parameters
#
#For example for SWIRLS, if we want 50 iterations, 6 dimensions, then input:
#
#pso(50,6,[[0,7],[0,7],[1,24],[1,50000],[1,9],[6,60]])
#
#parameters are in the order of
#[[start lvl], [max lvl], [rho], [alpha], [sigma], [varflow]]
#
 
def pso(iteration, p, settings):
    dimension=6
    #the following list is the bounds of the parameters
    #in the order of [[start level], [max level], [rho], [alpha], [sigma], [varflow]]
    parameter= [[0,7],[0,7],[1,24],[1,50000],[1,9],[6,60]]
 
     
    #initialize the weighting for each component in PSO
    #w1 for inertia, w2 for personal influence, w3 for social influence
    w1=0.9
    c2=2.05
    c3=2.05
     
    #define the constriction factor
    conf=2/abs(2-(c2+c3)-sqrt((c2+c3)**2-4*(c2+c3)))
 
 
    #initialize particle positions x(0) using sobol sequence
    for m in range(0,p):
        x0=[0]*dimension
        x0=i4_sobol(dimension,m)[0]
        for i in range (0, dimension):
            x0[i]=x0[i]*(parameter[i][1]-parameter[i][0])+parameter[i][0]
         
        x0[0]= int(round(x0[0]))            #integer value start_level
        x0[1]= int(round(x0[1]))            #integer value max_level            
        #!!begin
        if x0[1]<x0[0]:                                     
            x0[1]=random.randint(x0[0],parameter[1][1])     #require max level > start_level
        #!!end
        x0[5]=int(round(x0[5]/6)*6)  #interval_for_varflow (time interval between two radar data)
        if m==0:
            x=x0
        else:
            x=vstack((x,x0))            #initialize x(0)
    #initialize particle velocities v(0) using uniform distribution
        y0=[0]*dimension
        for i in range(0,dimension):
            y0[i]=random.uniform(parameter[i][0],parameter[i][1])
        y0[0]=random.randint(parameter[0][0],parameter[0][1])       #integer value start_level
        while y0[1]<y0[0]:
            y0[1]=random.randint(parameter[1][0],parameter[1][1])   #integer max_level
        y0[5]=random.randrange(parameter[5][0],parameter[5][1],6)  #multiple of 6 for interval_for_varflow (time interval between two radar data)
        y0=(y0-x0)/2.0                              #half-diff initilization
 
        if m==0:
                v=y0
        else:
                v=vstack((v,y0))            #initialize v(0)
 
 
    #define the random 1x6 vector
    def Urandom():
        return array([random.random()]*dimension)
 
 
    #define local best score(lbscore) and global best score(gbscore)
    lb = [0]*p
    lbscore = [0]*p
    gbscore = float(0)
    gb=[0]*dimension
 
    xx = x.tolist()
    input_list = []
    for i in range(0, p):
        #initialize the local best and global best score
        xx[i][0]=int(xx[i][0])              #convert to integer for start level
        xx[i][1]=int(xx[i][1])              #convert to integer for max level
        xx[i][2]=round(xx[i][2],3)          #round to 3 decimal places for rho
        xx[i][3]=round(xx[i][3],3)          #round to 3 decimal places for alpha
        xx[i][4]=round(xx[i][4],3)          #round to 3 decmial places for sigma
        xx[i][5]=int(round(xx[i][5]/6)*6)   #multiple of 6 for interval for varflow
        temp_list = [0]*2
        temp_list[0] = xx[i][:]
        temp_list[1] = settings
        input_list.append(temp_list)
  
    #MUTLIPROCESSING to get score
    pool = multiprocessing.Pool()
    scores = pool.map(get_score.get_score, input_list)   
    #update the local and global best
    for i in range(0, p):
        if scores[i] > lbscore[i]:
            lbscore[i] = scores[i]
            lb[i] = xx[i]
        if scores[i] > gbscore:
            gbscore = scores[i]
            gb = xx[i]
 
 
    print [gb, gbscore]
 
    ## PSO algorithm
    for n in range (0, iteration):
        for i in range(0,p):
            v[i]=conf*(w1*v[i]+c2*Urandom()*(lb[i]-x[i])+c3*Urandom()*(gb-x[i]))   #equation for updating the velocity of the i-th particle
            x[i]+=v[i]          #equation for updating the position of the i-th particle
    #the ifs below deals with situations when the parameters go beyond search space
    # if any parameter of a particle goes out of bounds
    # position is set to the boundary value
    # the particle is "bounced back" such that the velocity is the negative of the previous velociity
            for j in range(0,dimension):
                  if x[i][j]<parameter[j][0]:
                      x[i][j]=parameter[j][0]
                      v[i][j]=-v[i][j]
                  if x[i][j]>parameter[j][1]:
                      x[i][j]=parameter[j][1]
                      v[i][j]=-v[i][j]
    #!!begin
    #if max level< start level
    #0.5 chance to change the start level
    #0.5 chance to change the max level
            if x[i][1]<x[i][0]:                
                if random.random()<0.5:
                    x[i][1]=random.uniform(round(x[i][0]), parameter[1][1])
                else:
                    x[i][0]=random.uniform(parameter[0][0],round(x[i][1]))
    #!!end
        xx=x.tolist()
        #multiprocessing for the iterations
        jobs = []
        gbscore = 0
        input_list = []
        for i in range(0, p):
            #initialize the local best and global best score
            xx[i][0]=int(xx[i][0])
            xx[i][1]=int(xx[i][1])
            xx[i][2]=round(xx[i][2],3)
            xx[i][3]=round(xx[i][3],3)
            xx[i][4]=round(xx[i][4],3)
            xx[i][5]=int(round(xx[i][5]/6)*6)
            temp_list = [0]*2
            temp_list[0] = xx[i][:]
            temp_list[1] = settings
            input_list.append(temp_list)
        scores = pool.map(get_score.get_score, input_list)
        #updating the local and global best score and parameters
        for i in range(0, p):
            if scores[i] > lbscore[i]:
                lbscore[i] = scores[i]
                lb[i] = xx[i]
            if scores[i] > gbscore:
                gbscore = scores[i]
                gb = xx[i]
     
        print n, gb, gbscore, '\n', '\n', '\n', '\n', '\n', '\n'
    return [gb,gbscore]
