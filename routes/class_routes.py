from flask import Blueprint, request, render_template, redirect, url_for, flash

from managers.driving_appointment_manager import DrivingAppointmentManager

class_bp = Blueprint('class', __name__)

@class_bp.route('/add_class/<student_mobile_number>', methods=['POST', 'GET'])
def add_class(student_mobile_number):
    if request.method == 'POST':
        # student_mobile_number = request.form['student_mobile_number']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        # Import necessary modules or classes
        from app import mongo_client
        from managers.class_manager import ClassManager

        # Create an instance of the DrivingAppointmentManager
        class_manager = ClassManager(mongo_client)

        # Add the class appointment
        class_manager.add_class(student_mobile_number, date, start_time, end_time)

        flash('Class added successfully.')
        return redirect(url_for('class.list_classes', 
                                student_mobile_number=student_mobile_number))
    else:
        return render_template('classes/add.html', student_mobile_number=student_mobile_number)

@class_bp.route('/list_class/<student_mobile_number>')
def list_classes(student_mobile_number):
    from app import mongo_client
    from managers.class_manager import ClassManager
    class_manager = ClassManager(mongo_client)
    classes = class_manager.list_clasess(student_mobile_number)
    return render_template('classes/list.html', 
                           classes=classes,
                           student_mobile_number=student_mobile_number
                           )

# @class_bp.route('/delete_class')
# def delete_class():
#     return "delete class"

