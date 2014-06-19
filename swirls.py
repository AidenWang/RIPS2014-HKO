#Module for getting SWIRLS forecast and actual rainfall data
import os, sys, get_data, moving_max, filter_peaks, score_forecast, main
 
#intime = 200806061100
#intime = 200806070300
#intime = 200903240700
#intime = 200904250800
#intime = 200906110600
#intime = 201005070400
#intime = 201006100300
#intime = 201007281300
intime = 201104171530
#intime = 201105221000
print intime
 
#start_lvl=1; max_lvl=7; rho=4.2; alpha=4200; sigma=4.2; interval=42
#params = [2, 7, 20.686, 19418.492999999999, 1.7969999999999999, 6]
#params = [0, 7, 11.144, 12.801, 5.45, 12]
 
#params = [0, 0, 1, 1, 4.89, 6] #best monsson
#params = [0, 4, 12.155, 2315.751, 5.671, 6] #best for 200806061100
#params = [0, 7, 13.819, 47589.777, 8.465, 18] #best for 200806070300
params = [0, 7, 6.429, 49260.538, 9, 6] #NEW BEST
#params = [0, 7, 12.729, 1, 9, 60] #best for 200903240700 
params = [0, 7, 19.464, 23668.295, 7.432, 6] #NEW BEST
#params = [0, 6, 6.097, 1, 8.669, 6] #best for 200904250800 
#params = [4, 7, 23.109, 1, 1.035, 60] #best for 200906110600
#params = [1, 5, 16.744, 49743.389, 7.163, 54] #best for 201005070400
#params = [1, 7, 1.331, 1, 2.386, 36] #best for 201006100300
#params = [4, 7, 1, 1, 1.671, 6] #best for 201007281300
params = [3, 7, 1.065, 1, 2.63, 54] #NEW BEST
#params = [4, 6, 23.919, 1, 4.927, 48] #best for 201104171530
params = [2, 7, 1.209, 35.421, 1.057, 6] #NEW BEST
#params = [4, 6, 17.996, 6596.267, 1.477, 36] #best for 201105221000
print params
 
#params = [0, 7, 10.313000000000001, 1.0, 6.6660000000000004, 12]   #1
#params = [0, 0, 12.0, 1.0, 5.0, 12] #923, best from PSO_4           4
#params = [0, 2, 2.819, 1, 1.955, 6] #better from Cuckoo, 93.06      2
#params = [0, 0, 11.965, 1, 5.773, 12] #best from Cuckoo, 93.28      3
 
#params = [0, 3, 11.185, 317.438, 4.78, 12] #best from GA, 91ish    
#params = [1, 3, 4.936, 162.303, 3.194, 12]
#params = [3, 7, 1.0, 1914.3520000000001, 1.0, 6] # best from PSO_1 so far
#params = [0, 7, 2.812, 1, 1.969, 6] #from Cuckoo
#params = [0, 7, 1, 25, 10, 12]
#params = [0, 7, 11.144, 12.801, 5.45, 12]
#params = [0, 7, 8.5630000000000006, 3125.6880000000001, 1.75, 12]
 
start_lvl = params[0]; max_lvl = params[1]; rho = params[2]
alpha = params[3]; sigma = params[4]; interval = params[5]
qpf = get_data.get_forecast(intime, start_lvl, max_lvl, rho, alpha, sigma, interval)
 
#Generate actual raingauge list 
actual = get_data.get_actual(intime)
 
#Peak finding
qpf_maxes = moving_max.moving_max(qpf)
#Filter forecast
[qpf_maxes, qpf_times] = filter_peaks.peakfilter(qpf_maxes)
 
#Actual peak finding
actual_maxes = moving_max.moving_max(actual)
#Filter actual
[actual_maxes, actual_times] = filter_peaks.peakfilter(actual_maxes)
 
#Scores
score = score_forecast.score_forecast(qpf, qpf_maxes, qpf_times, actual, actual_maxes, actual_times, 4)
 
print 'forecast'
print qpf
print 'actual'
print actual
print 'score: ', score
