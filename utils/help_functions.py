"""
This source code file contains a series of help functions that facilitate the calculation of 
the features
"""

import numpy as np
import math
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error, r2_score

def linear_regression(x_pos, y_pos):
    
    x_train = np.array(x_pos).reshape(-1, 1)
    y_train = np.array(y_pos).reshape(-1, 1)
    
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(x_train, y_train)
    
    # Predict based on the constructed model
    pred = regr.predict(x_train)

    # Visualize linear regression
#     import matplotlib.pyplot as plt 
#     plt.scatter(x_train, y_train,  color='black')
#     plt.plot(x_train, pred, color='blue', linewidth=3)
#     plt.show()
    
    info = {}
    info["slope"] = regr.coef_[0][0]
    info["mean_squared_error"] = mean_squared_error(y_train, pred)
    info["mean_abs_error"] = mean_absolute_error(y_train, pred)
    info["median_abs_error"] = median_absolute_error(y_train, pred)
    info["coef_determination"] = r2_score(y_train, pred)
    
    return info

def calc_ellipse_area(x_pos, y_pos):
    
    x_cent = np.mean(x_pos)
    y_cent = np.mean(y_pos)
    maxim = -1
    ind = -1
    for i in range(0,len(x_pos)):
        dist = math.sqrt(pow(x_pos[i]-x_cent,2)+pow(y_pos[i]-y_cent,2))
        if(dist>maxim):
            maxim = dist
            ind = i
            
    xa = x_pos[ind]
    ya = y_pos[ind]
    if(xa==x_cent):
        A = 1
        B = 0
        C = -xa
    else:
        l = (ya-y_cent)/(xa-x_cent)
        A = l
        B = -1
        C = -l*x_cent+y_cent
    maxim = -1
    ind2 = -1
    
    for i in range(0,len(x_pos)):
        if(i==ind):
            continue
        dist = (np.abs(A*x_pos[i]+B*y_pos[i]+C))/(math.sqrt(pow(A,2)+pow(B,2)))
        if(dist>maxim):
            dist = maxim
            ind2 = i
            
    big_axis = math.sqrt(pow(x_pos[ind]-x_cent,2)+pow(y_pos[ind]-y_cent,2))
    small_axis = math.sqrt(pow(x_pos[ind2]-x_cent,2)+pow(y_pos[ind2]-y_cent,2))
    tap_size = math.pi*big_axis*small_axis
    
    return tap_size