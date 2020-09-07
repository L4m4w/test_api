import os
import secrets

from flask import Flask, request, render_template, current_app, redirect, \
    send_from_directory


app = Flask(__name__)


def save_file(file):
    hash_file = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(file.filename)
    file_name = hash_file + file_extention
    os.mkdir('static/store/'+str(file_name[:2]))
    file_path = os.path.join(current_app.root_path, 'static/store/'+str(file_name[:2]), file_name)
    file.save(file_path)
    return file_name


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload_page():
    if request.method == 'POST':
        file = save_file(request.files['rnd_file'])
        return file
    else:
        return render_template('upload.html')


@app.route('/download/<path:filename>')
def down_page(filename):
    return send_from_directory('static/store/' + filename[:2], filename)


@app.route('/delete/<name>')
def delete_page(name):
    os.remove('static/store/' + name[:2] + '/' + name)
    os.rmdir('static/store/' + name[:2])

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
