from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_time=current_time)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    if name:
        greeting = f"Привет, {name}!"
    else:
        greeting = "Привет, Гость!"
    return render_template('hello.html', greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True)