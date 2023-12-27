from flask import Flask, render_template

app = Flask(__name__)

# Thiết lập cấu hình
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Import Blueprint và đăng ký Blueprint vào app
from app.routes import upload, index
# predict

app.register_blueprint(index.index_bp)
app.register_blueprint(upload.upload_bp)
# app.register_blueprint(predict.predict_bp)
