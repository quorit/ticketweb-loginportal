import falcon

from .handlers import UserData
from .handlers import SubmitTicketRptSupport
from .handlers import SubmitTicketStudent
from .handlers import SubmitTicketAdmissions


from .handlers import BadRequest





def main():
   api = falcon.App()
   api.add_route('/user-data', UserData())
   api.add_route('/submit-ticket/student', SubmitTicketStudent())
   api.add_route('/submit-ticket/admissions', SubmitTicketAdmissions())
   api.add_route('/submit-ticket/rptsupport', SubmitTicketRptSupport())
   api.add_error_handler(BadRequest) 
   return api
