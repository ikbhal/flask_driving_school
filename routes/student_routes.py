from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from models.student import Student

students_bp = Blueprint('students', __name__, 
                        url_prefix="/students")


@students_bp.route('/list')
def list_students():
    from app import student_collection
    student_list = student_collection.find()
    return render_template('students/list.html', student_list=student_list)

@students_bp.route('/add', methods=['POST', 'GET'])
def add_student():
    print("inside add_student route")
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
        
        from app import student_collection
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
        print("inside add_student route else")
        return render_template('students/add.html')
    
# create a route for viewing student
@students_bp.route('/view/<student_id>')
def view_student(student_id):
    from app import student_collection
    student = student_collection.find_one({'_id': ObjectId(student_id)})
    return render_template('students/view.html', student=student)

@students_bp.route('/view/mobile_number/<student_mobile_number>', methods=['GET'])
def view_student_by_mobile_number(student_mobile_number):
    from app import student_collection
    student = student_collection.find_one({'mobile_number': student_mobile_number})
    return render_template('students/view.html', student=student)

# create route for editing student
@students_bp.route('/edit/<student_id>', methods=['POST', 'GET'])
def edit_student(student_id):
    from app import student_collection
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
        myquery = { "_id": ObjectId(student_id) }
        newvalues = { "$set": 
            {
                'name': name,
                'mobile_number': mobile_number,
                'joining_date': joining_date,
                'application_number': application_number,
                'amount': amount,
                'discount': discount,
                'amount_paid': amount_paid,
                'settle_amount': settle_amount,
                'course': course,
                'training_days': training_days,
                'notes': notes
            }
        }

        student_collection.update_one(myquery, newvalues)

        # save studenet back to db
        # student_collection.save(student)
        flash('Student Updated Successfully')

        # go back to view page student id
        return redirect(url_for('students.view_student', student_id=student_id))

    else:
        student = student_collection.find_one({'_id': ObjectId(student_id)})
        return render_template('students/edit.html', student=student)
    
@students_bp.route('/delete/<student_id>')
def delete_student(student_id):
    from app import student_collection
    student_collection.delete_one({'_id': ObjectId(student_id)})
    flash('Student Deleted Successfully')
    return redirect(url_for('index'))

@students_bp.route('/search', methods=['POST', 'GET'])
def search_student():
    if request.method == 'POST':
        mobile_number = request.form['mobile_number']
        from app import student_collection
        student = student_collection.find_one({'mobile_number': mobile_number})
        if student:
            return render_template('students/search.html', student=student, mobile_number=mobile_number)
        else:
            flash('Student not found')
    return render_template('students/search.html')