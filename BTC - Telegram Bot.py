#!/usr/bin/python3

import json
import threading
import time
import requests as r
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import datetime


def update_db(title,rawData):
    with open("data.json") as json_data:
        print(json_data)
        data = json.load(json_data)
    data[title]={"open":rawData[0] #continue from here i.e.,rawData[0][1]
    print(title,rawData)

def get_price(run_event):
    
    alteration = [0,1,7,30]
    alteration_index = 0
    now = datetime.datetime.now()
    today = (now-datetime.timedelta(days=1)).strftime("%d")
    print(today)

    
    #block to update price for 0,1,7 and 30 days in the same sequence
    while run_event.is_set():
        #if..else block to iterate through alteration array and choose values to update
        if alteration_index <=3 and not today==now.strftime("%d"):
            temp_now = now-datetime.timedelta(days=alteration[alteration_index])
            fixedDate = temp_now.strftime("%Y"+"-"+"%m"+"-"+"%d")

        else:
            today = now.strftime("%d")
            now = datetime.datetime.now()
            alteration_index = 0
            temp_now = now-datetime.timedelta(days=alteration[alteration_index])
            fixedDate = temp_now.strftime("%Y"+"-"+"%m"+"-"+"%d")
            
        alteration_index += 1    #instead of having this line in both if and else statement we have kept it outside but still it is part of if else logic
        url = "https://api.pro.coinbase.com/products/BTC-USD/candles?start="+fixedDate+"T00%3A00%3A00.0Z&end="+fixedDate+"T00%3A00%3A00.0Z&granularity=86400"
        session = Session()
        try:
            response = session.get(url)
            data = json.loads(response.text)
            update_db(alteration[alteration_index-1],data)
        except ValueError as e:
            print(e)
        time.sleep(1)  #Find out time to update


if __name__ == "__main__":
    
    run_event = threading.Event()
    run_event.set()
    with open('data.json', 'w') as new_file:
        new_file.write(json.dumps({"0":"","1":"","7":"","30":""},skipkeys=True))
    new_file.close()
    
    try:
        t1 = threading.Thread(target=get_price, args=(run_event,))
        t1.start()
    except ValueError:
        print("Error: unable to start thread", ValueError)

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        run_event.clear()
        t1.join()
