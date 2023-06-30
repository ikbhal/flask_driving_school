
from flask import Blueprint, render_template, request
import firebase_admin
from firebase_admin import credentials, storage
import os

current_directory = os.getcwd()
# parent_directory = os.path.dirname(current_directory)
service_account_path = os.path.join(current_directory, 'firebase-service-account.json')
print ("***** ikb service_account_path " + service_account_path)

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    # 'storageBucket': 'gs://ikbhal-cb53f.appspot.com'
    'storageBucket':'ikbhal-cb53f'
})

# firebase photo 
fbs_photo_bp = Blueprint('fbs_photos', __name__, url_prefix='/fbs')

@fbs_photo_bp.route('/upload', methods=['POST', 'GET'])
def upload_photo():
    if request.method == 'POST':
        file = request.files['photo']
        bucket = storage.bucket()
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        blob.make_public()
        url = blob.public_url
        output = 'Photo uploaded successfully. url: ' + url + "<br>" + '<img src="' + url +'" alt="Photo">'
        return output
    else:
        return render_template('fbs_photos/upload_photo.html')

@fbs_photo_bp.route('/photo/<photo_id>')
def get_photo(photo_id):
    bucket = storage.bucket()
    blob = bucket.blob(photo_id)
    url = blob.public_url
    return f'<img src="{url}" alt="Photo">'

