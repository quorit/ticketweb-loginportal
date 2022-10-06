import falcon
import jwt
import json
import re
import time
import os
import sys
import requests
import html
from ticketweb_rt_interface.handlers import SubmitTicket
from .config_data import config_data

class BadRequest(Exception):
    def __init__(self,message,status):
       self._message = message
       self.status = status

    def response_body(self):
       result = {
                  'message': self._message
                }
       cause = self.__cause__
       if cause:
          result['exception'] = str(cause)
       return result

    @staticmethod                     # This is like static in java
    def handle(e, req, resp, params): # These paramaters are required even though I'm only using resp and e
        resp.body = json.dumps(e.response_body())
        resp.status = e.status
        resp.content_type = falcon.MEDIA_JSON
    # i believe this function is a static because that allows me to refer to it even
    # when I don't have an object. I am registering the function with add_error_handler
    # and at that time no object is relevant




class BadRequestHeaderTooBig(BadRequest):
    def __init__(self):
         message = "'Authorization' header is too big"
         status = falcon.HTTP_REQUEST_HEADER_FIELDS_TOO_LARGE
         super().__init__(message,status)

class BadRequestHeaderBadFormatJWT(BadRequest):
    def __init__(self):
         message = "'Authorization' header does not have format, 'Bearer <jwt token>'"
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)

class BadRequestHeaderBadFormatUserId(BadRequest):
    def __init__(self):
        message = "'UserId' header does not have correct format."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)


class BadRequestHeaderBadFormatOTP(BadRequest):
    def __init__(self):
        message = "'OTP' header does not have correct format."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)



class BadRequestHeaderBadFormatGSSAPI(BadRequest):
    def __init__(self):
         message = "'Authorization' header does not have format, 'Negotiate <token encoding>'"
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)


class BadRequestExpiredToken(BadRequest):
    def __init__(self):
         message = "Token has expired."
         status = falcon.HTTP_UNAUTHORIZED # really means "unathenticated" in HTTP-speak
         super().__init__(message,status)

class BadRequestUnrecognizedMinion(BadRequest):
    def __init__(self,minion_id):
         message_fmt = "Unrecognized minion, {0}."
         message = message_fmt.format(minion_id)
         status = falcon.HTTP_UNAUTHORIZED # really means "unathenticated" in HTTP-speak
         super().__init__(message,status)

class BadRequestInvalidJWT_Token(BadRequest):
    def __init__(self):
         message = "Token is not valid."
         status = falcon.HTTP_BAD_REQUEST 
         super().__init__(message,status)

class BadRequestInvalidGSS_Token(BadRequest):
    def __init__(self):
         message = "GSS token is not valid."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)




class BadRequestRoleNotString(BadRequest):
    def __init__(self):
         message = "'role' field field in token payload is not a string."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)


class BadRequestContextNotString(BadRequest):
    def __init__(self):
         message = "'context' field field in token payload is not a string."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)


class BadRequestBadRoleName(BadRequest):
    def __init__(self):
         message =  "'role' field in token payload does not match pattern <computer_account_name>$@queensu.ca."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)

class BadRequestMissingHeader(BadRequest):
     def __init__(self,header):
          message = "'{0}' header is missing from the request.".format(header)
          status = falcon.HTTP_BAD_REQUEST
          super().__init__(message,status)

class BadRequestUnsupportedMechanism(BadRequest):
     def __init__(self):
          message = "GSSAPI Error: Unsupported mechanism requested."
          status = falcon.HTTP_BAD_REQUEST
          super().__init__(message,status)

class BadRequestBadQueryString(BadRequest):
     def __init__(self):
          message = "Unsupported query string for this route."
          status = falcon.HTTP_BAD_REQUEST
          super().__init__(message,status)

class BadRequestContextMismatch(BadRequest):
    def __init__(self):
        message = "Mismatching contexts."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)


class BadRequestLDAPAuthFail(BadRequest):
    def __init__(self):
        message = "LDAP authentication fail."
        status = falcon.HTTP_UNAUTHORIZED
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)


class BadRequestSecretFileIOFail(BadRequest):
    def __init__(self):
        message = "Could not open OTP secret file for user."
        status = falcon.HTTP_INTERNAL_SERVER_ERROR
        super().__init__(message,status)


class BadRequestInvalidOTP(BadRequest):
    def __init__(self):
        message = "Invalid OTP code."
        status = falcon.HTTP_UNAUTHORIZED
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)

class BadRequestUnknownContext(BadRequest):
    def __init__(self, context):
        message = "Uknown application context, {0}".format(context)
        status = falcon.HTTP_BAD_REQUEST
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)

class BadRequestUserNotFound(BadRequest):
    def __init__(self, user_id):
        message = "Failed to find user '{0}' in LDAP db.".format(user_id)
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)

class BadRequestNoContentReceived(BadRequest):
    def __init__(self):
        message = "No content received in request."
        status = falcon.HTTP_BAD_REQUEST
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)

class BadRequestMultipleContentParts(BadRequest):
    def __init__(self):
        message = "Multiple parts with the 'json' name have been sent."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)


class BadRequestContentNotJson(BadRequest):
    def __init__(self):
        message = "Part with the 'json' name cannot have mime type other than 'application/json'."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)

class BadRequestContentNotMultipart(BadRequest):
    def __init__(self):
        message = "The request cannot have a type other than 'multipart/form-data'."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)





def create_response_body_user_data(display_name,mail):
    return {
            "display_name": display_name,
            "mail": mail
        }







def _build_dtdd(title, data):
    return "<dt>" + title + ":</dt><dd>" + html.escape(data) + "</dd>"

if sys.base_prefix != sys.prefix:
    _data_path = sys.prefix + "/usr/local/share/ticketweb/applications/reporting/shared-data"
else:
    _data_path = "/usr/local/share/ticketweb/applications/reporting/shared-data"

def _get_shared_data():
    file = os.path.join(_data_path,"init_data.json")
    f = open(file,"r")
    shared_data = json.load(f)
    f.close()
    return shared_data

_shared_data = _get_shared_data()


def _build_requested_before(prev_report_info):
    if not prev_report_info:
        result = _build_dtdd("Requested Before","No")
    else:
        result = _build_dtdd("Requested Before","Yes") + \
                  _build_dtdd("Previous Report Info",prev_report_info)
    return result






def _build_terms(heading,terms):
    def term_lookup(term):
        last_digit = term[-1]
        base_year= 1901
        base_strm= 1011
        season_lookup = {
            "1": "Winter",
            "5": "Summer",
            "9": "Fall"
        }
        season = season_lookup[last_digit]
        term_int = int(term)
        (year_delta,remainder) = divmod(term_int-base_strm,10)
        year_int = base_year + year_delta
        return str(year_int) + " " + season

    result = "<dt>" + heading + ":</dt>" \
             + "<dd><ul style='padding-left:0;'>" \
             + "".join(["<li>" + term_lookup(term) + " (" + term + ")</li>" for term in terms]) \
             + "</ul></dd>"

    return result


def _build_list_choices(list_choices):
    def build_list_choice(item):
        choices = list_choices[item]
        list_def = _shared_data["data_lists"][item]
        header = list_def["heading"]
        result = "<dt>" + header + ":</dt>" \
                 + "<dd><ul style='padding-left:0;'>" \
                 + "".join(["<li>" + list_def["items"][choice] + "</li>" for choice in choices]) \
                 + "</ul></dd>"
        return result

    result  = "".join([build_list_choice(item) for item in list_choices])
    return result

def _build_requested_fields(requested_fields):
    result = "<dt>Requested Fields:</dt><dd><ul style='padding-left:0;'>" \
             + "".join(["<li>" + field + "</li>" for field in requested_fields]) \
             + "</ul></dd>"
    return result



class SubmitTicketRptSupport(SubmitTicket):
    def __init__(self):
        def get_subject(req_content):
            return "Data support request"

        def get_ticket_content(real_name,req_content):
            source_choice = req_content["source_choice"]
            if source_choice["rpt_source_type"] == "standard":
                report_txt = _shared_data["data_support_choices"][source_choice["source_key"]]
            else:
                report_txt = source_choice["description"]
            result = "<dl>" \
                      + _build_dtdd("Request Type","Data support") \
                      + _build_dtdd("Requestor Name",real_name)  \
                      + (_build_dtdd("Requestor Department", req_content["requestor_dept"]) if "requestor_dept" in req_content else "") \
                      + _build_dtdd("Due Date",req_content['due_date']) \
                      + (_build_dtdd("Requestor Position",req_content["requestor_position"]) \
                               if "requestor_position" in req_content else "") \
                      + _build_dtdd("Report Source",report_txt) \
                      + _build_dtdd("Problem Description",req_content["support_request_descr"]) \
                      + "</dl>"
            return result

        super().__init__("rptsupport",get_subject,get_ticket_content,config_data)



class SubmitTicketStudent(SubmitTicket):
    def __init__(self):
        def get_subject(req_content):
            return req_content["subject"]

        def get_ticket_content(real_name,req_content):
            def build_progs(progs_selected):
                def build_common_progs(common_progs):
                    def build_common_faculty(common_progs,faculty):
                        def build_prog(progs,prog):
                            def build_subprogs(subprogs):
                                if subprogs is True:
                                    result = ": <i>All</i>"
                                elif isinstance(subprogs,list) and len(subprogs) > 0:
                                    result = ":<ul>" \
                                    + "".join(["<li>" + html.escape(subprogs[i]) + "</li>" for i in range(len(subprogs))]) \
                                    + "</ul>"
                                else:
                                    result = ""
                                return result              
                            subprogs = progs[prog]
                            result = _shared_data["faculties_student"][faculty]["progs"][prog]["longhand"] \
                                     + build_subprogs(subprogs)
                            return result
                        progs = common_progs[faculty]
                        result = faculty + ":<ul>" \
                                 +  "".join([ "<li>" + build_prog(progs,prog) + "</li>" for prog in progs]) \
                                 + "</ul>"
                        return result
                    # here
                    result = "Commonly requested programs:<ul>" \
                           + "".join(["<li>" + build_common_faculty(common_progs,faculty) + "</li>" for faculty in common_progs]) \
                           + "</ul>"
                    return result
                def build_other_plans_progs(other_plansprogs):
                    result = "Other programs and plans:<ul>" \
                            + "".join(["<li>" + html.escape(progplan) + "</li>" for progplan in other_plansprogs]) \
                            + "</ul>"
                    return result
                result = "<dt>Programs and Plans:</dt><dd><ul style='padding-left:0;'>" \
                         + ("<li>" + build_common_progs(progs_selected["common_progs"]) + "</li>" if "common_progs" in progs_selected \
                                                                               else "") \
                         + ("<li>" + build_other_plans_progs(progs_selected["other_plans_progs"]) + "</li>" if \
                               "other_plans_progs" in progs_selected else "") \
                         + "</ul></dd>"
                return result
            result = "<dl>" \
                     + _build_dtdd("Request Type","Student data") \
                     + _build_dtdd("Subject",req_content["subject"]) \
                     + _build_dtdd("Requestor Name",real_name) \
                     + (_build_dtdd("Requestor Department", req_content["requestor_dept"]) if "requestor_dept" in req_content \
                            else "") \
                     + _build_dtdd("Due Date",req_content['due_date']) \
                     + (_build_dtdd("Requestor Position",req_content["requestor_position"]) if "requestor_position" in req_content \
                             else "") \
                     + _build_requested_before(req_content.get("prev_report_info")) \
                     + _build_dtdd("Report Purpose",req_content["report_purpose"]) \
                     + (_build_terms("Terms",req_content["terms"]) if "terms" in req_content else "") \
                     + (build_progs(req_content["progs"]) if "progs" in req_content else "") \
                     + (_build_list_choices(req_content["list_choices"]) if "list_choices" in req_content else "") \
                     + (_build_dtdd("Extra Details",req_content["extra_details"]) \
                         if "extra_details" in req_content else "") \
                     + _build_requested_fields(req_content["requested_fields"]) \
                     + "</dl>"
            return result
        super().__init__("student",get_subject,get_ticket_content,config_data)




class SubmitTicketAdmissions(SubmitTicket):
    def __init__(self):
        def get_subject(req_content):
            return req_content["subject"]

        def get_ticket_content(real_name,req_content):
            def build_progs(progs_selected):
                def build_first_year(progplans):
                    def build_faculty(faculty):
                        progs = progplans[faculty]
                        result = faculty + ":<ul>" \
                                  + "".join(["<li>" + _shared_data["faculties"][faculty][prog] + "</li>" for prog in progs]) \
                                  + "</ul>"
                        return result
                    result = "First year:<ul>" \
                             + "".join(["<li>" + build_faculty(faculty) + "</li>" for faculty in progplans]) \
                             + "</ul>"
                    return result
                def build_upper_year(progplans):
                    result = "Upper year:<ul>" \
                             + "".join(["<li>" + progplan + "</li>" for progplan in progplans]) \
                             + "</ul>"
                    return result
                result = "<dt>Programs:</dt><dd><ul style='padding-left:0;'>" \
                         + ("<li>" + build_first_year(progs_selected["first_year"]) + "</li>" \
                               if "first_year" in progs_selected else "") \
                         + ("<li>" + build_upper_year(progs_selected["upper_year"]) + "</li>" \
                               if "upper_year" in progs_selected else "") \
                         + "</ul></dd>" 
                return result    
            result = "<dl>" \
                     + _build_dtdd("Request Type","Applicant data") \
                     + _build_dtdd("Subject",req_content["subject"]) \
                     + _build_dtdd("Requestor Name",real_name) \
                     + (_build_dtdd("Requestor Department", req_content["requestor_dept"]) if "requestor_dept" in req_content \
                            else "") \
                     + _build_dtdd("Due Date",req_content['due_date']) \
                     + (_build_dtdd("Requestor Position",req_content["requestor_position"]) if "requestor_position" in req_content \
                             else "") \
                     + _build_requested_before(req_content.get("prev_report_info")) \
                     + _build_dtdd("Report Purpose",req_content["report_purpose"]) \
                     + _build_terms("Admit Terms",req_content["terms"]) \
                     + build_progs(req_content["progs"]) \
                     + _build_list_choices(req_content["list_choices"]) \
                     + (_build_dtdd("Extra Details",req_content["extra_details"]) \
                         if "extra_details" in req_content else "") \
                     + _build_requested_fields(req_content["requested_fields"]) \
                     + "</dl>"
            return result

        super().__init__("admissions",get_subject,get_ticket_content,config_data)

