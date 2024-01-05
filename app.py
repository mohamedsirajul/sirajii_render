from flask import Flask

app = Flask(__name__)

@app.route('/siraji')
def hello_world():
    return 'Hello Sirajj!'

if __name__ == '__main__':
    app.run()