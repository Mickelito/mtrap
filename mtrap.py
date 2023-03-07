import requests as req
import json
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import os

def get_changes_in_interval(oldest: dt.datetime, newest: dt.datetime, api: str):
    """
    Count occurences of "NEW", "MERGED", and "ABANDONED" among changes submitted between 'oldest' and 'newest', from the URL 'api'
    """
    lim_num_changes = 0
    if "android" in api:
        lim_num_changes = 2000
    else: # if "chromium" or "openstack"
        lim_num_changes = 500

    q_param = 'after:"' + oldest.strftime("%Y-%m-%d %H:%M:%S +0100") +'" and before:"' + newest.strftime("%Y-%m-%d %H:%M:%S +0100") +'"'
    query = {'q':q_param, 'no-limit':'true'}
    
    changes_raw = req.get(api, params = query)
    
    changes_json = json.loads(changes_raw.text[4:])
    tot_changes = [0,0,0]
    if len(changes_json) >= lim_num_changes:
        tot_diff = newest - oldest
    
        newer_changes, newer_json = get_changes_in_interval(oldest + tot_diff / 2, newest, api)
        older_changes, older_json = get_changes_in_interval(oldest, oldest + tot_diff / 2, api)
    
        for i in range(len(tot_changes)):
            tot_changes[i] += newer_changes[i]
            tot_changes[i] += older_changes[i]
        changes_json += older_json
        changes_json += newer_json[1:]
    
    else:
        for change in changes_json:
            if change["status"] == "NEW":
                tot_changes[0] += 1
            elif change["status"] == "MERGED":
                tot_changes[1] += 1
            elif change["status"] == "ABANDONED":
               tot_changes[2] += 1
    
    return tot_changes, changes_json

def get_changes_last_days(now:dt.datetime, api:str, no_days: int):
    """
    Get changes from the last 'no_days' days (no_days * 24h), datapoints every 30 minutes
    """
    start = now + dt.timedelta(days = -no_days)
    diff = dt.timedelta(minutes = 30)

    time_points = [] # to be used as x-axis for graph
    for i in range(1, (no_days*24*2)+1):
        time_points.append((start + i * diff).strftime("%Y-%m-%d %H:%M:%S"))

    data_points = [[],[],[]]
    full_json = []
    for i in range(no_days*24*2):
        changes_30_min, json_30_min = get_changes_in_interval(start + i*diff, start + (i+1)*diff, api)
        for i in range(len(data_points)):
            data_points[i].append(changes_30_min[i])
        full_json += json_30_min
    
    return time_points, data_points, full_json

def plot_changes(time_points, data_points, no_days:int, now_time:dt.datetime, save_path:str):
    total_plot_name = now_time.strftime("%Y-%m-%d_%H%M%S") +"_total_" + str(no_days) + "d.pdf"
    new_plot_name = now_time.strftime("%Y-%m-%d_%H%M%S") +"_new_" + str(no_days) + "d.pdf"
    merged_plot_name = now_time.strftime("%Y-%m-%d_%H%M%S") +"_merged_" + str(no_days) + "d.pdf"
    abandoned_plot_name = now_time.strftime("%Y-%m-%d_%H%M%S") +"_abandoned_" + str(no_days) + "d.pdf"

    new = np.asarray(data_points[0])
    merged = np.asarray(data_points[1])
    abandoned = np.asarray(data_points[2])
    x = np.asarray(time_points, dtype='datetime64')
    
    no_new = 0
    no_merged = 0
    no_abandoned = 0
    for i in range(len(new)):
        no_new += new[i]
        no_merged += merged[i]
        no_abandoned += abandoned[i]
    
    # total changes plot
    plt.figure("total")
    plt.tick_params(axis='x',which='major',labelsize='5')
    plt.plot(x, new)
    plt.plot(x, merged)
    plt.plot(x, abandoned)
    x_axis_str = "Time\n Total opened: " + str(no_new) + "    Total closed: " + str(no_merged+no_abandoned)
    plt.xlabel(x_axis_str)
    plt.ylabel('Number of changes')
    plt.title("Total changes between " + time_points[0] + " and " + time_points[-1])
    plt.legend(['NEW', 'MERGED', 'ABANDONED'])
    plt.savefig(os.path.join(save_path,total_plot_name), format="pdf")
    
    # new changes plot
    plt.figure("new")
    plt.plot(x, new)
    x_axis_str = "Time\n Total opened: " + str(no_new)
    plt.xlabel(x_axis_str)
    plt.ylabel('Number of changes')
    plt.title("Opened changes between " + time_points[0] + " and " + time_points[-1])
    plt.legend(['NEW'])
    plt.savefig(os.path.join(save_path,new_plot_name), format="pdf")

    # merged changes plot
    plt.figure("merged")
    plt.plot(x, merged)
    x_axis_str = "Time\n Total merged: " + str(no_merged)
    plt.xlabel(x_axis_str)
    plt.ylabel('Number of changes')
    plt.title("Merged changes between " + time_points[0] + " and " + time_points[-1])
    plt.legend(['MERGED'])
    plt.savefig(os.path.join(save_path,merged_plot_name), format="pdf")

    # abandoned changes plot
    plt.figure("abandoned")
    plt.plot(x, abandoned)
    x_axis_str = "Time\n Total abandoned: " + str(no_abandoned)
    plt.xlabel(x_axis_str)
    plt.ylabel('Number of changes')
    plt.title("Abandoned changes between " + time_points[0] + " and " + time_points[-1])
    plt.legend(['ABANDONED'])
    plt.savefig(os.path.join(save_path,abandoned_plot_name), format="pdf")

    return 0

def predict_word(input: str, available_words: list):
    for word in available_words:
        if input.lower()[0] == word[0] and input.lower() in word:
            return word
    return -1

def check_dir(dir_path:str):
    if not os.path.exists(dir_path):
        return 1
    if os.path.isfile(dir_path):
        print("Cannot create directoy: '"+dir_path+"' already exists" )
        return -1
    return 0
    
def number_of_days(input: str):
    for i in input:
        if i not in "0123456789":
            return -1
    num = int(input)
    if num > 60 or num < 1:
        return -1
    return num

def write_log(now:dt.time, no_days:int, log_dir:str, log_data):
    log_name = now.strftime("%Y-%m-%d_%H%M%S")+"_log_"+str(no_days)+"d.json"
    log_path = os.path.join(log_dir, log_name)
    with open(log_path, "w") as out:
        out.write(json.dumps(log_data, indent=4))
    return 0

def main():
    now = dt.datetime.now()
    links = {
        "chromium" : "https://chromium-review.googlesource.com/changes/",
        "openstack" : "https://review.opendev.org/changes/",
        "android" : "https://android-review.googlesource.com/changes/"
    }
    cwd = os.getcwd()
    plots = os.path.join(cwd, "mtrap_plots")
    logs = os.path.join(cwd, "mtrap_json_logs")
    if check_dir(plots) == -1:
        return -1
    elif check_dir(plots) == 1:
        os.mkdir(plots)
    if check_dir(logs) == -1:
        return -1
    elif check_dir(logs) == 1:
        os.mkdir(logs)
    
    while True:
        api_input = input("Pick one of the following as source for analysis [chromium | openstack | android]: ")
        api = predict_word(api_input, links.keys())
        if api == -1:
            print("  Invalid input: no source '" + api_input + "'\n  Valid sources are 'chromium', 'openstack' and 'android'")
            continue
        print("   Source: " + links[api])
        time_input = input("Choose a number of days in the past to analyze from (1-60): ")
        time = number_of_days(time_input)
        if time == -1:
            print("  Invalid number of days: '" + time_input + "'\n  Valid numbers are integers in the range [1,60]")
            continue
        print("   Number of days: " + str(time))
        print("Fetching data...")
        data_pts, time_pts, json_log = get_changes_last_days(now, links[api], time)
        plot_changes(data_pts, time_pts, time, now, plots)
        write_log(now, time, logs, json_log)
        return 0

if __name__ == "__main__":
    main()
