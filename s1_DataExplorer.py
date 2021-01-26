"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

DataExplorer : This script contains functions to explore sensors and gestures data, in order to select users with specific characteristics.
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
# findUsers_SensorsData : Find users with valid sensors data
# SensorsData_Path - The full path of json files directory
# ScreenName - The type of screen
# If syncSensorsData is True then select accelerometer and gyroscope data that occured at the same time 
# Select users with minSensorsData <= AccelerometerData_size, GyroscopeData_size <= maxSensorsData
#--------------------------------------------------
def findUsers_SensorsData(SensorsData_Path, ScreenName, syncSensorsData, minSensorsData, maxSensorsData):
    # List *.json files
    jsonFiles = [pos_json for pos_json in os.listdir(SensorsData_Path) if pos_json.endswith('.json')]
    
    # List all users with sensors data
    users = []
    for jsonFile in jsonFiles:
        jsonFile = jsonFile.replace('.json','')
        user = jsonFile.split('_')[0]
        if user not in users:
            users.append(user)
            
    # List only users with valid sensors data
    valUsers = pd.DataFrame(columns= ['User', 'Num_Of_AccelerometerData', 'Num_Of_GyroscopeData', 'List_Of_TimeStamps', 'AccGyrSizes_Of_TimeStamps'])
        
    for user in users:
        Num_Of_AccelerometerData = 0
        Num_Of_GyroscopeData = 0
        List_Of_TimeStamps = []
        AccGyrSizes_Of_TimeStamps = []
            
        jsonFiles = [pos_json for pos_json in os.listdir(SensorsData_Path) if (pos_json.startswith(user) & pos_json.endswith('.json'))]
        for js in jsonFiles:
            accSize = 0
            gyrSize = 0           
            
            with open(SensorsData_Path + "\\" + js) as jsonFile:
                json_text = json.load(jsonFile)
                js = js.replace('.json','')
                timestamp = float(js.split('_')[1])
                
                for i in json_text['accelerometer']:
                    if ScreenName in i['screen']:
                        x = i['x']
                        y = i['y'] 
                        if x == 0 and y == 0:
                            continue
                        accSize = accSize + 1
                        
                for i in json_text['gyroscope']:
                    if ScreenName in i['screen']:
                        x = i['x']
                        y = i['y'] 
                        if x == 0 and y == 0:
                            continue
                        gyrSize = gyrSize + 1
                        
                if syncSensorsData:
                    if accSize > gyrSize:
                        accSize = gyrSize
                    if accSize < gyrSize:
                        gyrSize = accSize
                
                if (accSize != 0) or (gyrSize != 0):
                    List_Of_TimeStamps.append(timestamp)
                    AccGyrSizes_Of_TimeStamps.append([accSize, gyrSize])                      
                    Num_Of_AccelerometerData = Num_Of_AccelerometerData + accSize    
                    Num_Of_GyroscopeData = Num_Of_GyroscopeData + gyrSize 
                                                 
        if (minSensorsData <= Num_Of_AccelerometerData <= maxSensorsData) and (minSensorsData <= Num_Of_GyroscopeData <= maxSensorsData):
            valUser = {'User': user, 'Num_Of_AccelerometerData': Num_Of_AccelerometerData, 'Num_Of_GyroscopeData': Num_Of_GyroscopeData, 'List_Of_TimeStamps': List_Of_TimeStamps, 'AccGyrSizes_Of_TimeStamps': AccGyrSizes_Of_TimeStamps}
            valUsers = valUsers.append(valUser, ignore_index=True)
            
    return valUsers, syncSensorsData


#--------------------------------------------------
# findUsers_GesturesData : Find users with valid gestures data
# GesturesData_DatabaseName - The dabase name in the mongoDB localhost:27017
# GesturesType - swipe | tap
# ScreenName - The type of screen
# maxDeviceWidth
# maxDeviceHeight
# Select gestures with minGestureData <= len(gesture["data"]) <= maxGestureData
# Select users with minGestures <= Gestures_size <= maxGestures
#--------------------------------------------------
def findUsers_GesturesData(GesturesData_DatabaseName, GesturesType, ScreenName, maxDeviceWidth, maxDeviceHeight, minGestureData, maxGestureData, minGestures, maxGestures):
    # Get data
    m = MongoDBHandler('mongodb://localhost:27017/', GesturesData_DatabaseName)
    d = DBDataHandler(m)
    
    # List only users with valid gestures data
    valUsers = pd.DataFrame(columns= ['User', 'Num_Of_Gestures', 'Gestures_IDs', 'NumData_Of_Gestures', 'tStartStop_Of_Gestures'])
        
    users = d.get_users()
    for user in users:
        if("xp" in user):
            # Remove usernames with problems
            if((user["xp"]>1)and("deth" not in user["username"])and("Marpap" not in user["username"])and("Johnys" not in user["username"])and("Tenebrific" not in user["username"])and("Sherlocked" not in user["username"])and("kavouras" not in user["username"])):
                Num_Of_Gestures = 0
                Gestures_IDs = []
                NumData_Of_Gestures = []
                tStartStop_Of_Gestures = []
                    
                user_id = user["_id"]
                devices = d.get_devices({'user_id':ObjectId(user_id)})               
                for device in devices:
                    # Remove kiosk device and devices with big dimensions (not mobile phones)
                    if(("TouchScreen" not in device["device_id"])and(device["width"]<maxDeviceWidth)and(device["height"]<maxDeviceHeight)):
                        device_id = device["device_id"]
                        gestures = d.get_gestures_from_device(device_id)
                        for gesture in gestures:
                            if (gesture["type"] == GesturesType):
                                if (ScreenName in gesture["screen"]):
                                   if (minGestureData <= len(gesture["data"]) <= maxGestureData):
                                       Num_Of_Gestures = Num_Of_Gestures + 1
                                       Gestures_IDs.append(gesture["_id"])
                                       NumData_Of_Gestures.append(len(gesture["data"]))
                                       tStartStop_Of_Gestures.append([gesture["t_start"], gesture["t_stop"]])
                                    
                if (minGestures <= Num_Of_Gestures <= maxGestures):
                    valUser = {'User': user["player_id"], 'Num_Of_Gestures': Num_Of_Gestures, 'Gestures_IDs': Gestures_IDs, 'NumData_Of_Gestures': NumData_Of_Gestures, 'tStartStop_Of_Gestures': tStartStop_Of_Gestures}
                    valUsers = valUsers.append(valUser, ignore_index=True)
                    
    return valUsers


#--------------------------------------------------
# findUsers : Find users with valid sensors and gestures data
# valUsers_sensors - Users with valid sensors data
# valUsers_gestures - Users with valid gestures data
# If syncSensorsGesturesData is True find sensors and gestures data of common time
# Select users with (minSensorsData <= AccelerometerData_size <= maxSensorsData) and (minSensorsData <= GyroscopeData_size <= maxSensorsData) and (minGestures <= Gestures_size <= maxGestures)
#--------------------------------------------------
def findUsers_SGdata(valUsers_S, isSensorsDataSynced, valUsers_G, syncSensorsGesturesData, minSensorsData, maxSensorsData, minGestures, maxGestures):

    if syncSensorsGesturesData:
        if not(isSensorsDataSynced):
            raise ValueError('syncSensorsGesturesData is True but isSensorsDataSynced is False')
            
    # List common users
    common_users = list(np.intersect1d(valUsers_S["User"], valUsers_G["User"]))
    
    # List users with valid sensors and gestures data
    valUsers = pd.DataFrame(columns= ['User', 'Num_Of_AccelerometerData', 'Num_Of_GyroscopeData', 'List_Of_TimeStamps', 'AccGyrSizes_Of_TimeStamps', 'Num_Of_Gestures', 'Gestures_IDs', 'NumData_Of_Gestures', 'tStartStop_Of_Gestures'])
    if syncSensorsGesturesData:
        valUsers = pd.DataFrame(columns= ['User', 'Num_Of_AccelerometerData', 'Num_Of_GyroscopeData', 'Num_Of_Gestures', 'Gestures_IDs', 'NumData_Of_Gestures', 'tStartStop_Of_Gestures', 'List_Of_TimeStamps_per_Gesture', 'AccGyrSizes_Of_TimeStamps_per_Gesture'])
        
    for user in common_users:
        Num_Of_AccelerometerData = valUsers_S.loc[valUsers_S['User'] == user]["Num_Of_AccelerometerData"].values[0]
        Num_Of_GyroscopeData = valUsers_S.loc[valUsers_S['User'] == user]["Num_Of_GyroscopeData"].values[0]
        
        List_Of_TimeStamps = valUsers_S.loc[valUsers_S['User'] == user]["List_Of_TimeStamps"].values[0]
        AccGyrSizes_Of_TimeStamps = valUsers_S.loc[valUsers_S['User'] == user]["AccGyrSizes_Of_TimeStamps"].values[0]
        
        Num_Of_Gestures = valUsers_G.loc[valUsers_G['User'] == user]["Num_Of_Gestures"].values[0]
        Gestures_IDs = valUsers_G.loc[valUsers_G['User'] == user]["Gestures_IDs"].values[0]
        NumData_Of_Gestures = valUsers_G.loc[valUsers_G['User'] == user]["NumData_Of_Gestures"].values[0]
        tStartStop_Of_Gestures = valUsers_G.loc[valUsers_G['User'] == user]["tStartStop_Of_Gestures"].values[0]
        
        if syncSensorsGesturesData:    
            new_Num_Of_AccelerometerData = 0
            new_Num_Of_GyroscopeData = 0
            
            List_Of_TimeStamps_per_Gesture = []
            AccGyrSizes_Of_TimeStamps_per_Gesture = []
            
            new_Num_Of_Gestures = 0
            new_Gestures_IDs = []
            new_NumData_Of_Gestures = []
            new_tStartStop_Of_Gestures = []                               
            
            # Can a timestap appear in more than one gesture ? -> I think No
            # Can a gestures hold more than one timestamp ? -> I think Yes
            for i in range(Num_Of_Gestures):
                g_List_Of_TS = []
                g_AccGyr_Of_TS = []
                
                hasTimeStamps = False
                for j in range(len(List_Of_TimeStamps)):
                    if (tStartStop_Of_Gestures[i][0] <= List_Of_TimeStamps[j] <= tStartStop_Of_Gestures[i][1]):
                        hasTimeStamps = True
                                                
                        new_Num_Of_AccelerometerData = new_Num_Of_AccelerometerData + AccGyrSizes_Of_TimeStamps[j][0]
                        new_Num_Of_GyroscopeData = new_Num_Of_GyroscopeData + AccGyrSizes_Of_TimeStamps[j][1]
                        
                        g_List_Of_TS.append(List_Of_TimeStamps[j])
                        g_AccGyr_Of_TS.append(AccGyrSizes_Of_TimeStamps[j])
                        
                if hasTimeStamps:                    
                    new_Num_Of_Gestures = new_Num_Of_Gestures + 1
                    new_Gestures_IDs.append(Gestures_IDs[i])
                    new_NumData_Of_Gestures.append(NumData_Of_Gestures[i])
                    new_tStartStop_Of_Gestures.append(tStartStop_Of_Gestures[i])
                    List_Of_TimeStamps_per_Gesture.append(g_List_Of_TS)
                    AccGyrSizes_Of_TimeStamps_per_Gesture.append(g_AccGyr_Of_TS)
                    
            Num_Of_AccelerometerData = new_Num_Of_AccelerometerData                        
            Num_Of_GyroscopeData = new_Num_Of_GyroscopeData 
            Num_Of_Gestures = new_Num_Of_Gestures
            Gestures_IDs = new_Gestures_IDs
            NumData_Of_Gestures = new_NumData_Of_Gestures
            tStartStop_Of_Gestures = new_tStartStop_Of_Gestures
            
        # Add user
        if (minSensorsData <= Num_Of_AccelerometerData <= maxSensorsData) and (minSensorsData <= Num_Of_GyroscopeData <= maxSensorsData) and (minGestures <= Num_Of_Gestures <= maxGestures):
            valUser = {'User': user, 'Num_Of_AccelerometerData': Num_Of_AccelerometerData, 'Num_Of_GyroscopeData': Num_Of_GyroscopeData, 'List_Of_TimeStamps': List_Of_TimeStamps, 'AccGyrSizes_Of_TimeStamps': AccGyrSizes_Of_TimeStamps, 'Num_Of_Gestures': Num_Of_Gestures, 'Gestures_IDs': Gestures_IDs, 'NumData_Of_Gestures': NumData_Of_Gestures, 'tStartStop_Of_Gestures': tStartStop_Of_Gestures}
            if syncSensorsGesturesData:
                valUser = {'User': user, 'Num_Of_AccelerometerData': Num_Of_AccelerometerData, 'Num_Of_GyroscopeData': Num_Of_GyroscopeData, 'Num_Of_Gestures': Num_Of_Gestures, 'Gestures_IDs': Gestures_IDs, 'NumData_Of_Gestures': NumData_Of_Gestures, 'tStartStop_Of_Gestures': tStartStop_Of_Gestures, 'List_Of_TimeStamps_per_Gesture': List_Of_TimeStamps_per_Gesture, 'AccGyrSizes_Of_TimeStamps_per_Gesture': AccGyrSizes_Of_TimeStamps_per_Gesture}                
            valUsers = valUsers.append(valUser, ignore_index=True)
        
    return valUsers, syncSensorsGesturesData
