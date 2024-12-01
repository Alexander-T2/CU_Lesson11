from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# база данных с информацией о картинках
database = []
next_id = 1

@app.route('/')
def hello():
    return render_template("hello.html")


@app.route('/upload_pics', methods=['GET', 'POST'])
def upload_pics():
    if request.method == 'GET':
        return render_template('upload_form.html')
    elif request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1] # чтобы имена файлов не повторялись
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            global next_id
            new_image = {
                'filename': filename,
                'id': next_id,
                'title': request.form.get('title', 'Без названия') # Обработка отсутствия заголовка
            }
            database.append(new_image)
            next_id += 1
            return jsonify({'task': new_image})

@app.route('/pics')
def get_pics():
  return jsonify({'database': database})


@app.route('/pics/<int:pic_id>')
def get_pic(pic_id):
    for pic in database:
        if pic['id'] == pic_id:
            return send_from_directory(app.config['UPLOAD_FOLDER'], pic['filename'])
    return jsonify({'error': 'Id not found'}), 404

@app.route('/pics/<int:pic_id>', methods=['PUT', 'DELETE'])
def modify_pic(pic_id):
    pic_index = next((i for i, pic in enumerate(database) if pic['id'] == pic_id), None)
    if pic_index is None:
        return jsonify({'error': 'Id not found'}), 404

    if request.method == 'PUT':
        try:
            data = request.get_json()
            if 'title' in data:
                database[pic_index]['title'] = data['title']
            return jsonify({'message': 'Image updated successfully', 'image': database[pic_index]})
        except:
            return jsonify({'error': 'Invalid JSON'}), 400

    elif request.method == 'DELETE':
        filename = database[pic_index]['filename']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)  # Удаляем файл
        del database[pic_index]
        return jsonify({'message': 'Image deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
