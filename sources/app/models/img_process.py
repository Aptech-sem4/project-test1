from flask import Blueprint, render_template, jsonify
import os, numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from flask import current_app
from app import MODEL_PATH

mymodel = load_model(MODEL_PATH)
    
def process_image(filename):
    # Lấy đường dẫn tuyệt đối của file hiện tại
    folder_name = '/static/uploads'
    root_path = current_app.root_path
    
    absolute_path = root_path + folder_name
    file_path = os.path.join(absolute_path, filename)

    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255
    
    predictions = mymodel.predict(img_array)

    y_pred = np.argmax(predictions, axis=1)
    # target_names = classes
    # Decode prediction
    # decoded_predictions = EfficientNetB0.decode_predictions(predictions)
    
    # Process decoded predictions to get the top result
    # top_prediction = decoded_predictions[0][0]  # Lấy kết quả dự đoán hàng đầu
    print(y_pred)
    return y_pred
    # pass
