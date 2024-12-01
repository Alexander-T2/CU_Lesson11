from flask import Flask, make_response
from flask import jsonify
from flask import render_template
from flask import request
import requests

tasks = [
    {
        'id': 1,
        'title': 'Долги по домашкам',
        'description': 'нету',
        'done': False
    },
    {
        'id': 2,
        'title': 'Реквием по мечте',
        'description': 'Хач ачач ачача',
        'done': True
    }
]

app = Flask(__name__)

@app.route('/')
def hello_library():
    return 'Я больше не могу... (приветствие)'

# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((b for b in tasks if b['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'задача не найдена'}), 404
    return jsonify({'task': task})

@app.route('/tasks', methods=['GET'])
def get_tasks():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 10, type=int)

  start = (page - 1) * per_page
  end = start + per_page

  total = len(tasks)
  paginated_tasks = tasks[start:end]

  response = {
    'tasks': paginated_tasks,
    'page': page,
    'per_page': per_page,
    'total': total
  }

  return jsonify(response)

@app.route('/new_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        return render_template('add_task.html')
    elif request.method == 'POST':
        new_task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.form['title'],
            'description': request.form['description'],
            'done': request.form['done']
        }
        tasks.append(new_task)
        return jsonify({'task': new_task})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((b for b in tasks if b['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'задача не найдена'}), 404

    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'dscription' in request.json:
        task['dscription'] = request.json['dscription']
    if 'done' in request.json:
        task['done'] = request.json['done']

    return jsonify({'task': task})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((b for b in tasks if b['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'задача не найдена'}), 404

    tasks.remove(task)
    return jsonify({'message': f'задача с id {task_id} удалена'})

if __name__ == '__main__':
    app.run(debug=True)