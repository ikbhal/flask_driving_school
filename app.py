from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class Student:
    def __init__(self, name, mobile_number, joining_date,
                  application_number,
                    amount, discount, amount_paid, settle_amount, 
                    course,
                    training_days=10, notes=''
                    ):
        self.name = name
        self.mobile_number = mobile_number
        self.joining_date = joining_date
        self.application_number = application_number
        self.amount = amount
        self.discount = discount
        self.amount_paid = amount_paid
        self.settle_amount = settle_amount
        self.course = course
        self.training_days = training_days
        self.notes = notes

app = Flask(__name__)
app.secret_key = 'allah raji hojaye'
mongo_client = PyMongo(app, uri="mongodb://localhost:27017/skool")
student_collection = mongo_client.db.students

@app.route('/')
def index():
    student_list = student_collection.find()
    return render_template('index.html', student_list=student_list)

@app.route('/list_students')
def list_students():
    student_list = student_collection.find()
    return render_template('list_students.html', student_list=student_list)

@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        joining_date = request.form['joining_date']
        application_number = request.form['application_number']
        amount = request.form['amount']
        discount = request.form['discount']
        amount_paid = request.form['amount_paid']
        settle_amount = request.form['settle_amount']
        course = request.form['course']
        training_days = request.form['training_days']
        notes = request.form['notes']


        student = Student(name, mobile_number, joining_date,
                           application_number,
                            amount, discount, amount_paid, settle_amount, 
                            course,
                            training_days, notes)
        
        student_collection.insert_one({
            'name': student.name,
            'mobile_number': student.mobile_number,
            'joining_date': student.joining_date,
            'application_number': student.application_number,
            'amount': student.amount,
            'discount': student.discount,
            'amount_paid': student.amount_paid,
            'settle_amount': student.settle_amount,
            'course': student.course,
            'training_days': student.training_days,
            'notes': student.notes
        })

        flash('Student Added Successfully')
        return redirect(url_for('index'))
    else:
        return render_template('add_student.html')
    
# create a route for viewing student
@app.route('/view_student/<student_id>')
def view_student(student_id):
    student = student_collection.find_one({'_id': ObjectId(student_id)})
    return render_template('view_student.html', student=student)

# create route for editing student
@app.route('/edit_student/<student_id>', methods=['POST', 'GET'])
def edit_student(student_id):
    if request.method == 'POST':
        #edit handling
        # fetch student from db given id
        student = student_collection.find_one({'_id': ObjectId(student_id)})

        # retrieve fields from form request , update the in the matched student
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        joining_date = request.form['joining_date']
        application_number = request.form['application_number']
        amount = request.form['amount']
        discount = request.form['discount']
        amount_paid = request.form['amount_paid']
        settle_amount = request.form['settle_amount']
        course = request.form['course']
        training_days = request.form['training_days']
        notes = request.form['notes']

        # update in student object
        student.name = name
        student.mobile_number = mobile_number
        student.joining_date = joining_date
        student.application_number = application_number
        student.amount = amount
        student.discount = discount
        student.amount_paid = amount_paid
        student.settle_amount = settle_amount
        student.course = course
        student.training_days = training_days
        student.notes = notes

        # save studenet back to db
        student_collection.save(student)
        flash('Student Updated Successfully')

    else:
        student = student_collection.find_one({'_id': ObjectId(student_id)})
        return render_template('edit_student.html', student=student)
    

@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    student_collection.delete_one({'_id': ObjectId(student_id)})
    flash('Student Deleted Successfully')
    return redirect(url_for('index'))

@app.route('/search_student', methods=['POST', 'GET'])
def search_student():
    if request.method == 'POST':
        mobile_number = request.form['mobile_number']
        student = student_collection.find_one({'mobile_number': mobile_number})
        if student:
            return render_template('search_student.html', student=student)
        else:
            flash('Student not found')
    return render_template('search_student.html')

if __name__ == '__main__':
    app.run(debug=True)
