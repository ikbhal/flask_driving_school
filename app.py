# create flask object
# run flask object
# import flask object
# use mongodb to store data
# improt mongodb relavent module python
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# import uuid module
# import uuid

# create Student class with properties id ,name, mobile number
class Student:
    def __init__(self,  name, mobile_numer):
        # self.id = id
        self.name = name
        self.mobile_numer = mobile_numer

app = Flask(__name__)
app.secret_key = 'allah raji hojaye'

# create pymongo object, specify mongodb uri localhost:27017 skool database
# mongo_client = PyMongo(app)
mongo_client = PyMongo(app, uri="mongodb://localhost:27017/skool")

# access mongo db from client
# access student collection from mongo db
student_collection = mongo_client.db.students

@app.route('/')
def index():
    student_list = student_collection.find()
    print('student_list: ' , student_list)
    # for student in student_list:
    #     print('student: ' , student)

    return render_template('index.html', student_list=student_list)

# create add student route
@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        mobile_numer = request.form['mobile_number']
        student = Student(name, mobile_numer)
        print(student.name)
        print(student.mobile_numer)
        # save student to mongo db
        student_collection.insert_one(
            {
                'name': student.name,
                'mobile_number': student.mobile_numer
            })

        # add flash messaage on success
        flash('Student Added Successfully')
        return redirect(url_for('index'))
    else:
        # sent add student form  html page
        return render_template('add_student.html')

# create delete student by id route 
@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    # delete student by id
    print('delete student _id: ' , student_id)
    student_collection.delete_one({'_id': ObjectId(student_id)})
    # add flash message
    flash('Student Deleted Successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
