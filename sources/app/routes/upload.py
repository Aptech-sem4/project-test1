from flask import Blueprint, render_template, request,jsonify
from werkzeug.utils import secure_filename
import base64, os, secrets
from app.models.img_process import process_image

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
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            random_string = secrets.token_hex(8)
            new_filename = random_string + '_' + filename
            file.save(os.path.join('app/static/uploads', new_filename))
            
            # Gọi model AI để xử lý ảnh
            process_image(file)

            return 'File uploaded successfully'
    
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
        filename = 'camera_image.png'  # Đặt tên file
        with open(os.path.join('app/static/uploads', filename), 'wb') as f:
            f.write(img_data)

        # Xử lý ảnh (nếu cần)
        # process_image(img_data)

        return 'Image uploaded successfully'
    return 'Invalid request'
