from bson.objectid import ObjectId
from flask_pymongo import PyMongo

class StudentManager:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def get_student_by_id(self, id):
        student = self.mongo_client.db.students.find_one({'_id': ObjectId(id)})
        return student
    
    def get_student_by_mobile_number(self, mobile_number):
        student = self.mongo_client.db.students.find_one({'mobile_number': mobile_number})
        return student