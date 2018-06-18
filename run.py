from flask import Flask, request, send_from_directory, jsonify

app = Flask('Amazon')

products = []


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        query = request.args['name']
        for prod in products:
            if prod['name'] == query:
                return jsonify(prod)
        return 'No match'
    elif request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        prod = {
            'name': name,
            'desc':  desc,
            'price': price
        }
        products.append(prod)
        return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
