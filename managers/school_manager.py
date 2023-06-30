from bson.objectid import ObjectId

class SchoolManager:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def get_school_by_id(self, id):
        school = self.mongo_client.db.schools.find_one({'_id': ObjectId(id)})
        return school
    
    def get_schools_by_city(self, city):
        school_list = self.mongo_client.db.schools.find_one({'city': city})
        return school_list
    
    def add_school(self, name, address, area, city, pincode, phone_number):
        school_collection = self.mongo_client.db.schools
        school_data = {
            'name': name,
            'address': address,
            'area': area,
            'city': city,
            'pincode': pincode,
            'phone_number': phone_number
        }
        school_collection.insert_one(school_data)
        return "School added successfully!"

    def update_school(self, school_id, name, address, area, city, pincode, phone_number):
        school_collection = self.mongo_client.db.schools
        school_data = {
            'name': name,
            'address': address,
            'area': area,
            'city': city,
            'pincode': pincode,
            'phone_number': phone_number
        }
        school_collection.update_one({'_id': ObjectId(school_id)}, {'$set': school_data})
        return "School updated successfully!"
    
    def delete_school(self, school_id):
        school_collection = self.mongo_client.db.schools
        school_collection.delete_one({'_id': ObjectId(school_id)})
        return "School deleted successfully!"
    
    #  school_list = school_manager.get_schools()
    def get_schools(self):
        school_collection = self.mongo_client.db.schools
        school_list = school_collection.find()
        return school_list