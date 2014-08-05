###########################################################################
                              
                                  #Cowbird.py
                     #Optimization code for 2014 HKO Team
                      #Cowbird code and related functions

############################################################################
 




#Vector that keeps track of how long each cowbird search run takes
#The last two entries indicate the start and end time of the most recent run
timingcowbird = []
date = 0
############################################################################
############################################################################ 

#Function that finds the fitness of one set of parameters
def get_fitness(a_nest, settings, gaugetime): 
    import get_score
    import math 

    #Restrictions on the parameters
    a_nest[0] = int(round(a_nest[0])) 
    a_nest[1] = int(round(a_nest[1]))
    a_nest[2] = int(round(a_nest[2]))
    a_nest[5] = int(round(a_nest[5]/float(6))*6) 
    
    #Scores the set of parameters
    a_nest[6] = get_score.get_score(a_nest,settings,gaugetime) 

    #Returns a scored set of parameters
    return a_nest[6]

############################################################################
############################################################################ 

#Determines whether the year specified by the settings is a leap year
def leapyr(n):
    if n % 400 == 0:
        return True
    if n % 100 == 0:
        return False
    if n % 4 == 0:
        return True
    else:
        return False

############################################################################
############################################################################ 

#Convert string to an integer value 
def num(s): 
    import exceptions 
    try: 
        return int(s) 
    except exceptions.ValueError: 
        return float(s) 
  
############################################################################
############################################################################ 

#Function that adds tuning run time to the date
def change_settings(settings, timingcowbird):
    import main, get_data
    import time, math
    
    #Split the date into years (yy), months (mm), hours (hh), and 
    #minutes (nn)
    timestr = str(settings[0])
    yy = int(timestr[0:4])
    mm = int(timestr[4:6])
    dd = int(timestr[6:8])
    hh = int(timestr[8:10])
    nn = int(timestr[10:12])
    tmpm = mm
    tmpd = dd
    tmph = hh
    
    #If main.runs is 0, the current run directly follows initialization
    if (main.runs == 1):

         #Timingcowbird[-1] is the ending time of the initialization
         #Timingcowbird[-2] is the beginning time of  initialization
         #This adds the initialization time to the current time
         #NOTE: Timing is changed from seconds to minutes
         nn = nn + (timingcowbird[-1] - timingcowbird[-2])/60

         #Begin timing the first tuning run
         timingcowbird.append(time.time())
         
    #The current run is not directly following initialization
    else:
         #End timing the previous tuning run
         timingcowbird.append(time.time())
         
         #Add time from last tuning run to "nn", the minutes value of 
         #the date
         nn = nn + (timingcowbird[-1]-timingcowbird[-2])/60

    #Round "nn" up to the nearest minute
    nn = int(float(nn))+1
    

    #There is the possibility that nn>60
    #Turn "nn" into the corresponding number of hours and minutes
    if nn > 60:
         diff = nn%60
         hours = (nn-diff)/60
         nn = diff
         
         hh = hh + hours
    
    #Shift one hour if at 60 min
    if nn == 60:
         nn = 0
         hh = hh + 1
         

    #Create a temporary holder for the hour value
    hhold = hh

    #If more than a day has gone by, find what hour you would be at for the  
    #next day
    if hh>23:
         hh = hh-24


    
    #Shift months and years based on how many days are in each month and  
    #whether it is a leap year  
    if hhold >23  and hhold != tmph:
        if (mm < 8 and mm%2 == 1 and dd == 31) or (mm>=8 and mm%2 == 0 and
           dd == 31) or (mm == 2 and leapyr(yy) and dd == 29) or (mm == 2
           and (not leapyr(yy)) and dd == 28) or ():
           dd = 1

        elif dd == 30:
             dd = 1
        else:
             dd = dd + 1

    if dd == 1 and dd != tmpd:
        if mm == 12:
            mm = 1
        else:
            mm = mm + 1

    if mm == 1 and mm != tmpm:
        yy = yy + 1

    yystr = str(yy)

    if mm < 10:
        mmstr = '0' + str(mm)
    else:
        mmstr = str(mm)

    if dd < 10:
        ddstr = '0' + str(dd)
    else:
        ddstr = str(dd)

    if hh < 10:
        hhstr = '0' + str(hh)
    else:
        hhstr = str(hh)

    if nn < 10:
        nnstr = '0' + str(nn)
    else:
        nnstr = str(nn)
    
    settings[0] = yystr + mmstr + ddstr + hhstr + nnstr
    
    #Return new date
    return settings[0]

############################################################################
############################################################################

def rollover(settings, nmin):
    import main, get_data
    import time, math
    
    #Split the date into years (yy), months (mm), hours (hh), and 
    #minutes (nn)
    timestr = str(settings[0])
    yy = int(timestr[0:4])
    mm = int(timestr[4:6])
    dd = int(timestr[6:8])
    hh = int(timestr[8:10])
    tmpm = mm
    tmpd = dd
    tmph = hh

   
    
    #Shift one hour if at 60 min
    if nmin == 60:
      
         nmin = 0
         hh = hh + 1
         

    #Create a temporary holder for the hour value
    hhold = hh

    #If more than a day has gone by, find what hour you would be at for the  
    #next day
    if hh>23:
         hh = hh-24

 
    
    #Shift months and years based on how many days are in each month and  
    #whether it is a leap year  
    if hhold >23  and hh != tmph:
        if (mm < 8 and mm%2 == 1 and dd == 31) or (mm>=8 and mm%2 == 0 and
           dd == 31) or (mm == 2 and leapyr(yy) and dd == 29) or (mm == 2
           and (not leapyr(yy)) and dd == 28) or ():
           dd = 1

        elif dd == 30:
             dd = 1
        else:
             dd = dd + 1

    if dd == 1 and dd != tmpd:
        if mm == 12:
            mm = 1
        else:
            mm = mm + 1

    if mm == 1 and mm != tmpm:
        yy = yy + 1

    yystr = str(yy)

    if mm < 10:
        mmstr = '0' + str(mm)
    else:
        mmstr = str(mm)

    if dd < 10:
        ddstr = '0' + str(dd)
    else:
        ddstr = str(dd)

    if hh < 10:
        hhstr = '0' + str(hh)
    else:
        hhstr = str(hh)

    if nmin < 10:
        nnstr = '0' + str(nmin)
    else:
        nnstr = str(nmin)
    
    settings[0] = yystr + mmstr + ddstr + hhstr + nnstr
    
    #Return new date
    return settings[0]

############################################################################
############################################################################

#Score new nests and compare to those of the current 32 sets of parameters
#Determine which nests to keep and make new list of 32 sets
def replace_nests(nests, new_nests, settings, gaugetime):
    import numpy, time
    from operator import itemgetter  

    print 'Producing new scores for ' + str(settings[0]) + ':' + '\n'

    #Begin timing how long it takes to score new nests
    start_time = time.time()

    print 'Old nests: \n'

    #Print out the 32 sets of parameters and their scores
    for i in range(len(nests)):
    	nests[i][6]=get_fitness(nests[i], settings, gaugetime)

        #Print out when certain percentages of nests have been scored
	if i*100/(len(nests))/10 < (i+1)*100/(len(nests))/10:
	    print str(i*100/(len(nests)))+ '% done'

    print '\n' + '='*17 + ' FITNESS OF NEW NESTS ' + '='*17 + '\n'

    #Get the scores of the new nests
    for i in range(len(new_nests)):
        new_nests[i][6]=get_fitness(new_nests[i], settings, gaugetime)

        #Maintain a parameter property
        new_nests[i][2] = int(round(new_nests[i][2]))

	#Print out the new nests and their scores
	print 'The fitness of', new_nests[i][:6], 'is', new_nests[i][6]

    #Combine the 32 old nests with the new nests
    nests = nests + new_nests

    #Sort all nests
    nests.sort(key=lambda x: x[6], reverse = True)
    
    #Remove the nests with the worst scores - there should again be 32 nests
    for i in range(len(new_nests)): 
	nests.pop()

    #Print out the list of new nests
    print '\n' + '='*20 + ' UPDATED NESTS ' + '='*20 + '\n'
    for i in range(len(nests)):
        print ' '*(3-len(str(i+1))), str(i+1) , '   ' , str(nests[i])


    #Finish timing and print how long it took to score the parameter sets
    end_time = time.time()
    print '\n'+'Time spent: ' + str(end_time - start_time) + ' seconds' + \
          '\n'

    #Return list of new nests
    return nests
   
############################################################################
############################################################################

#Peform Levy Flights on a percentage (pa) of the nests 
#NOTE: Levy Distribution is sampled by Mantegna's Algorithm
def get_new_nests(nests, Lb, Ub, nest_number, stepsize, percentage): 
    import math, scipy.special, random
    from operator import itemgetter 

    #Initialize parameters
    #Alpha is a flexible parameter but chosen to be 1.5
    alpha = 1.5
    #Sigma derived from Mantegna's Algorithm
    sigma = (scipy.special.gamma(1+alpha)*math.sin(math.pi*alpha/2)/(scipy.special.gamma((1+alpha)/2)*alpha*2**((alpha-1)/2)))**(1/alpha) 

    #Sort nests in descending order of scores
    nests.sort(key=lambda x: x[6], reverse = True)

    #Find the highest scored nest
    best_nest = nests[0]

    #Find the fraction of nests to perform Levy Flights on
    frac = int(round(nest_number*percentage))

    #Shuffle a bottom percentage of the nests
    random.shuffle(nests[int((nest_number-frac)*0.5):])
    
    #Set up a "frac" number of nests
    new_nests = [[0 for i in range(7)] for j in range(frac)]

    #Perform Levy Flights
    for i in range(frac): 
        #Temp saves the bottom fraction of nests
        #NOTE: Since a percentage of the worst nests were shuffled, temp 
        #doesn't necessarily contain the absolute worst nests
        temp = nests[nest_number-i-1][:] 

        #Step is the amount that a parameter is perturbed
        step = [0]*len(temp) 

        #Determine whether the step will be positive or negative
        for j in range(len(temp)): 
            sign = 1
            a = random.gauss(0,1)*sigma 
            b = random.gauss(0,1) 
            if a < 0: 
                sign = -1
            
            #Find step value
            step[j] = sign*stepsize[j]*((abs(a)/abs(b))**(1/alpha))*(temp[j]-best_nest[j]) 

            #Apply step to the parameter
            temp[j] = round(temp[j]+step[j]*random.gauss(0,1),3) 

            #Check to see if new solution is within bounds 
            if temp[j] <= Lb[j]: 
                temp[j] = Lb[j] 
            elif temp[j] >= Ub[j]: 
                temp[j] = Ub[j] 

            #Randomly alter the parameters
            if j == 1 and temp[j] < temp[0]: 
                coin = random.randint(0,1) 
                if coin == 0: 
                    temp[0] = round(random.uniform(Lb[0],temp[j]),3) 
                else: 
                    temp[j] = round(random.uniform(temp[0],Ub[j]),3) 

        #Save the modified nest to the new nest list
        new_nests[i][:] = temp 

    #Return the list of new nests
    return new_nests 

############################################################################
############################################################################ 

#Linear extrapolation method of last 2 raingauge values
def linear(x0, y0, x1, y1, x):
   value = y0 + (y1 - y0)*(x-x0)/(x1-x0)
   if (value < 0):
       return 0
   else:
       return value

############################################################################
############################################################################ 

#Alternative method to linear extrapolation
def weighted(xpts, gauges, x):
   if (gauges[-5:-1] == 0):
       return 0
   elif (sum(gauges[-5:-1])/5 > 5):
       if gauges[-1]> 1.5*gauges[-2]:
           return gauges[-2] + (gauges[-1] - gauges[-2])*(x-xpts[-2])/(xpts[-1]-xpts[-2])
       else: 
           return sum(gauges[-5:-1])/5
   else: 
       return (sum(gauges)/len(gauges))

############################################################################
############################################################################ 

#This function is called by main to perform each tuning run
def cowbird_search(nests, Iterations, nest_number, settings, timing0,  
    timing1): 

    import moving_max, get_data, main
    import random, math, os, exceptions, string, decimal, time
    from copy import deepcopy
    
    #Initialize Parameters
    #Set up a raingauge value vector
    real = [0]*5
    #Percentage of nests to replace with Levy Flighted nests
    pa = 0.2
    #Dimension of solutions (6 parameters and 1 fitness value)
    nd = 7
    #Lower bound to solution search domain 
    Lb = [0,0,1,1,1,6,0]  
    #Upper bound to solution search domain
    Ub = [7,7,24,50000,9,60,1]
    #A proportionality vector that will help decide how much each parameter
    #is perturbed
    stepsize = [1,1,0.75,0.75,0.75,1.5,0]  

    #If the initialization run just happened, keep track of how long it took
    #Timing0 is beginning time of initialization, timing1 is ending time of 
    #initialization
    #NOTE: timing0 and timing1 initialized in main.py
    if (main.runs == 0):
        timingcowbird.append(timing0)
        timingcowbird.append(timing1)

    #Keep track of what tuning run is occuring
    main.runs = main.runs + 1

    

  

    #Update what time it is
    change_settings(settings, timingcowbird)
    print '\n'*3 
   
    
    #Set timestr to the date and round that date down
    #If this rounds down nn to a multiple of 6, then the program will tune 
    #without waiting 5-6 more min
    timestr = str(settings[0])
    timestr = int(float(timestr))
    timestr = str(timestr)

    #Grab the minutes part of the date
    nn = timestr[-2:]
   
    
   

    #Turn the minutes value into an integer
    nn = int(nn)

    #Gaugetime is the closest raingauge measurement to the next potential 
    #tuning time
    gaugetime = deepcopy(settings[0])
    gaugetime = int(float(gaugetime))   
    gaugetime = str(gaugetime) 

    #Get the actual data if the raingauge and radar data sync up
    #No extrapolation necessary
    if nn == 00 or nn == 30:
         real = get_data.get_actual(timestr, settings[1])

    #Extrapolation of the raingauge data to the next potential tuning time 
    #is necessary
    else:    
         
         temp = list(str(settings[0]))

         #The last raingauge value measured
         closest = nn - nn % 5
         
       

         #When the next multiple of 6 is the next tuning time
         if nn>6 and (nn%6 != 0):
               next = nn + 6-(nn % 6)
               if next == 60:
                   
                   #The minutes are at 60 min again - must adjust the date
                   rollover(settings, next)  

                   newtime = str(settings[0])
                   newtime= int(float(newtime))
                   newtime = str(newtime)

                   #Grab the minutes part of the date
                   next = newtime[-2:]
                   next = int(next)
                   

         #If the minutes value is less than 6, then 6 is the next available 
         #tuning time
         elif nn <=6:
               
               next = 6

         #The current minutes value is the "next" available tuning time
         else:
               
               next = nn

     

         #The closest raingauge value to the next available tuning time is 
         #the next available raingauge time, not the previous raingauge
         #time
         if (next - closest>5):
               closest = closest + 5 

         #If "closest" is a single digit, you will shorten the updated 
         #gaugetime - Must add a "0" digit before "closest"
         if closest<10:
               gaugetime = gaugetime.replace(' ', '')[:-2].upper()   
               gaugetime = gaugetime + "0" + str(closest)  
         else:
               gaugetime = gaugetime.replace(' ', '')[:-2].upper()  
               gaugetime = gaugetime + str(closest)

         settings[0] = int(float(settings[0]))
         settings[0] = str(settings[0])

         #If "next" is a single digit, you will shorten the date
         #Must add a "0" digit before "next"
         if next<10:
               settings[0] = settings[0].replace(' ', '')[:-2].upper()   
               settings[0] = settings[0] + "0" + str(next)  
         else:
               settings[0] = settings[0].replace(' ', '')[:-2].upper()  
               settings[0] = settings[0] + str(next)

      
         

         #Find last 6 hours of raingauge data
         gauges = get_data.get_actual(gaugetime, main.base_dir)

    

         #Begin timing the next Cowbird tuning run
         timingcowbird.append(time.time())

        
   
         #Make temporary raingauge list
         lenx = 5
         tempy = list(gauges)
         pastgauges = [0]*lenx

         #Extrapvalue is the estimated raingauge value for time "next"
	 #Must make this a list to concatenate to templist
         extrapvalue = [0]*1
  
         #Get x-points vector for extrapolation
	 xpts = range(closest-5*(lenx-1), closest+1, 5)


	 #Pop off 10 most recent rainguage values from temporary list
         for i in range(lenx):
              pastgauges[lenx-i-1] = tempy.pop()
 
        
	 #Pop off oldest raingauge value to replace with an extrapolated 
         #value
         gauges.pop(0)

         #Linear extrapolation of the raingauge value at time "closest" to 
         #the time "next"
         extrapvalue[0] = linear(xpts[-1], pastgauges[-1], xpts[-2],
         pastgauges[-2], next)

         #Add the extrapolated value to the gauges list
         gauges = gauges + extrapvalue
         real = gauges

    print 'Actual maxes for ' + str(settings[0]) + ': ' 
    print real, '\n'

    nests_copy = nests


    #Only perform Levy flights if the rainfall amount is great enough
    if sum(real)/len(real) > -1:
        
        nests = replace_nests(nests, get_new_nests(nests, Lb, Ub,
                nest_number, stepsize, pa), settings, gaugetime)
        nests_copy = nests
        total = 0

        for i in range(len(nests)):
            total = total + nests[i][6]
            avg = total/len(nests)
      



    #If not enough rainfall, don't change the parameters
    else:
        nests = nests_copy
        print "No tuning involved! Reusing the old nests: \n"
        for i in range(nest_number):
            nests[i][6] = 0.0
        print '\n'

        #Print out nests
        print '\n' + '='*17 + ' UNCHANGED NESTS ' + '='*17 + '\n'
        for i in range(nest_number):
            print ' '*(3-len(str(i+1))), str(i+1) , '   ' , str(nests[i])

        print '\n'
        
    #Return the nests after the tuning run
    return nests
        
      
############################################################################     
############################################################################

#Initializes the original 32 parameters and scores them 
def initialize(Iterations, nest_number, settings): 
    import generate, get_data
    import time, random, math, os, exceptions, string
    from copy import deepcopy

    #Initialize parameters
    #Dimension of each parameter set
    nd = 7 
    #Lower bound to solution search domain 
    Lb = [0,0,1,1,1,6,0]  
    #Upper bound to solution search domain
    Ub = [7,7,24,50000,9,60,1]
    #A proportionality vector that will help decide how much each parameter 
    #is perturbed
    stepsize = [1,1,0.75,0.75,0.75,1.5,0] 
    #Percentage of nests to replace each tuning run
    pa = 0.2 


    #Uses generate.py to make 32 initial sets of parameters
    nests = generate.generate_your_own()

    #Assume that the initialization time is either on the hour or half-hour
    #Gaugetime is automatically the next available tuning time
    gaugetime = deepcopy(settings[0])
    gaugetime = int(float(gaugetime))   
    gaugetime = str(gaugetime) 

    #Generate actual raingauge list 
    actual = get_data.get_actual(settings[0], settings[1])

    print '\n'*3

    #Print the raingauge data for the last 6 hours
    print 'Actual maxes for ' + str(settings[0]) + ': ' 
    print actual, '\n'

    print '\n'*3 + '='*20 + ' INITIALIZING ' + '='*20 + '\n'

    #Begin timing initialization scoring
    start_time = time.time()
    
    #Score the nests
    for i in range(nest_number):
        nests[i][6] = get_fitness(nests[i],settings, gaugetime)
	if i*100/(nest_number)/10 < (i+1)*100/(len(nests))/10:
	    print str(i*100/(len(nests)))+ '% done'

    #Sort the nests based on their scores
    nests.sort(key=lambda x: x[6], reverse = True)

    for i in range(nest_number):
	print 'The fitness of', nests[i][:6], 'is', nests[i][6]
    
    #End timing initialization scoring
    end_time = time.time()

    print '\n'+'Time spent for initialization: ' + str(end_time - \
          start_time) + ' seconds' + '\n'
    
    #Return the scored nests after initialization
    return nests








