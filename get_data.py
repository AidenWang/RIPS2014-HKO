import os, datetime, time, sys, random
 #YOLO
def get_forecast(intime, min_lvl, max_lvl, rho, alpha, sigma, interval, base_dir, save_dir):
    # Runs the integrated script for SWIRLS forecaset, converts to list
    timestr = str(intime)
    # converts time to datetime format for addition of times
    yy = int(timestr[0:4]); mm = int(timestr[4:6]); dd = int(timestr[6:8])
    hh = int(timestr[8:10]); nn = int(timestr[10:12])
    startdatetime = datetime.datetime(yy,mm,dd,hh,nn)
    # folder for forecast data
    forecastpath = base_dir + "data/archive/" + str(yy) + \
        "/" + str(yy) + str(mm).zfill(2) + "/" + str(yy) + \
        str(mm).zfill(2) + str(dd).zfill(2) + "/output/statistic/" + \
        "irregular/qpf/2/064/ts_rank14p_full_time_steps/mugof-lv" + \
        str(min_lvl) + "-max" + str(max_lvl) + "-r" + str(rho) + \
        "-a" + str(alpha) + "-s" + str(sigma) + "-i" + str(interval) + \
        "-dbz33_zrhk"
    params = str(min_lvl) + " " + str(max_lvl) + " " + str(rho) + " "\
        + str(alpha) +  " " + str(sigma) + " " + str(interval)
 
    print '\n', 'Go to compare ' + timestr
    # checks if forecast has already been run
    while not os.path.isfile(forecastpath + '/ts_rank14p_' + timestr):
        #if it hasn't run it
    os.chdir(base_dir + "spt")
    os.system('./ForTuningCycle.spt ' + timestr + ' ' + params + ' > ' + \
    '/dev/null 2> /dev/null')
        #if the file still doesn't exist, output all zero forecast to guarantee 0 score
        if not os.path.isfile(forecastpath + '/ts_rank14p_' + timestr):
            #print/save error
            print '\n', '\n', '\n', 'ERROR!!!!!!'
            print '\n', 'Missing data ' + forecastpath + '/ts_rank14p_' + timestr
            print params
            f = open(save_dir + 'Bad_Parameters', 'a')
            f.write('['+str(min_lvl)+', '+str(max_lvl)+', '+str(rho)+', '+ \
                str(alpha)+', '+str(sigma)+', '+str(interval)+']\n')
            f.close()
            return [0]*60
    # Parses forecast, creates list
    os.chdir(forecastpath)
    # list for forecast data
    forecast = []
    titleline = 1
    # adds data to list
    forecastfile = open("ts_rank14p_" + timestr)
    for line in forecastfile:
        if titleline == 1:
            titleline = 0
            continue
        contents = line.split()
        forecast.append(float(contents[1]))
    forecastfile.close()
    # deletes raw output that takes up lots of space
    os.chdir(base_dir + "data/archive/" + str(yy) + "/" + str(yy) + \
        str(mm).zfill(2) + "/" + str(yy) + str(mm).zfill(2) + \
        str(dd).zfill(2) + "/output_raw/irregular/qpf/2/064/")
    os.system("rm -rf mugof-lv" + str(min_lvl) + "-max" + str(max_lvl) + "-r" + str(rho) + \
        "-a" + str(alpha) + "-s" + str(sigma) + "-i" + str(interval) + "-dbz33_zrhk")
    # Returns forecast
    return forecast
     
 
 
 
 
 
def prepare_actual(input_list):
    # Runs actual data preparation script
    intime = input_list[0]; base_dir = input_list[1]
    # parses input
    timestr = str(intime)
    yy = int(timestr[0:4]); mm = int(timestr[4:6]); dd = int(timestr[6:8])
    hh = int(timestr[8:10]); nn = int(timestr[10:12])
    startdatetime = datetime.datetime(yy,mm,dd,hh,nn)
    # loops through all times in forecast range
    for t in range(0, 120, 5):
        # runs data preparation script at each available interval in forecast (5 min)
        tempdatetime = startdatetime + datetime.timedelta(0,0,0,0,t)
        temptuple = tempdatetime.timetuple()
        temptimestr = time.strftime("%Y%m%d%H%M", temptuple)
        os.chdir(base_dir + "spt")
        os.system("./ForPreparation.spt " + temptimestr + " > " + \
            '/dev/null')            
        os.chdir('../module/04_post-processing/12_make_obs_rank_db_60qpfAtGauge/spt')
        os.system('./MakeObsRank.spt ' + str(temptimestr) + ' ' + str(temptimestr) + \
            ' 5 14 dummy > ' + '/dev/null')
 
 
 
 
 
 
def get_actual(intime, base_dir):
    # Parses actual data to list
    # parses input
    timestr = str(intime)
    yy = int(timestr[0:4]); mm = int(timestr[4:6]); dd = int(timestr[6:8])
    hh = int(timestr[8:10]); nn = int(timestr[10:12])
    startdatetime = datetime.datetime(yy,mm,dd,hh,nn)
    # list for holding actual raingauge data
    raingauge = []
    for t in range(0, 360, 5):
        # figures out time info for temptime
        tempdatetime = startdatetime + datetime.timedelta(0,0,0,0,t)
        temptuple = tempdatetime.timetuple()
        temptimestr = time.strftime("%Y%m%d%H%M", temptuple)
        tyy = int(temptimestr[0:4]); tmm = int(temptimestr[4:6]); tdd = int(temptimestr[6:8])
        thh = int(temptimestr[8:10]); tnn = int(temptimestr[10:12])
        # parses data, adds rainfall intensity to rainguage list
        raingaugepath = base_dir + "data/archive/" + \
            str(tyy) + "/" + str(tyy) + str(tmm).zfill(2) + "/" + str(tyy) + \
            str(tmm).zfill(2) + str(tdd).zfill(2) + "/output/statistic/" + \
            "irregular/gauge_rf/hk/rf60m_qced/rank14p"
        os.chdir(raingaugepath)
        titleline = 1
        print raingaugepath
        raingaugefile = open("rank14p_" + temptimestr)
        for line in raingaugefile:
            if titleline == 1:
                titleline = 0
                continue
            contents = line.split()
            raingauge.append(float(contents[1]))
        raingaugefile.close()
    # Returns list of actual rainfall intensity
    return raingauge
