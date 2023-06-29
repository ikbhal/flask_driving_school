from flask import Blueprint, render_template, request, redirect, url_for, flash
# from pymongo import MongoClient
# from db import client
from managers.driving_appointment_manager import DrivingAppointmentManager

# appointment_manager = DrivingAppointmentManager(client)
appointment_bp = Blueprint('appointment', __name__
                        #    , url_prefix="/appointments"
                           )

@appointment_bp.route('/ping')
def ping():
    return "pong"

@appointment_bp.route('/add', methods=['POST', 'GET'])
def add_appointment():
    if request.method == 'POST':
        student_id = request.form['student_id']
        date = request.form['date']
        time_slot = request.form['time_slot']

        from app import mongo_client
        appointment_manager = DrivingAppointmentManager(mongo_client)

        appointment_manager.add_appointment(student_id, date, time_slot)
        flash('Appointment added successfully.')
        return redirect(url_for('appointment.list_appointments'))
    else:
        return render_template('appointments/add.html')

@appointment_bp.route('/delete/<appointment_id>')
def delete_appointment(appointment_id):
    from app import mongo_client
    appointment_manager = DrivingAppointmentManager(mongo_client)

    appointment_manager.delete_appointment(appointment_id)
    flash('Appointment deleted successfully.')
    return redirect(url_for('appointment.list_appointments'))

@appointment_bp.route('/edit/<appointment_id>', methods=['POST'])
def edit_appointment(appointment_id):
    date = request.form['date']
    time_slot = request.form['time_slot']

    from app import mongo_client
    appointment_manager = DrivingAppointmentManager(mongo_client)
    appointment_manager.edit_appointment(appointment_id, date, time_slot)
    flash('Appointment edited successfully.')
    return redirect(url_for('appointment.list_appointments'))

@appointment_bp.route('/list')
def list_appointments():
    student_id = request.args.get('student_id')

    from app import mongo_client
    appointment_manager = DrivingAppointmentManager(mongo_client)
    appointments = appointment_manager.get_appointments_by_student(student_id)
    return render_template('list_appointments.html', appointments=appointments)

