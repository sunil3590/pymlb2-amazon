"""
do the actual configureation of flask app here
this means, adding routes and implementing the APIs
"""
from amazon import app
from flask import request, send_from_directory, render_template
from amazon.models import product as product_model


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        query_name = request.args['name']
        matching_products = product_model.search_by_name(query_name)

        # return the first matching product
        return render_template('results.html',
                               query=query_name,
                               results=matching_products)
    elif request.method == 'POST':
        # lets add and update here
        op_type = request.form['op_type']

        # read data from request and store in a dict
        prod = {
            'name': request.form['name'],
            'desc': request.form['desc'],
            'price': request.form['price']
        }

        if op_type == 'add':  # add the product here
            # insert to DB
            product_model.add_product(prod)

            # take user back to index page
            return send_from_directory('static', 'index.html')

        elif op_type == 'update':  # update the product here
            name = request.form['name']
            updated_product = {
                'name': name,
                'desc': request.form['desc'],
                'price': request.form['price']
            }
            product_model.update_product(name, updated_product)

            # take user back to index page
            return send_from_directory('static', 'index.html')