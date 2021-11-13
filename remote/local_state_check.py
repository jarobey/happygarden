from happygarden.mycoup import Coup
import sys, time, os

# hour then minute in current local tz and mode to switch to
# assume circular and low to high on 24h clock
times = [
[6, 30, 'mode_all_on'],   # at 6:30 am switch to all on
[19, 45, 'mode_pre_bed'], # at 7:45 pm switch to pre bed mode
[20, 00, 'mode_all_off']  # at 8:00 pm switch to all off
]

cur_datetime = time.localtime()

print("Current time is {0}".format(cur_datetime))
desired_state = times[-1][2]
for time in times:
    if cur_datetime.tm_hour < time[0]: break
    if cur_datetime.tm_hour == time[0] and cur_datetime.tm_min < time[1]: break
    desired_state = time[2]
        
print(desired_state)

modes = {
    'mode_all_on':  """{"Coup": {"Lights": {"Run Light 1": true , "Run Light 2": true , "Coup Light 1": true, "Coup Light 2": true}}}""",
    'mode_all_off': """{"Coup": {"Lights": {"Run Light 1": false, "Run Light 2": false, "Coup Light 1": false, "Coup Light 2": false}}}""",
    'mode_pre_bed': """{"Coup": {"Lights": {"Run Light 1": true , "Run Light 2": false, "Coup Light 1": false, "Coup Light 2": false}}}"""
}

mode = modes[desired_state]

coup = Coup()
status = coup.get_status()
print("Starting state: {0}\nSetting to:     {1}".format(coup.get_status(), mode))
coup.set_state(mode)
print("Final state:    {0}".format(coup.get_status()))
