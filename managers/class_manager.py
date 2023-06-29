from bson.objectid import ObjectId
from flask_pymongo import PyMongo

class ClassManager:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def add_class(self, student_mobile_number, date, start_time, end_time):
        class_doc = {
            'student_mobile_number': student_mobile_number,
            'date': date,
            'start_time': start_time,
            'end_time': end_time
        }
        self.mongo_client.db.classes.insert_one(class_doc)


    def list_clasess(self, student_mobile_number):
        classes = self.mongo_client.db.classes.find({'student_mobile_number': student_mobile_number})
        return list(classes)