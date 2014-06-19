import os, sys, get_data, moving_max, filter_peaks, score_forecast, main
 
intime = 201207232130
print intime
 
#start_lvl=1; max_lvl=7; rho=4.2; alpha=4200; sigma=4.2; interval=42
params = [1, 7, 24, 1, 8.0, 60] #NEW BEST
print params
 
start_lvl = params[0]; max_lvl = params[1]; rho = params[2]
alpha = params[3]; sigma = params[4]; interval = params[5]
base_dir = '/home/nowcast/rnd/swirls-rips/'
save_dir = '/tmp/'
qpf = get_data.get_forecast(intime, start_lvl, max_lvl, rho, alpha, sigma, interval, base_dir, save_dir)
 
#Generate actual raingauge list 
actual = get_data.get_actual(intime, base_dir)
 
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
