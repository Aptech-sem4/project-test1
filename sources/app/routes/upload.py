from flask import Blueprint, render_template, request,jsonify, redirect, Response
from werkzeug.utils import secure_filename
import base64, os, secrets, numpy as np
# import cv2
from flask import current_app

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

            # Lấy đường dẫn tuyệt đối của file hiện tại
            folder_name = '/static/uploads'
            root_path = current_app.root_path
            
            absolute_path = root_path + folder_name

            file.save(os.path.join(absolute_path, new_filename))
            
            # Gọi model AI để xử lý ảnh
            res_predict = process_image(new_filename)
            # res_predict = 'test'
            print(res_predict)

            res = {
                'message': 'File uploaded successfully',
                'data' : {
                    # 'type': res_predict,
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
        
        # Lấy đường dẫn tuyệt đối của file hiện tại
        folder_name = '/static/uploads'
        root_path = current_app.root_path
        absolute_path = root_path + folder_name
        
        with open(os.path.join(absolute_path, new_filename), 'wb') as f:
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


# @upload_bp.route('/detect_objects')
# def video_feed():
#     return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')


# def detect_objects():
#     camera = cv2.VideoCapture(0) 
#     net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
#     classes = []
#     with open("coco.names", "r") as f:
#         classes = [line.strip() for line in f.readlines()]

#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#     print(output_layers)

#     while True:
#         success, frame = camera.read()
#         if not success:
#             break

#         height, width, channels = frame.shape
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        
#         net.setInput(blob)
#         outs = net.forward(output_layers)
        
#         class_ids = []
#         confidences = []
#         boxes = []
        
#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5:
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)

#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)

#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)
        
#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
#         for i in range(len(boxes)):
#             if i in indexes:
#                 x, y, w, h = boxes[i]
#                 label = str(classes[class_ids[i]])
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
