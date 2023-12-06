from flask import Flask
from flask_restx import Api
from methods.poke_methods import api, ns as namespace
from database.poke_database import db

app=Flask(__name__)
api.init_app(app)
api.add_namespace(namespace)


if __name__ == '__main__':
    app.run(debug=True)







