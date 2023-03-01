import falcon

from .handlers import PubKeyHandler
from .handlers import LoginHandler








def main():
   api = falcon.App()
   api.add_route('/login/{url_key}', LoginHandler())
   api.add_route('/pubkey', PubKeyHandler())
   return api
