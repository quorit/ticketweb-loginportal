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
from .config_data import ldap_data
from .config_data import service_account_pw
from .config_data import rsa_key_data
import ldap
import binascii

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




if sys.base_prefix != sys.prefix:
    _data_path = sys.prefix + "/usr/local/share/ticketweb/loginportal/server-data"
else:
    _data_path = "/usr/local/share/ticketweb/loginportal/server-data"

def _get_shared_data():
    file = os.path.join(_data_path,"init_data.json")
    f = open(file,"r")
    shared_data = json.load(f)
    f.close()
    return shared_data

_shared_data = _get_shared_data()


def create_token(secret,net_id,real_name,email,duration):
     jti = binascii.b2a_base64(os.urandom(24)).decode().rstrip()
     exp_time = int(time.time()) + 60 * duration
     exp_time_english = time.ctime(exp_time)
     print (exp_time_english)
     jwt_payload = {
         'sub': net_id,
         'name': real_name,
         'email': email,
         'exp': exp_time,
         'jti': jti
     }
     headers = {
        'alg': "HS256",
        'typ': "JWT"
     }
     jwt_token = jwt.encode(jwt_payload, secret, algorithm='RS256')
     return jwt_token





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


def _get_json_string(obj,item_key,max_len):
    if item_key not in obj:
        raise br.MissingJSONItem(item_key)
    item = obj.get(item_key)
    if not isinstance(item,str):
        raise br.JSON_ItemNotString(item_key)
    if len(item) > max_len:
        raise br.StringTooBig(item_key)
    if len(item)==0:
        raise br.StringCannotBeEmpty(item_key)
    return item


def _get_user_data(ldap_handle,userid,attributes):
    search_base=ldap_data["search_base"]
    try:        
        ldap_search_result = ldap_handle.search_s(search_base,ldap.SCOPE_SUBTREE,"(sAMAccountName={0})".format(userid),attributes)
    except ldap.LDAPError as e:
        raise falcon.HTTPInternalServerError(description="Ldap failure: " + str(e))

    result_attributes = ldap_search_result[0][1]
    result_dict = {}
    for attribute in attributes:
        result_dict[attribute]=result_attributes[attribute][0].decode(encoding='utf-8', errors='strict')
    user_dn = ldap_search_result[0][0]
    if not user_dn:
        raise falcon.HTTPBadRequest(
            title="User not found in LDAP Search",
            description="User not found in LDAP Search"
        )
    return (user_dn,result_dict)



class LoginHandler ():



    def on_post(self,req,resp,url_key):

        content_len = req.content_length
        if content_len==0:
            raise br.NoContentReceived()
        if content_len > 1000:
            raise br.ContentTooLarge()
        try:
            req_content = json.load(req.stream)

        except json.decoder.JSONDecodeError as e:
            raise falcon.HTTPBadRequest({
                "description": "Failed to decode json"
            })
        
        user_id = _get_json_string(req_content,"user_id",255)
        re_pattern = r"^[0-9a-z]+$|^ad(\.queensu.ca){0,1}\\[0-9a-z]+$|^[0-9a-z]+@ad\.queensu\.ca$"
        if not re.search(re_pattern,user_id,flags=re.IGNORECASE):
             raise br.JSONBadFormatUserId()
        userid = _canonicalise_userid(user_id)
        password = _get_json_string(req_content,"password",255)
        url = ldap_data["url"]

        try:
            ldap_handle  = ldap.initialize(url)

            service_account_dn = ldap_data["dn"]
            search_base=ldap_data["search_base"]

            ldap_handle.simple_bind_s(service_account_dn,service_account_pw)

            ldap_handle.set_option(ldap.OPT_REFERRALS, 0)
        except ldap.LDAPError as e:
            raise falcon.HTTPInternalServerError(description="Ldap failure: " + str(e))
        (user_dn,user_data) = _get_user_data(ldap_handle,userid,["displayName","mail"])
        try:
             ldap_handle.simple_bind_s(user_dn,password)
             # The success of this tests the user's password
        except ldap.INVALID_CREDENTIALS:
            raise falcon.HTTPUnauthorized()
        except ldap.LDAPError as e:
            raise falcon.HTTPInternalServerError(description="Ldap failure: " + str(e))
        priv_key = rsa_key_data["private_key"]
        token = create_token(priv_key,userid,user_data["displayName"],user_data["mail"],15)
        response_json = {
            "jwt": token,
            "forward_url": _shared_data[url_key]
        }
        print(response_json)
        resp.text = json.dumps(response_json)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_CREATED
   



class PubKeyHandler():
    def on_get(self,req,resp):
        resp.text = rsa_key_data["public_key_pem"]
        resp.content_type = falcon.MEDIA_TEXT
        resp.status = falcon.HTTP_OK
