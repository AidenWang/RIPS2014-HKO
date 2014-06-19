def peakfilter(x): 
      
    #%we have 360.0 since 6 hours in minutes is 360 minutes and the .0 is 
    #%to make the variable type a float. 
    time_step = 360.0/len(x) 
      
    #we have the have 60.0 because we don't want peaks to be within 
    #60 minutes of each other. To change this criterion, change this value. 
    width = 60.0/time_step 
      
    width = int(width - 1) 
    temp = x[:] 
    for k in range(len(x)): 
        #filter peaks backwards to choose earliest in the case of plateau 
        l = len(x)-k-1
          
        #the value 10 is the threshold value for a local max to be 
        #considered as a peak. To change this, change the value to desired 
        #threshold 
        if x[l] <= 10: 
            temp[l] = 0
  
        else: 
            temp_right = [(l+width), (len(x))] 
            right = min(temp_right) 
            temp_left = [(l-width), 0] 
            left = max(temp_left) 
            y = x[left:l] 
            z = x[l:right] 
            if z == []: 
                z = [0] 
            elif y ==[]: 
                y = [0] 
            if max(y) >= x[l] or max(z) > x[l]: 
                temp[l] = 0
    dump = temp[:] 
    peaks = [] 
    indices = [] 
    for k in range(len(dump)): 
        if dump[k] != 0: 
            peaks.append(dump[k]) 
            indices.append(k) 
            dump[k] = 0
    for i in range(len(indices)): 
        indices[i] = int(indices[i]*time_step) 
    return peaks, indices      
