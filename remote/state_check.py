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

os.system('ssh pi@10.0.10.200 python3 -u - {0} < scripts/set_coup_mode.py'.format(desired_state))