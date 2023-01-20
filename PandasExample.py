#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Nina Nguyen

import pandas as pd

#Read the json
data = json.load(open('D:\\merged_partition_content\\Desktop\\01.01.2016.CHA.at.TOR\\0021500492.json'))
pd.reset_option('max_columns')
pd.set_option('expand_frame_repr', False)

# Extract the data from the JSON
gameid = data["gameid"]
gamedate = data["gamedate"]
events = data["events"]
rows = []
for event in events:
    eventid = event["eventId"]
    visitor = event["visitor"]
    visitor_name = visitor["name"]
    visitor_teamid = visitor["teamid"]
    visitor_abbreviation = visitor["abbreviation"]
    home = event["home"]
    home_name = home["name"]
    home_teamid = home["teamid"]
    home_abbreviation = home["abbreviation"]
    moments = event["moments"]
    for moment in moments:
        gameperiod = moment[0]
        timestamp = moment[1]
        seconds = moment[2]
        shotclock = moment[3]
        coordinates = moment[5]
        for coord in coordinates:
            teamid = coord[0]
            playerid = coord[1]
            x = coord[2]
            y = coord[3]
            z = coord[4]
            rows.append([gameid, gamedate, eventid, visitor_name, visitor_teamid, 
                         visitor_abbreviation, home_name, home_teamid, home_abbreviation, 
                         gameperiod, timestamp, seconds, shotclock, teamid, playerid, x, y, z])

# Create the DataFrame
df = pd.DataFrame(rows, columns=["gameid", "gamedate", "eventid", "visitor_name", 
                                 "visitor_teamid", "visitor_abbreviation", "home_name", 
                                 "home_teamid", "home_abbreviation", "gameperiod", 
                                 "timestamp", "seconds", "shotclock", "teamid", 
                                 "playerid", "x", "y", "z"])


#This is to grab records where the ball crossed half-court
#Assuming x is the length of the court and x=50 is half-court
df_temp = df[df['playerid'] == -1]
df_temp = df_temp[['timestamp','seconds','playerid', 'x', 'y', 'z']]
df_half = df_temp.sort_values(by=['seconds'], ascending=False)
new_df = pd.DataFrame(columns=df_half.columns)
for current_row, next_row in zip(df_half.iterrows(), df_half.iloc[1:].iterrows()):
    current_x = current_row[1]["x"]
    next_x = next_row[1]["x"]
    if (current_x > 50 and next_x < 50) or (current_x < 50 and next_x > 50):
        new_df = new_df.append(current_row[1])
new_df.to_json('half-court.json', orient='records', lines=True)

#Sum of all the players location based on timestamp
df_sum = df.groupby(["timestamp"], as_index=False)[["x","y","z"]].sum()
df_sum.to_json('sum-location.json', orient='records', lines=True)
#print(df_sum)

