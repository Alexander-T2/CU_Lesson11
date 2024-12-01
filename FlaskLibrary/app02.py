from flask import Flask, make_response
from flask import jsonify
from flask import render_template
from flask import request
import requests

tasks = [
    {
        'id': 1,
        'title': 'Гарри Поттер и философский камень',
        'author': 'Дж. К. Роулинг',
        'published': 1997,
        'read': False
    },
    {
        'id': 2,
        'title': 'Властелин колец: Братство Кольца',
        'author': 'Дж. Р. Р. Толкин',
        'published': 1954,
        'read': True
    }
]

app = Flask(__name__)

@app.route('/')
def hello_library():
    return 'Добро пожаловать в библиотеку книг!'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((b for b in tasks if b['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Книга не найдена'}), 404
    return jsonify({'task': task})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Id not found'}), 404)

@app.route('/new_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        return render_template('add_task.html')
    elif request.method == 'POST':
        new_task = {
            'id': tasks[-1]['id'] + 1,  # Присваиваем новый уникальный ID
            'title': request.form['title'],
            'author': request.form['author'],
            'published': int(request.form['published']),
            'read': False  # По умолчанию книга не прочитана
        }
        tasks.append(new_task)
        return jsonify({'task': new_task})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((b for b in tasks if b['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Книга не найдена'}), 404

    # Обновляем данные книги
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'author' in request.json:
        task['author'] = request.json['author']
    if 'published' in request.json:
        task['published'] = request.json['published']
    if 'read' in request.json:
        task['read'] = request.json['read']

    return jsonify({'task': task})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((b for b in tasks if b['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Книга не найдена'}), 404

    tasks.remove(task)
    return jsonify({'message': f'Книга с id {task_id} удалена'})

if __name__ == '__main__':
    app.run(debug=True)
    # Данные для обновления
    data = {'read': True}

    # Отправляем PUT-запрос
    response = requests.put('http://127.0.0.1:5000/tasks/1', json=data)

    # Выводим обновлённые данные книги
    print(response.json())
    # Отправляем DELETE-запрос
    response = requests.delete('http://127.0.0.1:5000/tasks/1')

    # Выводим сообщение о результате
    print(response.json())
    # Проверим, что книга 1 действительно удалена.
    # Это можно сделать по ссылке http://127.0.0.1:5000/tasks/1 в браузере или через requests. Сделаем вторым способом для разнообразия.
    r = requests.get('http://127.0.0.1:5000/tasks/1')
    print(r.text)
    # Вернулась ошибка, что запись не найдена. Всё верно, мы её только что удалили.