#date and time to start forecast in YYYYMMDDHHNN format 
date_list = [201005070400, 200904250800, 200903240700, 201104171530]  
#date_list = [201005070400, 200904250800, 200903240700, 201104171530] #squalls 
#date_list = [201006100300, 200906110600, 200806070300, 200806061100, 201007281300, 201105221000] #monsoon 
#date_list = [201005070400, 200904250800, 200903240700, 201104171530,  
#    201006100300, 200906110600, 200806070300, 200806061100, 201007281300, 201105221000] #combined 
#swirls2 directory (eg /home/swirls/operation/swirls2/) 
base_dir = '/home/swirls/rnd/swirls-rips/'
#directory to save files 
#save_dir = base_dir + '/APTT/' 
save_dir = '/home/swirls/rnd/APTT/'
#saves files as save_as_weight_type 
save_as = 'scores.txt'
  
#optimization algorithm to be used. 
#1-cuckoo search (default) 
#2-particle swarm optimization 
#3-genetic algorithm 
optimization_type = 1
#optimize ave over all dates or each date separately? 
#1-multi date, optimize average score for all dates 
#2-single date, optimize each date separately 
average_type = 2
#number of iterations to run optimization for 
#defults: cuckoo-100, PSO-50, GA-100 
iterations = 100
#number of candidate solutions held. 
#should be a multiple of the number of processors used 
#defaults: cuckoo-25, PSO-200, GA-200 
solution_number = 25
  
#list of settings to be  passed 
settings = [date_list, base_dir, save_dir, save_as] 
#accessors for prepare.py 
#do not use accessors for any routines run in parallel! 
def get_date(): 
    return date_list 
def get_base_dir(): 
    return base_dir 
  
  
#this block run when main.py is called directly from the terminal 
if __name__ == "__main__": 
    import GS, psof, CuckooSearch_forSWIRLS_multi, sort_file  
  
    #multi-date optimization 
    if average_type == 1: 
        #runs desired optimization function 
        if optimization_type == 1: 
            dump = CuckooSearch_forSWIRLS_multi.cuckoo_search(iterations, solution_number, settings) 
        if optimization_type == 2: 
            dump = psof.pso(iterations, solution_number, settings) 
        if optimization_type == 3: 
            dump = GS.imp_GS(iterations, solution_number, settings) 
        #outputs and saves results 
        print "parameters = " + str(dump[0]) 
        print "score = " + str(dump[1]) 
        parameters = dump[0] 
        score = dump[1] 
        f = open(base_dir + '/data/APTT/' + save_as + '_best','w') 
        f.write(repr(parameters) + ' ' +  str(score)) 
        f.close() 
        #creates file with top 100 distinct parameter sets 
        sort_file.sort_file(save_dir, save_as) 
  
  
    #single date optimization 
    if average_type == 2: 
        #stores original save_as name 
        original_save_as = save_as 
        for date in date_list: 
            #appends the date to the end of original save_as name 
            save_as = original_save_as + str(date) 
            #changes the settings passed to get_score to only include a single date 
            settings = [[date], base_dir, save_dir, save_as] 
            #runs desired optimization 
            if optimization_type == 1: 
                dump = CuckooSearch_forSWIRLS_multi.cuckoo_search(iterations, solution_number, settings) 
            if optimization_type == 2: 
                dump = psof.pso(iterations, solution_number, settings) 
            if optimization_type == 3: 
                dump = GS.imp_GS(iterations, solution_number, settings) 
            #outputs and saves results 
            print "parameters = " + str(dump[0]) 
            print "score = " + str(dump[1]) 
            parameters = dump[0] 
            score = dump[1] 
            f = open(base_dir + '/data/APTT/' + save_as + '_best','w') 
            f.write(repr(parameters) + ' ' +  str(score)) 
            f.close() 
            #creates file with top 100 distinct parameter sets 
            sort_file.sort_file(save_dir, save_as) 
