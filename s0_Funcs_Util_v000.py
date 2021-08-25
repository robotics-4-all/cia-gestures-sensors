"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Lab Group

Author : Christos Emmanouil
"""
# ============= #
#    Imports    #
# ============= #
import math
import numpy as np
from pymongo import MongoClient
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error, r2_score


# ========================= #
#    Functions & Classes    #
# ========================= #
class MongoDBHandler():

    def __init__(self, mongo_uri, db_name, timeout=5000):

        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=timeout)
            self.db = self.client.get_database(db_name)
            self.client.get_database(db_name).collection_names(include_system_collections=False)
        except Exception as e:
            print('Connection error: Timeout occurred, please check the mongo uri')
            raise
        # print('Connection to ' + mongo_uri + ' successful')

    def check_if_collection_exists(self, collection_name):

        collections = self.list_collections()
        if (collection_name in collections):
            return True

        return False

    def list_collections(self):

        collections = self.db.collection_names(include_system_collections=False)
        if (len(collections) == 0):
            print('WARNING: the selected db is empty')

        return collections

    def get_collection(self, collection_name, filter={}):

        if (self.check_if_collection_exists):
            results = []
            for document in self.db[collection_name].find(filter):
                results.append(document)
            return results
        else:
            return "Collection does not exist"

    def count_documents(self, collection_name, filter={}):

        if (self.check_if_collection_exists):
            return self.db[collection_name].count(filter)
        else:
            return "Collection does not exist"


class DBDataHandler():

    def __init__(self, MongoDBHandler):

        self.MongoDBHandler = MongoDBHandler

    def get_db_statistics(self):

        stats = {}
        for collection in self.MongoDBHandler.list_collections():
            stats[collection] = {}
            stats[collection]["number_of_docs"] = self.MongoDBHandler.count_documents(collection)

        return stats

    def get_users(self, filter={}):

        return self.MongoDBHandler.get_collection("users", filter)

    def get_gestures(self, filter={}):

        return self.MongoDBHandler.get_collection("gestures", filter)

    def get_devices(self, filter={}):

        return self.MongoDBHandler.get_collection("devices", filter)

    def get_user_from_device(self, device_id):

        device = self.get_devices({"device_id": device_id})
        if (len(device) > 0):
            user = self.get_users({"_id": device[0]["user_id"]})
            return user

        return "Device not found"

    def get_gestures_from_device(self, device_id):

        return self.get_gestures({"device_id": device_id})


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
    for i in range(0, len(x_pos)):
        dist = math.sqrt(pow(x_pos[i] - x_cent, 2) + pow(y_pos[i] - y_cent, 2))
        if (dist > maxim):
            maxim = dist
            ind = i

    xa = x_pos[ind]
    ya = y_pos[ind]
    if (xa == x_cent):
        A = 1
        B = 0
        C = -xa
    else:
        l = (ya - y_cent) / (xa - x_cent)
        A = l
        B = -1
        C = -l * x_cent + y_cent
    maxim = -1
    ind2 = -1

    for i in range(0, len(x_pos)):
        if (i == ind):
            continue
        dist = (np.abs(A * x_pos[i] + B * y_pos[i] + C)) / (math.sqrt(pow(A, 2) + pow(B, 2)))
        if (dist > maxim):
            dist = maxim
            ind2 = i

    big_axis = math.sqrt(pow(x_pos[ind] - x_cent, 2) + pow(y_pos[ind] - y_cent, 2))
    small_axis = math.sqrt(pow(x_pos[ind2] - x_cent, 2) + pow(y_pos[ind2] - y_cent, 2))
    tap_size = math.pi * big_axis * small_axis

    return tap_size


def frange(start, stop, step):

    i = start
    while (i < stop):
        yield i
        i += step
