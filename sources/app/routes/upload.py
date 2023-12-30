from flask import Blueprint, render_template, request,jsonify, redirect
from werkzeug.utils import secure_filename
import base64, os, secrets
from app.models.img_process import process_image
from datetime import datetime

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url) 

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")


            random_string = secrets.token_hex(8)
            new_filename = current_time + '_' + random_string + '_' + filename
            file.save(os.path.join('app/static/uploads', new_filename))
            
            # Gọi model AI để xử lý ảnh
            res_predict = process_image(new_filename)
            print(res_predict)

            res = {
                'message': 'File uploaded successfully',
                'data' : {
                    'type': res_predict,
                    'file_name' : new_filename
                }
            }

            return jsonify(res)
    
    return render_template('upload.html')

@upload_bp.route('/upload_from_camera', methods=['GET'])
def show_upload_from_camera():
    return render_template('capture_image.html')

@upload_bp.route('/upload_from_camera', methods=['POST'])
def upload_from_camera():
    data = request.get_json()
    if 'image' in data:
        image_data = data['image'].split(',')[1]  # Lấy dữ liệu ảnh từ base64
        img_data = base64.b64decode(image_data)
        
        # Lưu ảnh vào thư mục UPLOAD_FOLDER
        current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        random_string = secrets.token_hex(8)
        new_filename = 'camera_image' + '_' + current_time + '_' + random_string + '.jpg'
        with open(os.path.join('app/static/uploads', new_filename), 'wb') as f:
            f.write(img_data)

        # Xử lý ảnh (nếu cần)
        # process_image(img_data)
        res_predict = process_image(new_filename)
        print(res_predict)

        res = {
                'message': 'File uploaded successfully',
                'data' : {
                    'type': res_predict,
                    'file_name' : new_filename
                }
            }
        
        return jsonify(res)
    return 'Invalid request'
