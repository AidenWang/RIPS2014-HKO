# coding: utf-8
forecaststr = raw_input("enter forecast: ")
forecast = [float(x) for x in forecaststr.split(', ')]
#actualstr = raw_input("enter actual: ")
#actual = [float(x) for x in actualstr.split(', ')]
actual = [5.5, 5.5, 6.0, 5.5, 6.0, 6.0, 6.0, 6.0, 6.0, 5.5, 5.5, 5.0999999999999996, 5.5, 5.0, 4.5, 4.5, 4.0, 4.0, 4.5, 4.5, 4.5, 5.0, 6.5, 9.0, 14.5, 16.5, 19.0, 22.0, 22.0, 23.5, 25.0, 25.5, 28.0, 30.5, 31.0, 30.0, 33.0, 34.5, 33.5, 33.0, 36.0, 37.0, 35.5, 35.5, 32.0, 31.5, 31.5, 31.5, 29.0, 25.0, 23.0, 20.0, 17.0, 12.5, 8.5, 6.5, 4.5, 4.0, 3.5, 3.5, 3.0, 3.0, 2.5, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5]
plt.figure(2)
p = plt.axhspan(30, 50, facecolor='y', alpha=0.5)   #amber zone
p = plt.axhspan(50, 70, facecolor='r', alpha=0.5)   #red zone
p = plt.axhspan(70, 100, facecolor='k', alpha=0.5)  #black zone
x = range(0,360,6)
y = range(0,360,5)
plt.plot(x, forecast, 'x', x, forecast)
plt.plot(y, actual, 'y', y, actual)
import moving_max
import filter_peaks
import score_forecast
maxesF = moving_max.moving_max(forecast)
maxesA = moving_max.moving_max(actual)
peaksF = filter_peaks.peakfilter(maxesF)
peaksA = filter_peaks.peakfilter(maxesA)
timesF = filter_peaks.ser_time(forecast, peaksF)
timesA = filter_peaks.ser_time(actual, peaksA)
[peaksF, timesF] = filter_peaks.del_rep(peaksF, timesF)
[peaksA, timesA] = filter_peaks.del_rep(peaksA, timesA)
scoreMX = score_forecast.score_forecast(forecast, peaksF, timesF, actual, peaksA, timesA, 1)
print 'Mixed HKO:', scoreMX
scoreLS = score_forecast.score_forecast(forecast, peaksF, timesF, actual, peaksA, timesA, 3)
print 'Least Sqr:', scoreLS
scoreSG = score_forecast.score_forecast(forecast, peaksF, timesF, actual, peaksA, timesA, 5)
print 'Sft Gauss:', scoreSG
scoreAG = score_forecast.score_forecast(forecast, peaksF, timesF, actual, peaksA, timesA, 4)
print 'Asm Gauss:', scoreAG
blank = raw_input("Press enter to close")
