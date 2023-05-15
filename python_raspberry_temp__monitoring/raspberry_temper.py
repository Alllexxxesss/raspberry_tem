import argparse
import os
import time
import datetime


MAX_TEMP_MIN = 0
MAX_TEMP_MAX = 90
TEMP_FILE = "/sys/class/thermal/thermal_zone0/temp"
LOG_FILE = "./tempch.log"
LOCK_FILE = './90732056345lock.loc'



a = argparse.ArgumentParser()
b = argparse.FileType()
#print (type(b))
#print (type(a))
#print (type(func1))
a.add_argument('max_temp', type=int, help='Maximum allowable temperature (0-90)')
a.add_argument('time_max_temp', type=int, help='Maximum allowable operating time with excess temperature')
a.add_argument('what_to_do', type=str, help='Execute command if maximum allowed time is exceeded')
if (a.parse_args().max_temp < MAX_TEMP_MIN) or (a.parse_args().max_temp > MAX_TEMP_MAX):
    print (f'parameter max_temp must be within {MAX_TEMP_MIN} - {MAX_TEMP_MAX}')
    exit (1)
elif (a.parse_args().time_max_temp < 1):
    print ('parameter time_max_temp must be > 0')
    exit (1)
try:
    file = open(TEMP_FILE, 'r')
except FileNotFoundError:
    print('can not open file /sys/class/thermal/thermal_zone0/'
          'temp')
    exit (1)

try:
    file = open (LOCK_FILE,'x')

except FileExistsError:
    print ('lock file found, maybe an instance of the program is already runing')
    exit (1)
else:
    file.close()



for i in range(a.parse_args().time_max_temp):
    current_temp = int(file.readline()) // 1000
    if current_temp < a.parse_args().max_temp:
        break
    file.seek(0)
    time.sleep(1)
    print(i)
if i == (a.parse_args().time_max_temp - 1):
    print('the maximum allowable temperature has been exceeded : ', current_temp)
    try:
        file2 = open(LOG_FILE, 'a')
        file2.write ('\n-----------------------')
        file2.write (str(datetime.datetime.today()))
        file2.write ('------------------------\n')
        file2.write ('exceeding maximum temperature :\nmaximum allowable temperature - ')
        file2.write (str(a.parse_args().max_temp))
        file2.write ('\nrecorded temperature - ')
        file2.write (str(current_temp))
        #file2.write ('text')
        file2.close()
    except FileNotFoundError:
        print ('can not open log file')
    except PermissionError:
        print ('can not create log file')

    os.system("sudo echo Temperatura error")

try:
    os.remove(LOCK_FILE)

except FileNotFoundError:
        print ('can not delete lock file, file not found')
except PermissionError:
        print ('can not create lock file, permission denied')

file.close()


