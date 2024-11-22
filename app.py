from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from PIL import Image
import numpy as np
import cv2

app = Flask(__name__)

# Direktori untuk mengunggah dan menyimpan hasil gambar
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Pastikan folder ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Ambil file gambar yang diunggah
        file = request.files['image']
        dx = int(request.form['dx'])
        dy = int(request.form['dy'])

        if file:
            # Simpan file unggahan
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Proses translasi
            translated_path = translate_image(filepath, dx, dy)
            return render_template('index.html', original=file.filename, translated=translated_path)

    return render_template('index.html', original=None, translated=None)

def translate_image(image_path, dx, dy):
    # Baca gambar
    img = cv2.imread(image_path)
    rows, cols, _ = img.shape

    # Matriks transformasi translasi
    M = np.float32([[1, 0, dx], [0, 1, dy]])

    # Lakukan translasi
    translated_img = cv2.warpAffine(img, M, (cols, rows))

    # Simpan hasil gambar
    filename = os.path.basename(image_path)
    result_path = os.path.join(app.config['RESULT_FOLDER'], f"translated_{filename}")
    cv2.imwrite(result_path, translated_img)
    return f"results/translated_{filename}"

@app.route('/static/<path:filename>')
def serve_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
