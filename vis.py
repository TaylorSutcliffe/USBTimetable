from api import apiGet, timeTableGet
import matplotlib
import matplotlib.pyplot as plt
import requests
import traceback
import datetime
import dateutil
import seaborn as sns
import numpy as np

sense = ["occupancy-sensor", "co2", "room-temperature", "relative-humidity"]
events = timeTableGet(160508552)
e1 = events[-1]
loc = e1["location"].replace("USB.", "room-")
r4022 = []
r2022 = []
r4005 = []

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
        ax = plt.subplot(irange/3+1, 3, i+1)
        plt.plot_date(data[i]["times"], data[i]["values"], xdate=True, linestyle="-")
        plt.title(f'{room} {sensor} {data[i]["times"][0].strftime("%d %b")}')
        my_xticks = ax.get_xticks()
        plt.xticks([my_xticks[0], my_xticks[-1]], [data[i]["times"][0].strftime("%X"), data[i]["times"][-1].strftime("%X")], visible=True)
    fig.tight_layout()

for e in events:
    try:
        loc1 = e["location"].replace("USB.", "room-")
        loc2 = loc1.replace(" SR", "")
        #print(apiGet(loc2, sense[1], tfStart=e["start"], tfEnd=e["end"]))  
        #print(loc2)
        if loc2 == "room-4.022":
            r4022.append(formatData(apiGet(loc2, sense[1], tfStart=e["start"], tfEnd=e["end"])))
        if loc2 == "room-4.005":
            r4005.append(formatData(apiGet(loc2, sense[1], tfStart=e["start"], tfEnd=e["end"])))
        if loc2 == "room-2.022":
            r2022.append(formatData(apiGet(loc2, sense[1], tfStart=e["start"], tfEnd=e["end"])))
    except Exception:
        print(f"ERROR IN {e['location']}")
        traceback.print_exc()

vis(12, r2022, "2.022", "CO2")
vis(12, r4005, "4.005", "CO2")
vis(12, r4022, "4.022", "CO2")
plt.show()




