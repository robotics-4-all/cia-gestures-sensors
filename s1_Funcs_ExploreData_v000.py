"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Lab Group

Author : Christos Emmanouil
"""
#  ============ #
#    Imports    #
# ============= #
import os
import numpy as np
import pandas as pd
import ujson as json
from tqdm import tqdm
from bson.objectid import ObjectId

from s0_Funcs_Util_v000 import MongoDBHandler, DBDataHandler


# =============== #
#    Functions    #
# =============== #
def findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minData_Screen, minData_TimeStamp, minData_User):
    """
    Find users with 'valid' sensors (accelerometer, gyroscope) data.
    There in the screen information.
    There is the option that sensors data in a screen must have the same size in both sensors or not.

    :param SensData_Path: json files directory
    :param ScreenName: Type of screen - game
    :param Synced_Sensors: If True, select accelerometer and gyroscope data that occurred at the same time
    :param minData_Screen: A screen must have a minimum number of data to be accepted
    :param minData_TimeStamp: A timestamp must have a minimum number of data to be accepted
    :param minData_User: A user must have a minimum number of data to be accepted
    :return: A dataframe with the valid users and their valid data, Synced_Sensors
    """

    # List *.json files
    jsonFiles = [pos_json for pos_json in os.listdir(SensData_Path) if pos_json.endswith('.json')]

    # List all users with sensors data
    Users = []
    for jsonFile in jsonFiles:
        jsonFile = jsonFile.replace('.json', '')
        User = jsonFile.split('_')[0]
        if User not in Users:
            Users.append(User)

    # List only users with valid sensors data
    valUsers = pd.DataFrame(columns=['User', 'AccSize_User', 'GyrSize_User', 'List_Of_TimeStamps',
                                     'Screens_Of_TimeStamps', 'AccGyrSize_Of_Screens_Of_Timestamps'])

    for User in tqdm(Users, desc='Searching for Users with Valid Sensors Data'):
        AccSize_User = 0
        GyrSize_User = 0
        List_Of_TimeStamps = []
        Screens_Of_TimeStamps = []
        AccGyrSize_Of_Screens_Of_Timestamps = []

        jsonFiles = [pos_json for pos_json in os.listdir(SensData_Path)
                     if (pos_json.startswith(User) & pos_json.endswith('.json'))]

        for js in jsonFiles:

            with open(SensData_Path + "\\" + js) as jsonFile:
                json_text = json.load(jsonFile)
                js = js.replace('.json', '')
                timestamp = float(js.split('_')[1])

                ScreensAcc = []
                for i in json_text['accelerometer']:
                    if ScreenName in i['screen']:
                        if i['screen'] not in ScreensAcc:
                            ScreensAcc.append(i['screen'])

                ScreensGyr = []
                for i in json_text['gyroscope']:
                    if ScreenName in i['screen']:
                        if i['screen'] not in ScreensGyr:
                            ScreensGyr.append(i['screen'])

                if Synced_Sensors:
                    Screens = list(set(ScreensAcc) & set(ScreensGyr))
                else:
                    Screens = list(set(ScreensAcc) | set(ScreensGyr))

                Screens_Of_TimeStamp = []
                AccGyrSize_Of_Screens_Of_Timestamp = []
                AccSize_TimeStamp = 0
                GyrSize_TimeStamp = 0

                for Screen in Screens:
                    AccSize_Screen = 0
                    GyrSize_Screen = 0

                    for i in json_text['accelerometer']:
                        if Screen == i['screen']:
                            x = i['x']
                            y = i['y']
                            if x == 0 and y == 0:
                                continue
                            AccSize_Screen = AccSize_Screen + 1

                    for i in json_text['gyroscope']:
                        if Screen == i['screen']:
                            x = i['x']
                            y = i['y']
                            if x == 0 and y == 0:
                                continue
                            GyrSize_Screen = GyrSize_Screen + 1

                    if Synced_Sensors:
                        if AccSize_Screen > GyrSize_Screen:
                            AccSize_Screen = GyrSize_Screen
                        if AccSize_Screen < GyrSize_Screen:
                            GyrSize_Screen = AccSize_Screen
                        if (AccSize_Screen >= minData_Screen) and (GyrSize_Screen >= minData_Screen):
                            Screens_Of_TimeStamp.append(Screen)
                            AccGyrSize_Of_Screens_Of_Timestamp.append([AccSize_Screen, GyrSize_Screen])
                            AccSize_TimeStamp = AccSize_TimeStamp + AccSize_Screen
                            GyrSize_TimeStamp = GyrSize_TimeStamp + GyrSize_Screen
                    else:
                        if (AccSize_Screen >= minData_Screen) or (GyrSize_Screen >= minData_Screen):
                            Screens_Of_TimeStamp.append(Screen)
                            AccGyrSize_Of_Screens_Of_Timestamp.append([AccSize_Screen, GyrSize_Screen])
                            AccSize_TimeStamp = AccSize_TimeStamp + AccSize_Screen
                            GyrSize_TimeStamp = GyrSize_TimeStamp + GyrSize_Screen

                if (AccSize_TimeStamp >= minData_TimeStamp) or (GyrSize_TimeStamp >= minData_TimeStamp):
                    List_Of_TimeStamps.append(timestamp)
                    Screens_Of_TimeStamps.append(Screens_Of_TimeStamp)
                    AccGyrSize_Of_Screens_Of_Timestamps.append(AccGyrSize_Of_Screens_Of_Timestamp)
                    AccSize_User = AccSize_User + AccSize_TimeStamp
                    GyrSize_User = GyrSize_User + GyrSize_TimeStamp

        if (AccSize_User >= minData_User) and (GyrSize_User >= minData_User):
            valUser = {'User': User, 'AccSize_User': AccSize_User, 'GyrSize_User': GyrSize_User,
                       'List_Of_TimeStamps': List_Of_TimeStamps, 'Screens_Of_TimeStamps': Screens_Of_TimeStamps,
                       'AccGyrSize_Of_Screens_Of_Timestamps': AccGyrSize_Of_Screens_Of_Timestamps}
            valUsers = valUsers.append(valUser, ignore_index=True)

    print('-> Exploring Sensors Data Finished:', len(valUsers), 'Users with Valid Sensors Data found')

    return valUsers, Synced_Sensors


def findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minData_Gesture,
                     maxData_Gesture, minGestures_User):
    """
    Find users with 'valid' swipes.

    :param GestData_DBName: Database name in the mongoDB localhost:27017
    :param ScreenName: Type of screen - game
    :param maxDeviceWidth: Devices with a maximum width are accepted
    :param maxDeviceHeight: Devices with a maximum height are accepted
    :param Fake_Swipe_Limit: If Gesture_Time < Fake_Swipe_Limit the swipe is fake
    :param minData_Gesture: A gesture must have a minimum number of data to be accepted
    :param maxData_Gesture: A gesture must have a maximum number of data to be accepted
    :param minGestures_User: A user must have a minimum number of gestures to be accepted
    :return: A dataframe with the valid users and their valid gestures data
    """

    # Get data
    m = MongoDBHandler('mongodb://localhost:27017/', GestData_DBName)
    d = DBDataHandler(m)

    # List only users with valid gestures data
    valUsers = pd.DataFrame(columns=['User', 'Num_Of_Gestures', 'Gestures_IDs', 'Screen_Of_Gestures',
                                     'tStartStop_Of_Gestures'])

    Users = d.get_users()
    for User in tqdm(Users, desc='Searching for Users with Valid Swipes'):
        if 'xp' in User:
            # Remove usernames with problems
            if((User['xp'] > 1) and ('deth' not in User['username']) and ('Marpap' not in User['username']) and
                    ('Johnys' not in User['username']) and ('Tenebrific' not in User['username']) and
                    ('Sherlocked' not in User['username']) and ('kavouras' not in User['username'])):

                Num_Of_Gestures = 0
                Gestures_IDs = []
                Screen_Of_Gestures = []
                tStartStop_Of_Gestures = []

                User_id = User['_id']
                Devices = d.get_devices({'user_id': ObjectId(User_id)})
                for Device in Devices:
                    # Remove kiosk device and devices with big dimensions (not mobile phones)
                    if(('TouchScreen' not in Device['device_id']) and (Device['width'] < maxDeviceWidth) and
                            (Device['height'] < maxDeviceHeight)):

                        Device_id = Device['device_id']
                        Gestures = d.get_gestures_from_device(Device_id)
                        for Gesture in Gestures:
                            if Gesture['type'] == 'swipe':
                                if ScreenName in Gesture['screen']:
                                    if (Gesture['t_start'] == -1) or (Gesture['t_stop'] == -1):
                                        continue
                                    Gesture_Time = Gesture['t_stop'] - Gesture['t_start']
                                    if Gesture_Time < 0:
                                        continue
                                    if Gesture_Time < Fake_Swipe_Limit:
                                        continue
                                    if minData_Gesture <= len(Gesture['data']) <= maxData_Gesture:
                                        Num_Of_Gestures = Num_Of_Gestures + 1
                                        Gestures_IDs.append(Gesture['_id'])
                                        Screen_Of_Gestures.append(Gesture['screen'])
                                        tStartStop_Of_Gestures.append([Gesture['t_start'], Gesture['t_stop']])

                if Num_Of_Gestures >= minGestures_User:
                    valUser = {'User': User['player_id'], 'Num_Of_Gestures': Num_Of_Gestures,
                               'Gestures_IDs': Gestures_IDs, 'Screen_Of_Gestures': Screen_Of_Gestures,
                               'tStartStop_Of_Gestures': tStartStop_Of_Gestures}
                    valUsers = valUsers.append(valUser, ignore_index=True)

    print('-> Exploring Swipes Finished:', len(valUsers), 'Users with Valid Swipes Data found')

    return valUsers


def findUsers_Common(Users_Sensors, Users_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest):
    """
    Find common users in Users_Sensors ans Users_Swipes dataframes and save their data in a new one.

    :param Users_Sensors: A dataframe with the valid users and their valid data
    :param Users_Swipes: A dataframe with the valid users and their valid gestures data
    :param Synced_Sensors_Gestures:  If True find sensors and gestures data that occurred at the same time
    :param minSensData: A user must have a minimum number of sensors data to be accepted
    :param maxSensData: A user must have a maximum number of sensors data to be accepted
    :param minGest: A user must have a minimum number of gestures to be accepted
    :param maxGest: A user must have a maximum number of gestures to be accepted
    :return: A dataframe with valid users and their valid sensors and gestures data, Synced_Sensors_Gestures
    """

    # List common users
    Users_Common = list(np.intersect1d(Users_Sensors['User'], Users_Swipes['User']))

    # List users with valid sensors and gestures data
    valUsers = pd.DataFrame(columns=['User', 'AccSize_User', 'GyrSize_User', 'List_Of_TimeStamps',
                                     'Screens_Of_TimeStamps', 'Num_Of_Gestures', 'Gestures_IDs', 'Screen_Of_Gestures',
                                     'tStartStop_Of_Gestures'])

    for User in tqdm(Users_Common, desc='Searching for Common Users'):
        AccSize_User = Users_Sensors.loc[Users_Sensors['User'] == User]['AccSize_User'].values[0]
        GyrSize_User = Users_Sensors.loc[Users_Sensors['User'] == User]['GyrSize_User'].values[0]
        List_Of_TimeStamps = Users_Sensors.loc[Users_Sensors['User'] == User]['List_Of_TimeStamps'].values[0]
        Screens_Of_TimeStamps = Users_Sensors.loc[Users_Sensors['User'] == User]['Screens_Of_TimeStamps'].values[0]
        AccGyrSize_Of_Screens_Of_Timestamps = \
            Users_Sensors.loc[Users_Sensors['User'] == User]['AccGyrSize_Of_Screens_Of_Timestamps'].values[0]

        Num_Of_Gestures = Users_Swipes.loc[Users_Swipes['User'] == User]['Num_Of_Gestures'].values[0]
        Gestures_IDs = Users_Swipes.loc[Users_Swipes['User'] == User]['Gestures_IDs'].values[0]
        Screen_Of_Gestures = Users_Swipes.loc[Users_Swipes['User'] == User]['Screen_Of_Gestures'].values[0]
        tStartStop_Of_Gestures = Users_Swipes.loc[Users_Swipes['User'] == User]['tStartStop_Of_Gestures'].values[0]

        if Synced_Sensors_Gestures:
            new_AccSize_User = 0
            new_GyrSize_User = 0
            new_List_Of_TimeStamps = []
            new_Screens_Of_TimeStamps = []

            new_Num_Of_Gestures = 0
            new_Gestures_IDs = []
            new_Screen_Of_Gestures = []
            new_tStartStop_Of_Gestures = []

            # Can a timestamp appear in more than one gesture ? -> I think No
            # Can a gestures hold more than one timestamp ? -> I think Yes
            for i in range(Num_Of_Gestures):
                Flag = False

                for j in range(len(List_Of_TimeStamps)):
                    Screens_Of_TimeStamp = []
                    if tStartStop_Of_Gestures[i][0] <= List_Of_TimeStamps[j] <= tStartStop_Of_Gestures[i][1]:
                        for k in range(len(Screens_Of_TimeStamps[j])):
                            if Screen_Of_Gestures[i] == Screens_Of_TimeStamps[j][k]:
                                Flag = True
                                new_AccSize_User = new_AccSize_User + AccGyrSize_Of_Screens_Of_Timestamps[j][k][0]
                                new_GyrSize_User = new_GyrSize_User + AccGyrSize_Of_Screens_Of_Timestamps[j][k][1]
                                Screens_Of_TimeStamp.append(Screens_Of_TimeStamps[j][k])
                                new_List_Of_TimeStamps.append(List_Of_TimeStamps[j])
                                new_Screens_Of_TimeStamps.append(Screens_Of_TimeStamp)

                if Flag:
                    new_Num_Of_Gestures = new_Num_Of_Gestures + 1
                    new_Gestures_IDs.append(Gestures_IDs[i])
                    new_Screen_Of_Gestures.append(Screen_Of_Gestures[i])
                    new_tStartStop_Of_Gestures.append(tStartStop_Of_Gestures[i])

            AccSize_User = new_AccSize_User
            GyrSize_User = new_GyrSize_User
            List_Of_TimeStamps = new_List_Of_TimeStamps
            Screens_Of_TimeStamps = new_Screens_Of_TimeStamps
            Num_Of_Gestures = new_Num_Of_Gestures
            Gestures_IDs = new_Gestures_IDs
            Screen_Of_Gestures = new_Screen_Of_Gestures
            tStartStop_Of_Gestures = new_tStartStop_Of_Gestures

        # Add user
        if ((minSensData <= AccSize_User <= maxSensData) and (minSensData <= GyrSize_User <= maxSensData) and
                (minGest <= Num_Of_Gestures <= maxGest)):

            valUser = {'User': User, 'AccSize_User': AccSize_User, 'GyrSize_User': GyrSize_User,
                       'List_Of_TimeStamps': List_Of_TimeStamps, 'Screens_Of_TimeStamps': Screens_Of_TimeStamps,
                       'Num_Of_Gestures': Num_Of_Gestures, 'Gestures_IDs': Gestures_IDs,
                       'Screen_Of_Gestures': Screen_Of_Gestures, 'tStartStop_Of_Gestures': tStartStop_Of_Gestures}
            valUsers = valUsers.append(valUser, ignore_index=True)

    print('-> Searching for Common Users Finished:', len(valUsers), 'Users with Valid Sensors Data & Swipes found')

    return valUsers, Synced_Sensors_Gestures