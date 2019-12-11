from pymongo import MongoClient
from pymongo import errors
from datetime import date
import datetime

class SurveillanceDbCreator:
    def __init__(self):
        self.conn = MongoClient()
        self.db = self.conn.SurveillanceDb
        self.collection = self.db.users
    
    def add_new_user(self, name,landmarks):

        line_to_insert = {
                "name": name,
                "landmarks": landmarks,
                "create_date": datetime.datetime.today(),
                "commands": []
            }
        try:
            self.collection.insert_one(line_to_insert)
        except Exception as e:
            print(e)  

    def user_exists_by_landmarks(self,landmarks):
        try:
            return self.collection.find({"landmarks": landmarks}).count() > 0
        except Exception as e:
            print(e)  
            #return False
        

    def get_user_by_landmarks(self, landmarks):
        try:
            #print(landmarks)
            return self.collection.find({"landmarks": landmarks})[0]
        except Exception as e:
            print(e)
            return None
        
    def get_all_users(self):
        return self.collection.find({})

    def get_users_by_landmarks(self, landmarks_list):
        users = []
        for landmarks in enumerate(landmarks_list):
            user = self.get_users_by_landmarks(landmarks)
            if user == None: 
                continue
            users.append(user)
        return users


#surveillance = SurveillanceDbCreator()
#surveillance.add_new_user("junior", "[[286, 261], [284, 283], [284, 306], [287, 327], [292, 348], [302, 369], [315, 385], [332, 395], [354, 398], [377, 396], [399, 387], [419, 373], [433, 356], [442, 336], [447, 314], [450, 292], [451, 271], [296, 249], [305, 239], [321, 238], [335, 241], [349, 248], [371, 248], [385, 242], [402, 239], [418, 242], [429, 250], [359, 266], [357, 282], [355, 298], [354, 314], [335, 322], [344, 325], [355, 328], [366, 325], [376, 322], [307, 266], [317, 261], [329, 262], [340, 269], [328, 271], [316, 271], [381, 269], [391, 261], [403, 261], [413, 266], [404, 270], [392, 271], [324, 348], [335, 344], [346, 342], [355, 343], [364, 341], [378, 343], [393, 347], [379, 356], [365, 360], [355, 361], [345, 361], [334, 356], [330, 348], [346, 350], [355, 351], [365, 350], [387, 348], [365, 349], [355, 350], [346, 349]]")