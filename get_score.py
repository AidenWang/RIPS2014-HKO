def get_score(params, settings):
    #Module for getting SWIRLS forecast and actual rainfall data
    import os, sys, get_data, moving_max, filter_peaks, score_forecast, numpy, math

    #SET WEIGHT SCHEME. 1=mix, 2=all peak, 3=all least-squares, 4=asymmetric Gaussain, 5=shifted Gaussian
    weight_scheme = 4

    #parses argument list
    #seperates input tuning parameters
    start_lvl = params[0]; max_lvl = params[1]; rho = params[2]
    alpha = params[3]; sigma = params[4]; interval = params[5]
    #seperates settings sent from main
    date_list = settings[0]; base_dir = settings[1]; 
    save_dir = settings[2]; save_as = settings[3]

    #list of scores for each date in date_list
    scores = []
    #Loops over all dates in main.get_date()
    #for intime in date_list:
        #Generate forecast list 
    qpf = get_data.get_forecast(date_list, start_lvl, max_lvl, rho, alpha, sigma, interval, base_dir, save_dir)

        #Generate actual raingauge list 
    actual = get_data.get_actual(date_list, base_dir)

        #Peak finding
    qpf_maxes = moving_max.moving_max(qpf)
        #Filter forecast
    [qpf_maxes, qpf_times] = filter_peaks.peakfilter(qpf_maxes)

        #Actual peak finding
    actual_maxes = moving_max.moving_max(actual)
        #Filter actual
    [actual_maxes, actual_times] = filter_peaks.peakfilter(actual_maxes)

        #Scores
    scores.append(math.sqrt(score_forecast.score_forecast(qpf, qpf_maxes, qpf_times, actual, actual_maxes, actual_times, weight_scheme)))

    #Average score over all dates in range
    score = numpy.average(scores)
    #Standard deviation of scores over dates in date_list
    stddev = numpy.std(scores)
    #print str(round(score, 4)) + ' score, ' + str(round(stddev, 4)) + ' stddev,  ' + repr(params)

    #Saves ave score and std dev to save_dir/save_as
    f = open(save_dir + save_as,'a')
    f.write(str(round(score, 4)) + ' score, ' + str(round(stddev, 4)) + ' stddev, ' + repr(params) + '\n')
    f.close()

    return score
