from flask import Blueprint, render_template, jsonify
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# # from tensorflow.keras.applications import EfficientNetB0
# import numpy as np
# import pickle

# predict_bp = Blueprint('predict', __name__)

MODEL_PATH = os.path.join('./sources/app/models', 'model_EfficientnetB0.h5')
mymodel = load_model(MODEL_PATH)

# # Load pre-trained model
# model = EfficientNetB0(weights=MODEL_PATH)
    
def process_image(filename):
    file_path = os.path.join('app/static/uploads', filename)
     # Load and preprocess the image
    img = image.load_img(file_path, target_size=(224, 224))
    # img_array = image.img_to_array(img)
    # img_array = np.expand_dims(img_array, axis=0)
    # processed_img = EfficientNetB0.preprocess_input(img_array)

    # Make prediction
    predictions = mymodel.predict(img)
    # Decode prediction
    # decoded_predictions = EfficientNetB0.decode_predictions(predictions)
    
    # Process decoded predictions to get the top result
    # top_prediction = decoded_predictions[0][0]  # Lấy kết quả dự đoán hàng đầu

    return jsonify({
        'predicted_class': predictions,
        # 'probability': float(top_prediction[2])
    })
    # pass
