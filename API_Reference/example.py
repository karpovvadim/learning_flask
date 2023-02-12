import json
from tkinter import Image
from typing import io
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def predict_image():
    return "Error processing image', 500"


def predict_image_handler():
    try:
        imageData = None
        if 'imageData' in request.files:
            imageData = request.files['imageData']
        else:
            imageData = io.BytesIO(request.get_data())

        # img = scipy.misc.imread(imageData)
        img = Image.open(imageData)
        results = predict_image(img)
        return json.dumps(results)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image', 500


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)
