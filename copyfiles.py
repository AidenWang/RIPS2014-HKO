#Module for getting SWIRLS forecast and actual rainfall data
import os
 
dates = ['20110522', '20100507', '20090425', '20090324', '20110417', '20090609', \
    '20100610', '20090611', '20080607', '20080606', '20100728']
 
for timestr in dates:
    yy = timestr[0:4]; mm = timestr[4:6]; dd = timestr[6:8]
    hh = timestr[8:10]; nn = timestr[10:12]
 
    baseinput = '/home/nowcast/rnd/swirls-rips/data/archive/test/HKO-SWIRLS-RIPS-HK-2012/' + timestr
    baseoutput = '/home/nowcast/rnd/swirls-rips/data/archive/' + yy + '/' + yy + mm + '/' + yy + \
        mm + dd
 
    print baseoutput
 
    os.system('mkdir -p ' + baseoutput + '/input_raw/grid/radar/ref/2/128')
    os.system('mv ' + baseinput + '/ref/128/* ' + baseoutput + '/input_raw/grid/radar/ref/2/128')
    os.system('mkdir -p ' + baseoutput + '/input_raw/grid/radar/ref/2/256')
    os.system('mv ' + baseinput + '/ref/256/* ' + baseoutput + '/input_raw/grid/radar/ref/2/256')
    os.system('mkdir -p ' + baseoutput + '/input_raw/irregular/gauge_rf/hk/rf4h')
    os.system('mv ' + baseinput + '/rf4h/* ' + baseoutput + '/input_raw/irregular/gauge_rf/hk/rf4h')
    os.system('mkdir -p ' + baseoutput + '/input/aux/zr/param/hk')
    os.system('mv ' + baseinput + '/zr/* ' + baseoutput + '/input/aux/zr/param/hk')
