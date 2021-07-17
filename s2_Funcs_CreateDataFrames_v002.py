#################
#    IMPORTS    #
#################
import os
import numpy as np
import pandas as pd
import ujson as json
from tqdm import tqdm
from bson.objectid import ObjectId
from s0_Funcs_Util_v000 import MongoDBHandler, DBDataHandler


##############################
#    INITIALIZE FUNCTIONS    #
##############################
# ============================================================================================================
#
# ============================================================================================================
def Create_DF_Sensors(SensData_Path, DF_Users):
    DF_Acc = pd.DataFrame(columns= ['User', 'TS', 'Screen', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle'])
    DF_Gyr = pd.DataFrame(columns= ['User', 'TS', 'Screen', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle'])
    
    Users = list(DF_Users['User'])
    for User in tqdm(Users, desc = '-> Creating Sensors Data Frames'):
        List_Of_TS = DF_Users.loc[DF_Users['User'] == User]['List_Of_TS'].values[0]
        S_Of_TSs = DF_Users.loc[DF_Users['User'] == User]['S_Of_TSs'].values[0]
        AccGyrSize_Of_S_Of_TSs = DF_Users.loc[DF_Users['User'] == User]['AccGyrSize_Of_S_Of_TSs'].values[0]
        
        for i in range(len(List_Of_TS)):
            TS = str(int(List_Of_TS[i]))
            
            with open(os.path.join(SensData_Path, User + '_' + TS + '.json')) as jsonFile:
                json_text = json.load(jsonFile)
                
                for k in range(len(S_Of_TSs[i])):
                    ScreenName = S_Of_TSs[i][k]
                    AccSize_S = 0
                    GyrSize_S = 0
                    
                    for j in json_text['accelerometer']:
                        if ScreenName in j['screen']:
                            Screen = j['screen']
                            X = j['x']
                            Y = j['y']
                            Z = j['z']
                            if X == 0 and Y == 0:
                                continue
                            Magnitude = np.sqrt(X**2 + Y**2 + Z**2)
                            Combine_Angle = np.sqrt(Y**2 + Z**2)
                            df = {'User': User, 'TS': List_Of_TS[i], 'Screen': Screen, 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle}
                            DF_Acc = DF_Acc.append(df, ignore_index=True)
                            AccSize_S = AccSize_S + 1
                            if AccSize_S >= AccGyrSize_Of_S_Of_TSs[i][k][0]:
                                break
                            
                    for j in json_text['gyroscope']:
                        if ScreenName in j['screen']:
                            Screen = j['screen']
                            X = j['x']
                            Y = j['y']
                            Z = j['z']
                            if X == 0 and Y == 0:
                                continue
                            Magnitude = np.sqrt(X**2 + Y**2 + Z**2)
                            Combine_Angle = np.sqrt(Y**2 + Z**2)
                            df = {'User': User, 'TS': List_Of_TS[i], 'Screen': Screen, 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle}
                            DF_Gyr = DF_Gyr.append(df, ignore_index=True)
                            GyrSize_S = GyrSize_S + 1
                            if GyrSize_S >= AccGyrSize_Of_S_Of_TSs[i][k][1]:
                                break  
                        
    print('-> Creating Sensors Data Frames Finished')
                        
    return DF_Acc, DF_Gyr      


# ============================================================================================================
# Create_DF_Gestures : Create data frames for gestures data
# GestData_DBName - The dabase name in the mongoDB localhost:27017
# DF_Users - A data frame that must have the shape of findUsers_Common function result in s1_Funcs_ExploreData
# ============================================================================================================
def Create_DF_Gestures(GestData_DBName, DF_Users):
    DF_Gest = pd.DataFrame(columns= ['User', 'Screen', 'G_ID', 'G_Type', 'G_tStart', 'G_tStop', 'G_Duration', 'G_Data', 'D_Height', 'D_Width'])
    
    m = MongoDBHandler('mongodb://localhost:27017/', GestData_DBName)
    d = DBDataHandler(m)
    
    Users = list(DF_Users['User'])
    for User in tqdm(Users, desc = '-> Creating Gestures Frames'):
        G_IDs = DF_Users.loc[DF_Users['User'] == User]["Gestures_IDs"].values[0]
        
        for i in range(len(G_IDs)):
            G_ID = G_IDs[i]
            G = d.get_gestures({'_id':ObjectId(G_ID)})
            Screen = G[0]['screen']
            G_Type = G[0]['type']
            G_tStart = G[0]['t_start']
            G_tStop = G[0]['t_stop']
            G_Duration = G_tStop - G_tStart
            G_Data = G[0]['data']
            
            D_ID = G[0]['device_id']            
            D = d.get_devices({'device_id':D_ID})
            D_Height = D[0]['height']
            D_Width = D[0]['width']
            
            df = {'User': User, 'Screen': Screen, 'G_ID': G_ID, 'G_Type': G_Type, 'G_tStart': G_tStart, 'G_tStop': G_tStop, 'G_Duration': G_Duration, 'G_Data': G_Data, 'D_Height': D_Height, 'D_Width': D_Width}
            DF_Gest = DF_Gest.append(df, ignore_index=True)
                  
    print('-> Creating Gestures Frames Finished')
            
    return DF_Gest      