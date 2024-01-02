from flask import Blueprint, render_template, jsonify
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from flask import current_app
from app import MODEL_PATH

# # from tensorflow.keras.applications import EfficientNetB0
# import numpy as np
# import pickle

# predict_bp = Blueprint('predict', __name__)

mymodel = load_model(MODEL_PATH)

# # Load pre-trained model
# model = EfficientNetB0(weights=MODEL_PATH)
    
def process_image(filename):
    # Lấy đường dẫn tuyệt đối của file hiện tại
    folder_name = '/static/uploads'
    root_path = current_app.root_path
    
    absolute_path = root_path + folder_name
    file_path = os.path.join(absolute_path, filename)
     # Load and preprocess the image
    print('111111111 vao img process')
    print(file_path)
    img = image.load_img(file_path, target_size=(224, 224))
    print('22222 vao img process')
    print(img)
    # img_array = image.img_to_array(img)
    # img_array = np.expand_dims(img_array, axis=0)
    # processed_img = EfficientNetB0.preprocess_input(img_array)

    # Make prediction
    predictions = mymodel.predict(img)
    # Decode prediction
    # decoded_predictions = EfficientNetB0.decode_predictions(predictions)
    
    # Process decoded predictions to get the top result
    # top_prediction = decoded_predictions[0][0]  # Lấy kết quả dự đoán hàng đầu
    print(predictions)
    return jsonify({
        'predicted_class': predictions,
        # 'probability': float(top_prediction[2])
    })
    # pass
