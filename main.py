
############################################################################ 
                                  #Main.py
                     #Choose a date and optimization method
               #Calls Cowbird, Firefly, or CPSO Firefly Algorithms

############################################################################



#Date and time to start forecast in YYYYMMDDHHNN format 
#date_list = [200806070500, 200906110800, 201006100300, 201007281300, \
             #201204290100]
#end_list = [200806071300, 200906111600, 201006101100, 201007282100, \
            #201204290900]
date_list = [200906110800, 201006100300, 201007281300]
end_list = [200906111600, 201006101100, 201007282100]
#Additional date lists
#date_list = [201005070400, 200904250800, 200903240700, 201104171530]  
#date_list = [201005070400, 200904250800, 200903240700, 201104171530] #squalls 
#date_list = [201006100300, 200906110600, 200806070300, 200806061100, \n
             #201007281300, 201105221000] #monsoon 
#date_list = [201005070400, 200904250800, 200903240700, 201104171530,  
             #201006100300, 200906110600, 200806070300, 200806061100, \n
             #201007281300, 201105221000] #combined 

#SWIRLS directory (eg /home/swirls/operation/swirls2/) 
base_dir = '/home/swirls/rnd/swirls-rips/'

#Directory to save files 
#save_dir = base_dir + '/APTT/' 
save_dir = '/home/swirls/rnd/APTT/'
#Saves files as save_as_weight_type 
save_as = 'scores.txt'
  
#Optimization algorithm choices 
#1-Cowbird
#2-Firefly 

#Set to Cowbird
optimization_type = 1 

#Set single date
algorithm_type = 2

#Number of iterations to run optimization for 
iterations = 1

#Number of candidate solutions held (number of parameter sets)
#Note: Should be a multiple of the number of processors used 
solution_number = 32

#Vector keeps track of initialization time
timing = []

#Tracks how many tuning runs have occured
runs = 0

#List of settings to be  passed 
settings = [date_list, base_dir, save_dir, save_as] 

#Accessors for prepare.py 
#Do not use accessors for any routines run in parallel! 
def get_date(): 
    return date_list 
def get_base_dir(): 
    return base_dir 
def get_save_dir(): 
    return save_dir 
def get_save_as():
    return save_as

#This block run when main.py is called directly from the terminal
if __name__ == "__main__": 
    import GS, psof, sort_file, time
    import Cowbird, numpy

    #Run if Cowbird chosen as the preferred algorithm
    if optimization_type == 1:

          #Run Grasshopper for all listed dates
          for i in range(len(date_list)):
               print i, 'at the beginning'
               end_list[i], 'at the beginning'

               #Stores original save_as name 
               original_save_as = save_as 

               #For date in date_list: 
               #Appends the date to the end of original save_as name 
               save_as = original_save_as + str(date_list[i]) 

               #Changes the settings passed to get_score to only include a 
               #single date 
               settings = [date_list[i], base_dir, save_dir, save_as] 

               #Runs desired optimization 
               print '\n'*3 + 'Input date list: ' + str(date_list)

               #Begin timing initialization and add to vector "timing"
               timing.append(time.time())
       
               #Initialize the 32 parameter sets
	       nests = Cowbird.initialize(iterations, solution_number, settings)

               #End timing initialization and add to vector "timing"
               timing.append(time.time())

               #Take the begin and end times out of the "timing" vector to 
               #more easily be sent to the tuning run code
               firsttime = timing[-2]
               secondtime = timing[-1]

               
               tempdate = settings[0]
               print i, 'before while'
                    
                    #While the date is before the specified end time, run the program
               while int(tempdate)<int(end_list[i]): 
                    f = open(save_dir + 'best/' + save_as + '_best','a')
                    f.write(str(settings[0]) + ' / ' + str(nests[0][:6]) + ' / ' +  str(nests[0][6]) + '\n')
                    f.close()

                    g = open(save_dir + save_as + '_average','a')
                    g.write(str(settings[0]) + ' / Average: ' +  sum(nests[:][6])/float(len(nests[:][6]) + '\n')
                    g.close()

                    print i, 'inside while'
                    print end_list[i], 'end_list inside '
                    print 'Main: (Before) ' + str(settings[0])

                         #Run Grasshopper for one tuning run
	            nests = Cowbird.cowbird_search(nests, iterations, solution_number, settings, firsttime, secondtime)        
                    print 'Main: (After) ' + str(settings[0])
                    print i, 'at the end'
                    print settings[0]
                    print end_list[i]

                         #Update the temporary time
                    tempdate = settings[0]
                    print tempdate, 'tempdate'
                    


    if optimization_type == 2:
          print 'optimization 2'


