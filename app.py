from flask import Flask

app = Flask(__name__)

@app.route('/sirajulllls')
def sirajull():
    return 'MOHAMED SIRAJIII!'

if __name__ == '__main__':
    app.run()