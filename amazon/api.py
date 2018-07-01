"""
do the actual configureation of flask app here
this means, adding routes and implementing the APIs
"""
from amazon import app
from flask import request, session, render_template
from amazon.models import product as product_model
from amazon.models import user as user_model


# this is the index page of our website
@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        user_details = user_model.search_by_userid(session['user_id'])
        return render_template('home.html', name=user_details['name'])
    else:
        return render_template('index.html', message='10% off with PayPal')


# this is to logout of our website
@app.route('/logout', methods=['GET'])
def logout():
    print(session)
    del session['user_id']
    return render_template('index.html', message='10% off with PayPal')


# this is the entry point for administrators
@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html', message='Welcome admin')


# API related to products - add, delete, update, get/search
@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        query_name = request.args['name']
        matching_products = product_model.search_by_name(query_name)

        # sort based on price
        # matching_products.sort(key=lambda x: x['price'], reverse=False)

        # return the first matching product
        return render_template('results.html',
                               query=query_name,
                               products=matching_products)
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

            # take user back to admin page
            return render_template('admin.html', message='Successfully added')

        elif op_type == 'update':  # update the product here
            # TODO - update product using _id
            name = request.form['name']
            updated_product = {
                'name': name,
                'desc': request.form['desc'],
                'price': request.form['price']
            }
            product_model.update_product(name, updated_product)

            # take user back to admin page
            return render_template('admin.html', message='Successfully updated')


# API related to users - login, signup
@app.route('/api/user', methods=['POST'])
def user():
    # to login and signup
    op_type = request.form['op_type']

    if op_type == 'login':
        username = request.form['username']
        password = request.form['password']
        success = user_model.authenticate(username, password)
        if success:
            user_details = user_model.search_by_username(username)
            # save the user_id in the session for use in future requests
            # convert the _id from ObjectId to str
            session['user_id'] = str(user_details['_id'])
            return render_template('home.html', name=user_details['name'])
        else:
            return render_template('index.html', message='Invalid username/password')
    elif op_type == 'signup':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        success = user_model.signup_user(name, username, password)
        if success:
            user_details = user_model.search_by_username(username)
            # save the user_id in the session for use in future requests
            # convert the _id from ObjectId to str
            session['user_id'] = str(user_details['_id'])
            return render_template('home.html', name=user_details['name'])
        else:
            return render_template('index.html', message='username already exists')
    else:
        # take user back to admin page
        return render_template('index.html', message='Something went wrong')


# API related to cart - add to cart, remove from cart, view cart
@app.route('/api/cart', methods=['POST'])
def cart():
    # add / delete / retrieve
    op_type = request.form['op_type']
    user_id = session['user_id']
    if op_type == 'add':
        product_id = request.form['product_id']
        user_model.add_to_cart(user_id, product_id)
        user_details = user_model.search_by_userid(user_id)
        return render_template('home.html', name=user_details['name'])
    elif op_type == 'delete':
        product_id = request.form['product_id']
        user_model.delete_from_cart(session['user_id'], product_id)
    elif op_type == 'retrieve':
        cart_item_ids = user_model.retrieve_cart(user_id)

        cart_items = []
        for p_id in cart_item_ids:
            cart_items.append(product_model.get_details(p_id))

        user_details = user_model.search_by_userid(user_id)

        return render_template('cart.html',
                               products=cart_items,
                               name=user_details['name'])
