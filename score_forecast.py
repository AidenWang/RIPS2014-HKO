#Functions for scoring an individual peak according to a specified scoring scheme
def scoreT_peak(eT, peakA, weight_scheme):
    import math
    #Score forecast using HKO hard cut-off metric.
    if weight_scheme == 1 or weight_scheme == 2 or weight_scheme == 3:
        Tmax = 40
        if abs(eT) <= Tmax:
            return peakA*(1-math.sqrt(abs(eT/Tmax)))
        else:
            return 0
    #Score forecast using asymmetric Gaussian
    elif weight_scheme == 4:
        sigmaTleft = 40.0; sigmaTright = 20.0
        if eT > 0:
            return peakA*math.exp(-(eT)**2/(2*sigmaTright**2))
        else:
            return peakA*math.exp(-(eT)**2/(2*sigmaTleft**2))
    #Score forecast using shifted Gaussian
    elif weight_scheme == 5:
        sigmaT = 40.0; kT = 20
        return peakA*math.exp(-(eT + kT)**2/(2*sigmaT**2))
    else:
        return 0
 
def scoreR_peak(eR, peakA, weight_scheme):
    import math
    #Score forecast using HKO hard cut-off metric.
    if weight_scheme == 1 or weight_scheme == 2 or weight_scheme == 3:
    Rmax = .3*peakA
        if abs(eR) <= Rmax:
            return peakA*(1-math.sqrt(abs(eR/Rmax)))
        else:
            return 0
    #Score forecast using asymmetric Gaussian
    elif weight_scheme == 4:
        sigmaRup = .3*peakA; sigmaRdown = .15*peakA
        if eR > 0:
            return peakA*math.exp(-(eR)**2/(2*sigmaRup**2))
        else:
            return peakA*math.exp(-(eR)**2/(2*sigmaRdown**2))
    #Score forecast using shifted Gaussian
    elif weight_scheme == 5:
        sigmaR = .3*peakA; kR = .2*peakA
        return peakA*math.exp(-(eR - kR)**2/(2*sigmaR**2))
    else:
        return 0
 
def scoreB_peak(eT, eR, peakA, weight_scheme):
    import math
    #Score forecast using HKO hard cut-off metric.
    if weight_scheme == 1 or weight_scheme == 2 or weight_scheme == 3:
        theta = math.atan2(eR, eT)
        #Adds 1 (weighted by actual intensity) if the forecast was early and an overestimate
        if theta <= math.pi and theta >= math.pi/2:
            return peakA
        else:
            return 0
    else:
        return 0
 
#For peak matching, deciding which of two candidate peaks is a better match
def tiebreaker(a, peakA, timeA, b, peakB, timeB, matchtime):
    #if one peak is way closer than the other, pick that one
    if abs(timeA - matchtime) + 10 < abs(timeB - matchtime):
        return a
    elif abs(timeB - matchtime) + 10 < abs(timeA - matchtime):
        return b
    #if one of the peaks is at a different warning color level choose the higher peak
    if peakA >= 70 and peakB < 70:
        return a
    elif peakB >= 70 and peakA < 70:
        return b
    elif peakA >= 50 and peakB < 50:
        return a
    elif peakB >= 50 and peakA < 50:
        return b
    elif peakA >= 30 and peakB < 30:
        return a
    elif peakB >= 30 and peakA < 30:
        return b
    #otherwise choose the earlier peak
    else:
        if timeA < timeB:
            return a
        else:
            return b
 
 
 
 
 
 
 
 
 
 
#Calculates the score for (filtered) forecast and actual data lists and peak info.
def score_forecast(forecast, peaksF, timesF, actual, peaksA, timesA, weight_scheme):
    import numpy
 
    #Weights of timing (T), intensity (R), bias (B), and least-squares error (LS)
    #Details of weight_schemes explained in get_score
    if weight_scheme == 1: #mixed sqrt metric
        wT = 0.35; wR = 0.25; wB = 0.2; wLS = 0.2
    elif weight_scheme == 2: #all peak sqrt metric
        wT = 0.4; wR = 0.35; wB = 0.25; wLS = 0
    elif weight_scheme == 3: #all least-squares
        wT = 0; wR = 0; wB = 0; wLS = 1
    elif weight_scheme == 4: #asymmetric Gaussian
        wT = 0.45; wR = 0.35; wLS = 0.2; wB = 0
    elif weight_scheme == 5: #offset Gaussian
        wT = 0.45; wR = 0.35; wLS = 0.2; wB = 0
 
 
    #peak matching
    epsilonT = [0]*len(peaksA); epsilonR = [0]*len(peaksA);
    matchedpeaksF = [0]*len(peaksA); matchedtimesF = [0]*len(peaksA)
    #loops through actual peaks, finds best match for each
    for j in range(0, len(peaksA)):
        #best time difference to actual peak
        besteT = 5000
        for i in range(0, len(peaksF)):
            #stores whether a candidate peak is a match
            match = 0
            #time diff for this peak
            eT = timesF[i] - timesA[j]
            #if this peak is definitely closer than current best, call it a match
            if abs(eT) < besteT + 10:
                match = 1
            #if its close, consider a tie
            elif abs(eT) < besteT - 10:
                best = tiebreaker(1, peaksF[i], timesF[i], 0, matchedpeaksF[j], matchedtimesF[j], timesA[j])
                #if it wins tie, call it a match
                if best == i:
                    match = 1
            if match == 1:
                #check for 1-2 matchings (single forecast peak used twice)
                if peaksF[i] in matchedpeaksF:
                    k = matchedpeaksF.index(peaksF[i])
                    best = tiebreaker(1, peaksF[i], timesF[i], 0, matchedpeaksF[k], matchedtimesF[k], timesA[j])
                    #if its better, remove the other peak
                    if best == 1:
                        matchedpeaksF[k] = 0
                        matchedtimesF[k] = 0
                    #if its worse, its no longer a match
                    else:
                        match = 0
                #if its still a match, add it to matched list
                if match == 1:
                    matchedpeaksF[j] = peaksF[i]
                    matchedtimesF[j] = timesF[i]
                    epsilonT[j] = eT
                    epsilonR[j] = peaksF[i] - peaksA[j]
 
 
    #Computes least squares score
    scoreLS = 0; normalize = 0
    #Interpolates the actual data to be of the same length as the forecast list
    forecast_grid = range(0,360,360/len(forecast))
    actual_grid = range(0,360,360/len(actual))
    actual_interp = numpy.interp(forecast_grid, actual_grid, actual)
    #Computes LS error
    for x in range(0, len(forecast)):
        scoreLS += abs(forecast[x]-actual_interp[x])**2
        normalize += actual_interp[x]**2
    #normalizes by overall squared intensity. now in 0<=SLS<=1, but 1 is bad.
    scoreLS /= normalize
    #reverses so 1 is good
    scoreLS = 1 - scoreLS
    #floors at 0
    if scoreLS < 0:
        scoreLS = 0
         
    scoreT = 0; scoreR = 0; scoreB = 0; normalize = 0
    #Scores each peak, weights by intensity of actual peak
    for k in range(len(peaksA)):
        normalize += peaksA[k]
        lowestT = 1; lowestR = 1
        if matchedpeaksF[k] != 0:
            scoreT = scoreT_peak(epsilonT[k], peaksA[k], weight_scheme)
            scoreR += scoreR_peak(epsilonR[k], peaksA[k], weight_scheme)
            scoreB += scoreB_peak(epsilonT[k], epsilonR[k], peaksA[k], weight_scheme)
    #normalizes by actual peak intensity
    scoreT /= normalize; scoreR /= normalize; scoreB /= normalize
    #Computes total score
    score = wT*scoreT + wR*scoreR + wB*scoreB + wLS*scoreLS
     
    return score
