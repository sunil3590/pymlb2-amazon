from amazon.models import db


def search_by_name(name):
    # lets search for the product here
    query = {'name': name}
    matching_products = db['products'].find(query)
    return list(matching_products)


def add_product(product):
    db['products'].insert_one(product)


def update_product(name, updated_product):
    # create filter and update dicts
    filter = {'name': name}
    update = {
        '$set': updated_product
    }

    # update in DB
    db['products'].update_one(filter=filter, update=update)