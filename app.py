from flask import Flask, render_template
from flask_pymongo import PyMongo
from routes.student_routes import students_bp
from routes.class_routes import class_bp
from routes.photo_routes import photo_bp
from routes.school_routes import school_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'allah raji hojaye'

mongo_client = PyMongo(app, uri="mongodb://localhost:27017/skool")
student_collection = mongo_client.db.students

app.register_blueprint(students_bp)
app.register_blueprint(class_bp)
app.register_blueprint(photo_bp)
app.register_blueprint(school_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
