from flask import Blueprint, redirect, render_template, request, url_for
school_bp = Blueprint('schools', __name__, url_prefix='/schools')

@school_bp.route('/search', methods=['GET', 'POST'])
def search(): 
    # read from mongodb collection schools filter by city
    if request.method == 'POST':
        city = request.form['city']
        from app import mongo_client
        from managers.school_manager import SchoolManager
        school_manager = SchoolManager(mongo_client)
        school_list = school_manager.get_schools_by_city(city)
        return render_template('schools/search.html',
                               city=city, school_list=school_list)
    else:
        return render_template('schools/search.html')

@school_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        area = request.form['area']
        city = request.form['city']
        pincode = request.form['pincode']
        phone_number = request.form['phone_number']

        # Save the data to MongoDB
        from app import mongo_client
        from managers.school_manager import SchoolManager
        school_manager = SchoolManager(mongo_client)
        school_manager.add_school(name, address, area, city, pincode, phone_number)
        
        return redirect(url_for('schools.search'))
    else:
        return render_template('schools/add.html')

@school_bp.route('/edit/<school_id>', methods=['GET', 'POST']) 
def edit(school_id):
    from app import mongo_client
    from managers.school_manager import SchoolManager
    school_manager = SchoolManager(mongo_client)
    if request.method == 'POST':
        #handle saving school from form, redirect to search
        # populate school_id, name, address, area, city, pincode, phone_number from form
        name = request.form['name']
        address = request.form['address']
        area = request.form['area']
        city = request.form['city']
        pincode = request.form['pincode']
        phone_number = request.form['phone']
        school_manager.update_school(school_id, name, address, area, city, pincode, phone_number)
        return redirect(url_for('schools.search'))
    else:
        #read school from mongodb, display edit form
        school = school_manager.get_school_by_id(school_id)
        return render_template('schools/edit.html', school=school)

@school_bp.route('/delete/<school_id>', methods=['GET'])
def delete(school_id):
    from app import mongo_client
    from managers.school_manager import SchoolManager
    school_manager = SchoolManager(mongo_client)
    school_manager.delete_school(school_id)
    return redirect(url_for('schools.search'))


@school_bp.route('/list', methods=['GET'])
def list():
    from app import mongo_client
    from managers.school_manager import SchoolManager
    school_manager = SchoolManager(mongo_client)
    school_list = school_manager.get_schools()
    return render_template('schools/list.html', school_list=school_list)