from flask import Flask

app = Flask(__name__)

@app.route('/siraji')
def sirajull():
    return 'Hello Sirajulllll!'

@app.route('/sirajulllls')

def sirajii():
    return 'MOHAMED SIRAJIII!'

if __name__ == '__main__':
    app.run()