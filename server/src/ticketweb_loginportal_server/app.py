import falcon

from .handlers import PubKeyHandler
from .handlers import LoginHandler



from .handlers import BadRequest




def main():
   api = falcon.App()
   api.add_route('/login/{url_key}', LoginHandler())
   api.add_route('/pubkey', PubKeyHandler())
   api.add_error_handler(BadRequest) 
   return api
