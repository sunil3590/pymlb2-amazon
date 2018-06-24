from flask import Flask

# create the app
app = Flask('amazon')

# import api to invoke it and configure the app
from amazon import api
