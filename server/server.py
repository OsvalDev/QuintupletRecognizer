from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
CORS(app)
# dic = ['ichika', 'itsuki', 'miku', 'nino', 'yotsuba']
dic = ['asuna', 'chizuru', 'ichika', 'itsuki', 'kaede', 'mai', 'mami', 'miku', 'nino', 'rei', 'ruka', 'serena', 'sumi', 'yotsuba', 'zerotwo']

img_size=(150, 300)

model = load_model('../exportedModels/modelFeatureMaps.h5')

model.make_predict_function()

def predict_label(img_path):
    img = image.load_img(img_path, target_size=(img_size[1], img_size[0]))
    img = np.reshape(img, (1,img_size[1],img_size[0],3))

    p = model.predict(img)
    predicted_index = np.argmax(p)
    predicted_class = dic[predicted_index]
    prediction_value = p[0][predicted_index]
    return predicted_class, prediction_value

# routes
@app.route("/", methods=['GET'])
def main():
    return render_template("index.html")

@app.route("/submitPreset", methods = ['POST'])
def get_prediction_preset():
    data = request.get_json()
    print(data)

    img_path = data.get('pathPreset', "")
    predicted_class, prediction_value = predict_label(img_path)
    response = {
        "confidence" : float(prediction_value),
        "name" : predicted_class,
        "img_path" : img_path
    }
    return jsonify(response)

@app.route("/submit", methods = ['POST'])
def get_prediction():
    img = request.files.get('my_image')
    if img:
        directory = "static/img/"
        base_name = "predictedImg"
        for filename in os.listdir(directory):
            if filename.startswith(base_name):
                os.remove(os.path.join(directory, filename))
                break

        _, ext = os.path.splitext(img.filename)
        new_filename = base_name + ext
        img_path = directory + new_filename
        img.save(img_path)
    predicted_class, prediction_value = predict_label(img_path)
    response = {
        "confidence" : float(prediction_value),
        "name" : predicted_class,
        "img_path" : img_path
    }
    return jsonify(response)

if __name__ =='__main__':
    #app.debug = True
    app.run(debug = True, host='0.0.0.0')