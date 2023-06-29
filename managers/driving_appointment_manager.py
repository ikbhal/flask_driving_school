from bson.objectid import ObjectId
from flask_pymongo import PyMongo

class DrivingAppointmentManager:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def list_appointments(self, student_id):
        appointments = self.mongo_client.db.appointments.find({'student_id': student_id})
        return list(appointments)

    def add_appointment(self, student_id, date, time_slot):
        appointment = {
            'student_id': student_id,
            'date': date,
            'time_slot': time_slot
        }
        self.mongo_client.db.appointments.insert_one(appointment)

    def delete_appointment(self, appointment_id):
        self.mongo_client.db.appointments.delete_one({'_id': ObjectId(appointment_id)})

    def edit_appointment(self, appointment_id, new_date, new_time_slot):
        self.mongo_client.db.appointments.update_one(
            {'_id': ObjectId(appointment_id)},
            {'$set': {'date': new_date, 'time_slot': new_time_slot}}
        )
