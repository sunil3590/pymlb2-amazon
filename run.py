from flask import Flask, request

app = Flask('Amazon')


@app.route('/', methods=['GET'])
def index():
    return 'Welcome!'


# http://127.0.0.1:5005/say_hello?name=Sunil
@app.route('/say_hello', methods=['GET'])
def say_hello():
    if request.method == 'GET':
        return 'Hello, ' + request.args['name']


@app.route('/say_bye', methods=['GET'])
def say_bye():
    return 'Bye!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005)
