from pymongo import MongoClient
from pymongo import errors
from datetime import date

class SurveillanceDbCreator:
    def __init__(self):
        self.conn = MongoClient()
        self.db = self.conn.SurveillanceDb
        self.collection = self.db.users
    
    def add_new_user(self, name,landmarks):

        line_to_insert = {
                "name": name,
                "landmarks": landmarks,
                "create_date": date.today(),
                "commands": []
            }
        try:
            self.collection.insert_one(line_to_insert)
        except Exception as e:
            print(e)  

    def user_exists_by_landmarks(self,landmarks):
        return self.collection.find({"landmarks": landmarks}).count() > 0

    def get_user_by_landmarks(self, landmarks):
        return self.collection.find({"landmarks": landmarks})[0]

    def get_users_by_landmarks(self, landmarks_list):
        users = []
        for landmarks in enumerate(landmarks_list):
            user = self.get_users_by_landmarks(landmarks)
            if user == None: 
                continue
            users.append(user)
        return users


