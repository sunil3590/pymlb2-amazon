from amazon.models import db
from bson.objectid import ObjectId


# this function will return the details of "username"
def search_by_userid(user_id):
    # lets search for the user here
    query = {'_id': ObjectId(user_id)}
    matching_user = db['users'].find(query)
    if matching_user.count() == 1:
        return matching_user.next()
    else:
        return None


# this function will return the details of "username"
def search_by_username(username):
    # lets search for the user here
    query = {'username': username}
    matching_user = db['users'].find(query)
    if matching_user.count() > 0:
        return matching_user.next()
    else:
        return None


def signup_user(name, username, password):
    existing_user = search_by_username(username)
    if existing_user is not None:
        return False
    user = {
        'name': name,
        'username': username,
        'password': password,
        'cart': []
    }
    db['users'].insert_one(user)
    return True


def authenticate(username, password):
    user = search_by_username(username)

    if user is None:
        # user does not exist
        return False

    if user['password'] == password:
        # user exists and correct password
        return True
    else:
        # user exists but wrong password
        return False


def add_to_cart(user_id, product_id):
    condition = {'_id': ObjectId(user_id)}

    cursor = db.users.find(condition)

    if cursor.count() == 1:
        user_data = cursor[0]
    else:
        # user id does not exist
        return False

    # to support old users
    if 'cart' not in user_data:
        user_data['cart'] = []

    # add product only if it hasnt been added in the past
    if product_id not in user_data['cart']:
        user_data['cart'].append(product_id)
        db.users.update_one(filter=condition, update={'$set': user_data})

    return True


def delete_from_cart(user_id, product_id):
    condition = {'_id': ObjectId(user_id)}

    cursor = db.users.find(condition)

    if cursor.count() == 1:
        user_data = cursor[0]
    else:
        # user id does not exist
        return False

    # remove from cart and update mongodb
    if product_id not in user_data['cart']:
        return False
    user_data['cart'].remove(product_id)
    db.users.update_one(filter=condition, update={'$set': user_data})

    return True


# return _id of products in a users cart
def retrieve_cart(user_id):
    condition = {'_id': ObjectId(user_id)}

    cursor = db.users.find(condition)

    if cursor.count() == 1:
        user_data = cursor[0]
        return user_data['cart']
    else:
        # user id does not exist
        return False
