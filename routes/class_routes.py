from flask import Blueprint, request, render_template, redirect, url_for, flash

class_bp = Blueprint('class', __name__)

@class_bp.route('/add_class/<student_id>', methods=['POST', 'GET'])
def add_class(student_id):
    print( "inside add_class route: student_id = ", student_id)
    from app import mongo_client
    from managers.class_manager import ClassManager
    from managers.student_manager import StudentManager
    student_manager = StudentManager(mongo_client)
    student =  student_manager.get_student_by_id(student_id)
    # student_mobile_number = student['mobile_number'] 
    
    if request.method == 'POST':
        # student_mobile_number = request.form['student_mobile_number']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        # Create an instance of the DrivingAppointmentManager
        class_manager = ClassManager(mongo_client)
        
        # Add the class appointment
        class_manager.add_class(student_id, date, start_time, end_time)

        flash('Class added successfully.')
        return redirect(url_for('class.list_classes', 
                                student_id=student_id))
    else:
        return render_template('classes/add.html', student_id=student['_id'])

@class_bp.route('/students/<student_id>/list_class')
def list_classes(student_id):
    # list classes
    from app import mongo_client
    from managers.class_manager import ClassManager
    class_manager = ClassManager(mongo_client)
    classes = class_manager.list_clasess(student_id)
    #get student 
    from managers.student_manager import StudentManager
    studenet_manager = StudentManager(mongo_client=mongo_client)
    student = studenet_manager.get_student_by_id(student_id)
    return render_template('classes/list.html', 
                           classes=classes,
                           student=student
                           )

@class_bp.route('/students/<student_id>/delete_class/<class_id>')
def delete_class(student_id, class_id):
    # delete class
    from app import mongo_client
    from managers.class_manager import ClassManager
    class_manager = ClassManager(mongo_client)
    class_manager.delete_class(class_id)

    flash('Class deleted successfully.')
    return redirect(url_for('class.list_classes',student_id=student_id))

