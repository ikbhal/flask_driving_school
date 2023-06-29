from flask import Flask, render_template
from routes.student_routes import students_bp
from flask_pymongo import PyMongo
# from routes.appointment_routes import appointment_bp


app = Flask(__name__)
app.secret_key = 'allah raji hojaye'

mongo_client = PyMongo(app, uri="mongodb://localhost:27017/skool")
student_collection = mongo_client.db.students

app.register_blueprint(students_bp)
# app.register_blueprint(appointment_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
