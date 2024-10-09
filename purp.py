from flask import Flask, render_template, request, redirect, url_for
from waitress import serve
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    return render_template('landing.html')  # Redirects to the landing page

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return redirect(url_for('display_image', filename=file.filename))
    return render_template('upload.html')

@app.route('/display/<filename>')
def display_image(filename):
    return render_template('display.html', filename=filename)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)

