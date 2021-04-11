"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

ExploreData : This script contains functions to explore sensors and gestures data, in order to select users with specific characteristics.
"""
########################################
# Imports
########################################
import os
import ujson as json
import pandas as pd
from utils.MongoDBHandler import MongoDBHandler
from utils.DBDataHandler import DBDataHandler
from bson.objectid import ObjectId
import numpy as np


########################################
# Initialize Functions
########################################
#--------------------------------------------------
# findUsers_Sensors : Find users with 'valid' sensors (accelerometer, gyroscope) data
# SensData_Path - The full path of json files directory
# ScreenName - The type of screen
# Synced_Sensors - If True then select accelerometer and gyroscope data that occured at the same time 
# minTmStData - A timestamp (.json file) must have at least minTmStData number of data to be accepted
# minUserData - A user must have at least minUserData number of data to be accepted
#--------------------------------------------------
def findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minTmStData, minUserData):
    # List *.json files
    jsonFiles = [pos_json for pos_json in os.listdir(SensData_Path) if pos_json.endswith('.json')]
    
    # List all users with sensors data
    Users = []
    for jsonFile in jsonFiles:
        jsonFile = jsonFile.replace('.json','')
        User = jsonFile.split('_')[0]
        if User not in Users:
            Users.append(User)
            
    # List only users with valid sensors data
    valUsers = pd.DataFrame(columns= ['User', 'Num_Of_AccData', 'Num_Of_GyrData', 'List_Of_TimeStamps', 'AccGyrSizes_Of_TimeStamps'])
        
    for User in Users:
        Num_Of_AccData = 0
        Num_Of_GyrData = 0
        List_Of_TimeStamps = []
        AccGyrSizes_Of_TimeStamps = []
            
        jsonFiles = [pos_json for pos_json in os.listdir(SensData_Path) if (pos_json.startswith(User) & pos_json.endswith('.json'))]
        for js in jsonFiles:
            AccSize = 0
            GyrSize = 0           
            
            with open(SensData_Path + "\\" + js) as jsonFile:
                json_text = json.load(jsonFile)
                js = js.replace('.json','')
                timestamp = float(js.split('_')[1])
                
                for i in json_text['accelerometer']:
                    if ScreenName in i['screen']:
                        x = i['x']
                        y = i['y'] 
                        if x == 0 and y == 0:
                            continue
                        AccSize = AccSize + 1
                        
                for i in json_text['gyroscope']:
                    if ScreenName in i['screen']:
                        x = i['x']
                        y = i['y'] 
                        if x == 0 and y == 0:
                            continue
                        GyrSize = GyrSize + 1
                        
                if Synced_Sensors:
                    if AccSize > GyrSize:
                        AccSize = GyrSize
                    if AccSize < GyrSize:
                        GyrSize = AccSize
                
                if (AccSize >= minTmStData) or (GyrSize >= minTmStData):
                    List_Of_TimeStamps.append(timestamp)
                    AccGyrSizes_Of_TimeStamps.append([AccSize, GyrSize])                      
                    Num_Of_AccData = Num_Of_AccData + AccSize    
                    Num_Of_GyrData = Num_Of_GyrData + GyrSize 
                                                 
        if (Num_Of_AccData >= minUserData) and (Num_Of_GyrData >= minUserData):
            valUser = {'User': User, 'Num_Of_AccData': Num_Of_AccData, 'Num_Of_GyrData': Num_Of_GyrData, 'List_Of_TimeStamps': List_Of_TimeStamps, 'AccGyrSizes_Of_TimeStamps': AccGyrSizes_Of_TimeStamps}
            valUsers = valUsers.append(valUser, ignore_index=True)
            
    return valUsers, Synced_Sensors


#--------------------------------------------------
# findUsers_Swipes : Find users with 'valid' swipes
# GestData_DBName - The dabase name in the mongoDB localhost:27017
# ScreenName - The type of screen
# maxDeviceWidth
# maxDeviceHeight
# Fake_Swipe_Limit - If Gesture_Time < Fake_Swipe_Limit the swipe is fake
# minGestData, maxGestData - Select gestures with minGestData <= len(gesture["data"]) <= maxGestData
# minUserGest - A user must have at least minUserGest number of valid gestures to be accepted
#--------------------------------------------------
def findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minGestData, maxGestData, minUserGest):
    # Get data
    m = MongoDBHandler('mongodb://localhost:27017/', GestData_DBName)
    d = DBDataHandler(m)
    
    # List only users with valid gestures data
    valUsers = pd.DataFrame(columns= ['User', 'Num_Of_Gestures', 'Gestures_IDs', 'NumData_Of_Gestures', 'tStartStop_Of_Gestures'])
        
    Users = d.get_users()
    for User in Users:
        if("xp" in User):
            # Remove usernames with problems
            if((User["xp"]>1)and("deth" not in User["username"])and("Marpap" not in User["username"])and("Johnys" not in User["username"])and("Tenebrific" not in User["username"])and("Sherlocked" not in User["username"])and("kavouras" not in User["username"])):
                Num_Of_Gestures = 0
                Gestures_IDs = []
                NumData_Of_Gestures = []
                tStartStop_Of_Gestures = []
                    
                User_id = User["_id"]
                Devices = d.get_devices({'user_id':ObjectId(User_id)})               
                for Device in Devices:
                    # Remove kiosk device and devices with big dimensions (not mobile phones)
                    if(("TouchScreen" not in Device["device_id"])and(Device["width"]<maxDeviceWidth)and(Device["height"]<maxDeviceHeight)):
                        Device_id = Device["device_id"]
                        Gestures = d.get_gestures_from_device(Device_id)
                        for Gesture in Gestures:
                            if (Gesture["type"] == 'swipe'):
                                if (ScreenName in Gesture["screen"]):
                                    if ((Gesture["t_start"] == -1) or ( Gesture["t_stop"] == -1)):
                                        continue
                                    Gesture_Time = Gesture["t_stop"] - Gesture["t_start"]
                                    if (Gesture_Time < 0):
                                        continue
                                    if (Gesture_Time < Fake_Swipe_Limit):
                                        continue                                    
                                    if (minGestData <= len(Gesture["data"]) <= maxGestData):
                                        Num_Of_Gestures = Num_Of_Gestures + 1
                                        Gestures_IDs.append(Gesture["_id"])
                                        NumData_Of_Gestures.append(len(Gesture["data"]))
                                        tStartStop_Of_Gestures.append([Gesture["t_start"], Gesture["t_stop"]])
                                    
                if (Num_Of_Gestures >= minUserGest):
                    valUser = {'User': User["player_id"], 'Num_Of_Gestures': Num_Of_Gestures, 'Gestures_IDs': Gestures_IDs, 'NumData_Of_Gestures': NumData_Of_Gestures, 'tStartStop_Of_Gestures': tStartStop_Of_Gestures}
                    valUsers = valUsers.append(valUser, ignore_index=True)
                    
    return valUsers


#--------------------------------------------------
# findUsers_Common : Find users with 'valid' sensors and swipes data
# Users_Sens - Users with 'valid' sensors data
# Users_Gest - Users with 'valid' gestures data
# Synced_Common - If True find sensors and gestures data of common time
# minSensData, minGest - A use users must have at least minSensData number of sensros data and at least minGest number of valid gestures to be accepted
#--------------------------------------------------
def findUsers_Common(Users_Sensors, Synced_Sensors, Users_Swipes, Synced_Common, minSensData, minGest):

    if Synced_Common:
        if not(Synced_Sensors):
            raise ValueError('syncSensorsGesturesData is True but isSensorsDataSynced is False')
            
    # List common users
    Users_Common = list(np.intersect1d(Users_Sensors["User"], Users_Swipes["User"]))
    
    # List users with valid sensors and gestures data
    valUsers = pd.DataFrame(columns= ['User', 'Num_Of_AccData', 'Num_Of_GyrData', 'List_Of_TimeStamps', 'AccGyrSizes_Of_TimeStamps', 'Num_Of_Gestures', 'Gestures_IDs', 'NumData_Of_Gestures', 'tStartStop_Of_Gestures'])
        
    for User in Users_Common:
        Num_Of_AccData = Users_Sensors.loc[Users_Sensors['User'] == User]["Num_Of_AccData"].values[0]
        Num_Of_GyrData = Users_Sensors.loc[Users_Sensors['User'] == User]["Num_Of_GyrData"].values[0]
        
        List_Of_TimeStamps = Users_Sensors.loc[Users_Sensors['User'] == User]["List_Of_TimeStamps"].values[0]
        AccGyrSizes_Of_TimeStamps = Users_Sensors.loc[Users_Sensors['User'] == User]["AccGyrSizes_Of_TimeStamps"].values[0]
        
        Num_Of_Gestures = Users_Swipes.loc[Users_Swipes['User'] == User]["Num_Of_Gestures"].values[0]
        Gestures_IDs = Users_Swipes.loc[Users_Swipes['User'] == User]["Gestures_IDs"].values[0]
        NumData_Of_Gestures = Users_Swipes.loc[Users_Swipes['User'] == User]["NumData_Of_Gestures"].values[0]
        tStartStop_Of_Gestures = Users_Swipes.loc[Users_Swipes['User'] == User]["tStartStop_Of_Gestures"].values[0]
        
        if Synced_Common:    
            new_Num_Of_AccData = 0
            new_Num_Of_GyrData = 0
            
            new_List_Of_TimeStamps = []
            new_AccGyrSizes_Of_TimeStamps = []
            
            new_Num_Of_Gestures = 0
            new_Gestures_IDs = []
            new_NumData_Of_Gestures = []
            new_tStartStop_Of_Gestures = []                               
            
            # Can a timestap appear in more than one gesture ? -> I think No
            # Can a gestures hold more than one timestamp ? -> I think Yes
            for i in range(Num_Of_Gestures):                
                hasTimeStamps = False
                
                for j in range(len(List_Of_TimeStamps)):
                    if (tStartStop_Of_Gestures[i][0] <= List_Of_TimeStamps[j] <= tStartStop_Of_Gestures[i][1]):
                        hasTimeStamps = True
                                                
                        new_Num_Of_AccData = new_Num_Of_AccData + AccGyrSizes_Of_TimeStamps[j][0]
                        new_Num_Of_GyrData = new_Num_Of_GyrData + AccGyrSizes_Of_TimeStamps[j][1]
                       
                        new_List_Of_TimeStamps.append(List_Of_TimeStamps[j])
                        new_AccGyrSizes_Of_TimeStamps.append(AccGyrSizes_Of_TimeStamps[j])
                        
                if hasTimeStamps:                    
                    new_Num_Of_Gestures = new_Num_Of_Gestures + 1
                    new_Gestures_IDs.append(Gestures_IDs[i])
                    new_NumData_Of_Gestures.append(NumData_Of_Gestures[i])
                    new_tStartStop_Of_Gestures.append(tStartStop_Of_Gestures[i])
                    
            Num_Of_AccData = new_Num_Of_AccData                        
            Num_Of_GyrData = new_Num_Of_GyrData
            List_Of_TimeStamps = new_List_Of_TimeStamps
            AccGyrSizes_Of_TimeStamps = new_AccGyrSizes_Of_TimeStamps
            Num_Of_Gestures = new_Num_Of_Gestures
            Gestures_IDs = new_Gestures_IDs
            NumData_Of_Gestures = new_NumData_Of_Gestures
            tStartStop_Of_Gestures = new_tStartStop_Of_Gestures
            
        # Add user
        if (minSensData <= Num_Of_AccData) and (minSensData <= Num_Of_GyrData) and (minGest <= Num_Of_Gestures):
            valUser = {'User': User, 'Num_Of_AccData': Num_Of_AccData, 'Num_Of_GyrData': Num_Of_GyrData, 'List_Of_TimeStamps': List_Of_TimeStamps, 'AccGyrSizes_Of_TimeStamps': AccGyrSizes_Of_TimeStamps, 'Num_Of_Gestures': Num_Of_Gestures, 'Gestures_IDs': Gestures_IDs, 'NumData_Of_Gestures': NumData_Of_Gestures, 'tStartStop_Of_Gestures': tStartStop_Of_Gestures}
            valUsers = valUsers.append(valUser, ignore_index=True)
        
    return valUsers, Synced_Common

