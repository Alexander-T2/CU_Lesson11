# Импортируй Flask
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request


# Создай приложение
app = Flask(__name__)

# Определи маршрут для главной страницы
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/hello/<name>')
def hello(name):
  return render_template('hello.html', name=name)

@app.route('/data')
def data():
    return jsonify({'key': 'value'})

@app.route('/hello_post', methods=['GET', 'POST'])
def hello_post_world():
    if request.method == 'GET':
        return render_template('name.html')
    else:
        return render_template('hello.html', name=request.form['name'])

# Запусти приложение в режиме отладки
if __name__ == '__main__':
    app.run(debug=True)
    hello("Natasha")