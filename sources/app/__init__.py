from flask import Flask, render_template, current_app
import  os

app = Flask(__name__)

# Thiết lập cấu hình
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Thực hiện các hoạt động yêu cầu ngữ cảnh ứng dụng ở đây
root_path_folder = current_app.root_path
# Lấy thư mục chứa file hiện tại
current_directory = root_path_folder + '/models'
MODEL_PATH = os.path.join(current_directory, 'model_EfficientnetB0.h5')


# Import Blueprint và đăng ký Blueprint vào app
from app.routes import upload, index
# predict

app.register_blueprint(index.index_bp)
app.register_blueprint(upload.upload_bp)
# app.register_blueprint(predict.predict_bp)
