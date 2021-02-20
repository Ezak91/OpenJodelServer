from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Open Jodel API',
          version='1.0',
          description='a api for open jodel'
          )

api.add_namespace(user_ns, path='/user')
