from flask import Flask

# create the app
app = Flask('amazon')

app.secret_key = 'some_secret'

# import api to invoke it and configure the app
from amazon import api
