def moving_max(controlpts):
    # Takes input list and finds local maxes, defined as points that are 
    # the max of 5 neighboring points in a moving box
    import numpy
 
    num_pts = len(controlpts) #number of data points
    windowsize = 5 #insert windowsize here
 
    #We want to extend the control points so endpoints are treated equally
    #This is done by mirroring 4 points on each end
    controlpts_extend = []
    controlpts_extend = controlpts[:]
    for i in range(windowsize-1):
        controlpts_extend.insert(0, controlpts[i+1])
        controlpts_extend.append(controlpts[num_pts-i-2])
     
    #Here do the sliding window method to find peaks
    num_pts_extend = len(controlpts_extend)
    max_dump = (num_pts_extend-windowsize)*[None] 
    for index in range(len(controlpts_extend[0:(num_pts_extend-windowsize)])):
        max_dump[index] = max(controlpts_extend[index:(index+windowsize+1)])
 
    #Now that we have the values of the maximum for each window, we filter out
    #the special values that gets repeated as many time as the windowsize.
    #These are the local maxs
    holder = 0
    max_num = num_pts_extend*[None]
    for index in range(len(max_dump)):
        Count = max_dump.count(max_dump[index])
        if Count >= windowsize:
            max_num[holder] = max_dump[index]
            holder = holder + 1
 
    #The following steps removes None values.
    max_num = list(set(max_num))
    max_num = [f for f in max_num if f != None]
    max_num.reverse()
 
    #find index of local maxs
    #note difference between local_maxs which is a 2x num_pts array and
    #local_max which is a list
    zeros = [[0]*num_pts]
    local_maxs = numpy.array(zeros[:]*len(max_num), float)
    for i in range(len(max_num)):
        for j in range(num_pts):
            if controlpts[j] == max_num[i]:
                local_maxs[i][j] = controlpts[j] #first entry row, 2nd column
            if j <= (windowsize-1):
                if max(controlpts[0:j+1]) != max_num[i]:
                    local_maxs[i][j] = 0
            elif j >= (num_pts-windowsize +1):
                if max(controlpts[j:num_pts+1]) != max_num[i]:
                    local_maxs[i][j] = 0
            else:
                if max(controlpts[j:(j+windowsize)]) != max_num[i]:
                    local_maxs[i][j] = 0
    local_max = [0]*num_pts 
    for index in range(num_pts):
        local_max[index] = round((max(local_maxs[:,index])),3)
     
    return local_max
