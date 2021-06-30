#!/usr/bin/env python3

import requests
import time
import notify2
import os

from datetime import datetime, timedelta, date

      
def check(cur_date, pincode, age_limit):
    query = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, cur_date)

    res = requests.get(query)
    r = res.json()

    # get centers
    centers = []
    for center in r['centers']:
        centers.append(center)

    # for each center get sessions

    available = False
    sessions_list = []    
    for center in centers:  
        #print(center['name'])
        #print("Fee: ", center['fee_type'])
        for session in center['sessions']:
             # min age limit = 18
            min_age_limit = session['min_age_limit']
            if min_age_limit < age_limit:
                s_date = session['date']
                cap = session['available_capacity_dose1']
                #print("Date: ", s_date)
                #print("Capacity: ", cap)
                #print()
                # only free sessions
                if cap > 0 and center['fee_type'] == 'Free':
                    available = True
                sessions_list.append((s_date, cap))
    

    # if vaccinen available notify
    notify2.init('alert')
    if available:
        vdate, vcap = sessions_list[0]
        str_date = 'On ' +  vdate
        str_cap = 'Slots: ' + str(vcap)
        msg = 'Vaccine Available!\n' + str_date + '\n' + str_cap + '\n\n'
            
        # alert
        play_sound()
        n = notify2.Notification(msg)
        n.show()
    else:
        n = notify2.Notification('No free slots available')
        n.show()
        
def play_sound():
    import os
    duration = 2  # seconds
    freq = 540  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


if __name__ == "__main__":
    cur_date = date.today().strftime("%d-%m-%Y")
    pincode = '713206'
    duration = 15   # minutes
    
    while True:
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        print(result, ' checking vaccine slot..')
        check(cur_date, pincode, 45)

        dt = datetime.now() + timedelta(minutes=duration)
        dt = dt.replace(second=1)

        while datetime.now() < dt:
            # check every 15 mins
            time.sleep(60*duration)
