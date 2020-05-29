from api import apiGet, timeTableGet
import matplotlib
import matplotlib.pyplot as plt
import traceback
import datetime
import dateutil
import numpy as np

def formatData(json):
    list = {"times": [], "values": []}
    for time in json:
        time["time"] = dateutil.parser.isoparse(time["time"])
    for item in json:
        list["times"].append(item["time"])
        list["values"].append(item["value"])
    return list

def vis(subplotNo, data, room, sensor):
    fig = plt.figure(figsize=(10, 8))
    if len(data) >= subplotNo:
        irange = subplotNo
    else:
        irange = len(data)

    for i in range(irange):
        if data[i]["times"] != []:
            ax = plt.subplot(irange/3+1, 3, i+1)
            plt.plot_date(data[i]["times"], data[i]["values"], xdate=True, linestyle="-")
            plt.title(f'{room} {sensor} {data[i]["times"][0].strftime("%d %b")}: {len(data[i]["values"])} datapoints')
            print(f'{room} {sensor} {data[i]["times"][0].strftime("%d %b")}: {len(data[i]["values"])} datapoints' )
            my_xticks = ax.get_xticks()
            plt.xticks([my_xticks[0], my_xticks[-1]], [data[i]["times"][-1].strftime("%X"), data[i]["times"][0].strftime("%X")])
    fig.tight_layout()

def display(room1, room2, room3, sensor, subplots, studentNo):
    """ A function that displays the infomation from a given sensor for 3 rooms if the student is scheduled to be in that room 
        
        roomX: in the format of a USB room such as "room-8.025"
        
        sensor: one of ["occupancy-sensor", "co2", "room-temperature", "relative-humidity"]
        
        studentNo: in the format XXXXXXXXX
        """
        
    r1 = []
    r3 = []
    r2 = []
    events = timeTableGet(studentNo)
    for e in events:
        try:
            loc1 = e["location"].replace("USB.", "room-")
            loc2 = loc1.replace(" SR", "")
            #print(apiGet(loc2, sense[1], tfStart=e["start"], tfEnd=e["end"]))  
            #print(loc2)
            if loc2 == room1:
                r1.append(formatData(apiGet(loc2, sensor, tfStart=e["start"], tfEnd=e["end"])))
            if loc2 == room2:
                r2.append(formatData(apiGet(loc2, sensor, tfStart=e["start"], tfEnd=e["end"])))
            if loc2 == room3:
                r3.append(formatData(apiGet(loc2, sensor, tfStart=e["start"], tfEnd=e["end"])))

        except Exception:
            print(f"ERROR IN {e['location']}")
            traceback.print_exc()

    vis(subplots, r3, room3.replace("room-", ""), sensor)
    vis(subplots, r2, room2.replace("room-", ""), sensor)
    vis(subplots, r1, room1.replace("room-", ""), sensor)
    plt.show()

sense = ["occupancy-sensor", "co2", "room-temperature", "relative-humidity"]


display("room-4.022", "room-4.005", "room-2.022", sense[1], 12, 160508552)




