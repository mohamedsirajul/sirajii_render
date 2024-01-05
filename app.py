from flask import Flask

app = Flask(__name__)

@app.route('/siraji')
def sirajull():
    return 'Hello Sirajulllll!'

if __name__ == '__main__':
    app.run()