
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import send_from_directory
from werkzeug.utils import secure_filename
from bson import ObjectId

import os
# Create a blueprint for the photo-related routes
photo_bp = Blueprint('photos', __name__)

# Define the allowed photo extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for displaying photo upload form page
@photo_bp.route('/upload_photo/<student_id>', methods=['GET'])
def upload_photo_form(student_id):
    # TODO create upload_photo.html -> form -> file tag, action , multi part
    return render_template('photos/upload_photo.html', student_id= student_id)


# Route for uploading a photo for a student
@photo_bp.route('/upload_photo/<student_id>', methods=['POST'])
def upload_photo_handle(student_id):
    # Check if a file is included in the request
    if 'photo' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('students.view_student', student_id=student_id))
    
    photo = request.files['photo']
    
    # Check if a file is selected
    if photo.filename == '':
        flash('No file selected')
        return redirect(url_for('students.view_student', student_id=student_id))
    
    # Check if the file has an allowed extension
    if not allowed_file(photo.filename):
        flash('Invalid file extension')
        return redirect(url_for('students.view_student', student_id=student_id))
    
    # Secure the filename to prevent any malicious behavior
    filename = secure_filename(photo.filename)
    
    # Save the photo to a folder on the server
    from app import mongo_client, app
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Store the photo path in MongoDB
    
    student_collection = mongo_client.db.students
    student_collection.update_one({'_id': ObjectId(student_id)}, {'$set': {'photo_path': filename}})
    
    flash('Photo uploaded successfully')
    return redirect(url_for('students.view_student', student_id=student_id))


@photo_bp.route('/photos/<filename>')
def view_photo(filename):
    return send_from_directory('uploads', filename)