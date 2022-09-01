import falcon
import jwt
import json
import re
import time
import os
import ldap
import sys
import requests
import urllib
import html
import tempfile
from requests_toolbelt.multipart.encoder import MultipartEncoder
from contextlib import ExitStack




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




def _get_user_id_from_jwt_data(req):
    receive = requests.get(_config_data["pub_key_url"])
    if receive.status_code != 200:
            raise Exception("Failed commmunication with token server")
    pub_key=receive.text

    req_auth_hdr = req.get_header('Authorization')
    if not req_auth_hdr:
        raise BadRequestMissingHeader('Authorization')
    if len(req_auth_hdr) > 2048:
        raise BadRequestHeaderTooBig()
    re_pattern = r"^Bearer [-a-zA-Z0-9._]+$"
    if not re.search(re_pattern,req_auth_hdr):
        raise BadRequestHeaderBadFormatJWT()
    req_token = req_auth_hdr[len("Bearer "):]
    try:
        req_decoded = jwt.decode(
                req_token,pub_key,
                algorithms=['RS256'],
                options={"require": ["user_id","exp"]})
    except jwt.exceptions.ExpiredSignatureError as e:
        raise BadRequestExpiredToken()
    except jwt.exceptions.InvalidTokenError as e:
        # note that if the exp part of the claim has expired an exception will be thrown
        # (That test is built in)
        raise BadRequestInvalidJWT_Token() from e
    user_id = req_decoded['user_id']
    if not isinstance(user_id,str):
        raise BadRequestRoleNotString()
    return user_id



def create_token(secret,user_id, duration):

     exp_time = int(time.time()) + 60 * duration
     exp_time_english = time.ctime(exp_time)
     jwt_payload = {
         'user_id': user_id,
         'exp': exp_time
     }
     headers = {
        'alg': "HS256",
        'typ': "JWT"
     }
     jwt_token = jwt.encode(jwt_payload, secret, algorithm='HS256')
     return jwt_token



def create_response_body_user_data(display_name,mail):
    return {
            "display_name": display_name,
            "mail": mail
        }




def _canonicalise_userid(userid):
    userid_local = userid.lower()
    re_pattern = r"^[0-9a-z]+$"
    if re.search(re_pattern,userid_local):
        return userid_local
    re_pattern = r"^ad(\.queensu.ca){0,1}\\[0-9a-z]+$"
    if re.search(re_pattern,userid_local):
        return userid_local.split("\\")[1]
    re_pattern = r"^[0-9a-z]+@ad\.queensu\.ca$"
    if re.search(re_pattern,userid_local):
        return userid_local.split("@")[0]
     



if sys.base_prefix != sys.prefix:
    etc_path = sys.prefix + "/etc"
else:
    etc_path = "/etc"




def _get_config_data_all():
    print(etc_path)
    ldap_file = os.path.join(etc_path,"ticketweb/applications/reporting/config.json")

    f = open(ldap_file,"r")
    ldap_data = json.load(f)
    f.close()
    return ldap_data


_config_data = _get_config_data_all()


def _get_rt_api_token():
    api_token_exec = _config_data["rt"]["api_token_exec"]
    api_token = os.popen(api_token_exec).read()
    return api_token


_rt_api_token = _get_rt_api_token()




def _get_pw():
    password_exec = _config_data["ldap"]["password_exec"]
    pw = os.popen(password_exec).read()
    return pw


_service_account_pw = _get_pw()




def _get_ldap_handle():
        ldap_data = _config_data["ldap"]
        url = ldap_data["url"]
        ldap_handle  = ldap.initialize(url)
        service_account_dn = ldap_data["dn"]
        ldap_handle.simple_bind_s(service_account_dn,_service_account_pw)
        return ldap_handle


def _get_user_data(attributes,req):
    user_dn = _get_user_id_from_jwt_data(req)
    ldap_handle = _get_ldap_handle()
    ldap_handle.set_option(ldap.OPT_REFERRALS, 0)
    ldap_search_result = ldap_handle.search_s(user_dn,ldap.SCOPE_SUBTREE,"objectclass=*",attributes)
    if not user_dn:
            raise BadRequestUserNotFound(user_dn)
    result_attributes = ldap_search_result[0][1]
    result_dict = {}

    for attribute in attributes:
        result_dict[attribute]=result_attributes[attribute][0].decode(encoding='utf-8', errors='strict')
    return result_dict






class UserData ():

    def on_get(self,req,resp):
        user_data = _get_user_data(["displayName","mail"],req)
        response_body = create_response_body_user_data(user_data["displayName"],user_data["mail"])
        print(response_body)
        resp.text=json.dumps(response_body)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK


# def get_req_content(req):
#    if req.content_length == 0:
#        raise BadRequestNoContentReceived()
#    req_content = json.load(req.stream)
#    return req_content
#    #need more tests. is content too large? does it actually parse



class SubmitTicket():
    def __init__(self,report_type,get_subject,get_ticket_content):
        self.report_type=report_type
        self.get_subject=get_subject
        self.get_ticket_content=get_ticket_content
    

    






    def on_post(self,req,resp):
        def get_req_content(req,tempdir):
            # Might want to test that content isn't too big here
            if not req.content_type.startswith(falcon.MEDIA_MULTIPART):
                raise BadRequestContentNotMultipart()
            parts = req.get_media()
            attachments = []
            json_part = None
            attach_count = 0
            for part in parts:
                if part.name == 'json':
                    if json_part:
                        raise BadRequestMultipleContentParts()
                    if part.content_type != falcon.MEDIA_JSON:
                        raise BadRequestContentNotJson()
                    # if part.content_length == 0:
                    #    raise BadRequestNoContentReceived()
                    # testing for content_lenght probably won't work because
                    # we probably won't have content length headers in the parts
                    # In fact it's not a good test because it might not actually
                    # be the same as the real content length.
                    json_part = json.load(part.stream)
                elif part.name == 'attachment':
                    tmp_filename = os.path.join(tempdir,str(attach_count))
                    tmp_file_s = open(tmp_filename, 'wb')
                    try:
                        part.stream.pipe(tmp_file_s)
                    finally:
                        tmp_file_s.close()
                    attachments.append({
                        "filename": part.filename,
                        "content_type": part.content_type
                    })
                    attach_count = attach_count + 1
            return {
                "json": json_part,
                "attachments": attachments
            }

        def get_due_date_rt(due_date):
            return time.strftime("%Y-%m-%d %H:%M:%S" ,
                                    time.gmtime(time.mktime(time.strptime(due_date + " 23:59:59",
                                    "%Y-%m-%d %H:%M:%S"))))
    # need to throw bad requestrs if the due date is unparseable.

        user_data = _get_user_data(["displayName","mail","sAMAccountName"],req)
        #For other form types this comes out of the request
        


        rt_path_base = _config_data["rt"]["path_base"]
        auth_string = "Token " + _rt_api_token

        headers = {
            "Authorization": auth_string
        }
        mail = user_data["mail"]

        mail_enc = urllib.parse.quote(mail)
        rt_path= rt_path_base + "REST/2.0/"
        print (rt_path + "user/" + mail_enc)
        receive = requests.get(rt_path + "user/" + mail_enc,headers=headers)
        
        current_user_name = None

        if receive.status_code == 200:
            current_user_name = mail_enc
        elif receive.status_code == 404:
            receive = requests.get(rt_path + "user/" + user_data["sAMAccountName"],headers=headers)
            if receive.status_code == 200:
                current_user_name = user_data["sAMAccountName"]
            elif receive.status_code != 404:
                raise Exception("Failed RT communication")
        else:
            raise Exception("Failed RT communication")
            # this will result in a 500 error for the user
            # which is appropriate if this happens
        
        user_fields = {
            "RealName": user_data["displayName"],
            "Name": user_data["sAMAccountName"],
            "EmailAddress": mail
        }
        
        headers = {
            "Authorization": auth_string,
            "Content-Type": "application/json"
        }

        if not current_user_name:
            receive = requests.post(rt_path + "user",headers=headers,json=user_fields)
        else:
            url = rt_path+"user/"+current_user_name
            receive = requests.put(url,
                                   headers=headers,
                                   json=user_fields)
        


        if receive.status_code not in [200,201]:
            print (receive.status_code)
            raise Exception("Failed RT commmunication")


        with tempfile.TemporaryDirectory() as temp_dir:
            req_content = get_req_content(req,temp_dir)
            json_part = req_content["json"]
            due_date_rt = get_due_date_rt(json_part["due_date"])
            real_name = user_data["displayName"]
            ticket_content = self.get_ticket_content(real_name,json_part)
            attachments = req_content["attachments"]
            subject = self.get_subject(json_part)

            internal_req_content = {
                "Requestor": mail,
                "Subject": subject,
                "Queue": _config_data["rt"]["queue"],
                "CustomFields": {
                    "RequestType": self.report_type
                },
                "Content": ticket_content,
                "ContentType": "text/html",
                "Due": due_date_rt

            }

            print(internal_req_content)

            mp_fields = [ 
                            ('JSON', (None, json.dumps(internal_req_content)))
                        ]



            with ExitStack() as stack:
                # See https://stackoverflow.com/questions/4617034/how-can-i-open-multiple-files-using-with-open-in-python
                # for why exitstack is being used
                # Note that if you do
                #
                # with open(file) as f:
                #   blah
                #
                # f will always be closed no matter what,
                # it's the same as doing:
                #
                # f = open(file)
                # try:
                #    do blah
                # finally:
                #    f.close()
                #
                # Either of these work for just one file,
                # but what if i have an abitrary length list?
                # this is where ExitStack comes in.
                # If something should go wrong in the below code,
                # all of the streams added to the exit stack will be guaranteed closed.


                for attach_count in range(len(attachments)):
                    srcfile = os.path.join(temp_dir,str(attach_count))
                    stream = open(srcfile,'rb')
                    stack.enter_context(stream)
                    attachment = attachments[attach_count]
                    filename = attachment["filename"]
                    content_type = attachment["content_type"]
                    mp_fields.append(('Attachments',(filename,stream,content_type)))
            


                mp_encoder = MultipartEncoder(
                    fields = mp_fields
                )

                headers = {
                    "Authorization": auth_string,
                    "Content-Type": mp_encoder.content_type,
                }


                receive = requests.post(rt_path + "ticket",
                                        headers=headers,
                                        data=mp_encoder)


        if receive.status_code != 201:
            raise Exception("Failed RT commmunication")
        resp.text=receive.text
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK






def _get_subject(req_content):
    return req_content["subject"]








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

        super().__init__("rptsupport",get_subject,get_ticket_content)



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
        super().__init__("student",get_subject,get_ticket_content)




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

        super().__init__("admissions",get_subject,get_ticket_content)

