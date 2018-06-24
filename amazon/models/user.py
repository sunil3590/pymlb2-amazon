from amazon.models import db


def __search_by_username(username):
    # lets search for the user here
    query = {'username': username}
    matching_user = db['users'].find(query)
    if matching_user.count() > 0:
        return matching_user.next()
    else:
        return None


def signup_user(name, username, password):
    existing_user = __search_by_username(username)
    if existing_user is not None:
        return False
    user = {
        'name': name,
        'username': username,
        'password': password
    }
    db['users'].insert_one(user)
    return True


def authenticate(username, password):
    user = __search_by_username(username)

    if user is None:
        # user does not exist
        return False

    if user['password'] == password:
        # user exists and correct password
        return True
    else:
        # user exists but wrong password
        return False
