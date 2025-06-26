from flask import Blueprint
from controllers.hello_controller import hello

hello_route = Blueprint('hello_route', __name__)

@hello_route.route('/api/hello')
def hello_route_handler():
    return hello()
