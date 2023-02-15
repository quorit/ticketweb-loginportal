import falcon

from .handlers import SubmitTicketRptSupport
from .handlers import SubmitTicketStudent
from .handlers import SubmitTicketAdmissions


from .handlers import BadRequest
from .config_data import config_data




def main():
   api = falcon.App()
   api.add_route('/submit-ticket/student', SubmitTicketStudent())
   api.add_route('/submit-ticket/admissions', SubmitTicketAdmissions())
   api.add_route('/submit-ticket/rptsupport', SubmitTicketRptSupport())
   api.add_error_handler(BadRequest) 
   return api
