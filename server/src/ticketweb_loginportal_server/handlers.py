import falcon
import jwt
import json
import re
import time
import os
from .config_data import config_data
from .config_data import ldap_data
from .config_data import service_account_pw
from .config_data import rsa_key_data
import ldap
import binascii




def create_token(secret,net_id,real_name,email,duration):
     jti = binascii.b2a_base64(os.urandom(24)).decode().rstrip()
     exp_time = int(time.time()) + 60 * duration
     exp_time_english = time.ctime(exp_time)
     print (exp_time_english)
     jwt_payload = {
         'upn': net_id + '@' + "queensu.ca",
         'name': real_name,
         'email': email,
         'exp': exp_time,
         'uti': jti,
         'aud': "ticketweb_auth_server",
         'iss': "ticketweb_portal"
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
        raise falcon.HTTPBadRequest(
            description="Missing JSON item:" + item_key
        )
    item = obj.get(item_key)
    if not isinstance(item,str):
        raise falcon.HTTPBadRequest (
            description="JSON Field {0} is not a string".format(item_key)
        )
    if len(item) > max_len:
        raise falcon.HTTPBadRequest (
            description="JSON Field {0} is too long".format(item_key)
        )
    if len(item)==0:
        raise falcon.HTTPBadRequest (
            description="JSON Field {0} cannot be empty".format(item_key)
        )
    return item


def _get_user_data(ldap_handle,userid):
    search_base=ldap_data["search_base"]
    attributes = ["displayName","proxyAddresses"]
    try:        
        ldap_search_result = ldap_handle.search_s(search_base,ldap.SCOPE_SUBTREE,"(sAMAccountName={0})".format(userid),attributes)
    except ldap.LDAPError as e:
        raise falcon.HTTPInternalServerError(description="Ldap failure: " + str(e))

    user_dn = ldap_search_result[0][0]
    if not user_dn:
        raise falcon.HTTPBadRequest(
            title="User not found in LDAP Search",
            description="User not found in LDAP Search"
        )
    result_attributes = ldap_search_result[0][1]
    print (result_attributes)
    result_dict = {}
    result_dict["display_name"] = result_attributes["displayName"][0].decode(encoding='utf-8', errors='strict')
    proxy_addresses = result_attributes["proxyAddresses"]
    result_dict["primary_email"] = get_primary_email(proxy_addresses)

    # for attribute in attributes:
    #    result_dict[attribute]=result_attributes[attribute][0].decode(encoding='utf-8', errors='strict')
    return (user_dn,result_dict)

def get_primary_email(proxy_addresses):
    # 1. Handle ldap3 Attribute objects explicitly
    if hasattr(proxy_addresses, 'values'):
        proxy_addresses = proxy_addresses.values
        
    if not proxy_addresses:
        return None

    for address in proxy_addresses:
        # 2. Handle bytes vs strings
        if isinstance(address, bytes):
            address = address.decode('utf-8')
        
        # 3. Use case-insensitive check
        # Primary is 'SMTP:', secondary is 'smtp:'
        if address.startswith('SMTP:'):
            return address[5:] # More efficient than replace()

    return None

# Example Usage:
# ldap_proxy_list = ['smtp:alias@company.com', 'SMTP:primary@company.com', 'smtp:hr@company.com']
# primary = get_primary_email(ldap_proxy_list)

# print(f"Primary Email: {primary}")

class LoginHandler ():



    def on_post(self,req,resp):

        content_len = req.content_length
        if content_len==0:
            raise falcon.HTTPBadRequest(
                description="No Content received in request"
            )
        if content_len > 1000:
            raise falcon.HTTPRequestEntityTooLarge(
                description="No Content received in request"
            )
        try:
            req_content = json.load(req.stream)

        except json.decoder.JSONDecodeError as e:
            raise falcon.HTTPBadRequest(
                description = "Failed to decode json"
            )
        
        user_id = _get_json_string(req_content,"user_id",255)
        re_pattern = r"^[0-9a-z]+$|^ad(\.queensu.ca){0,1}\\[0-9a-z]+$|^[0-9a-z]+@ad\.queensu\.ca$"
        if not re.search(re_pattern,user_id,flags=re.IGNORECASE):
             raise falcon.HTTPBadRequest(
                 description= "'user_id' JSON item does not have correct format."
             )
        userid = _canonicalise_userid(user_id)
        # password = _get_json_string(req_content,"password",255)
        url = ldap_data["url"]

        try:
            # WARNING: This makes the connection insecure!
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            #please try to fix this asap
            ldap_handle  = ldap.initialize(url)

            service_account_dn = ldap_data["dn"]
            search_base=ldap_data["search_base"]
            print (service_account_pw)
            ldap_handle.simple_bind_s(service_account_dn,service_account_pw)
            print ("hello hello 2")
            ldap_handle.set_option(ldap.OPT_REFERRALS, 0)
        except ldap.LDAPError as e:
            raise falcon.HTTPInternalServerError(description="Ldap failure: " + str(e))
        (user_dn,user_data) = _get_user_data(ldap_handle,userid)
        print ("USER DATA FOLLOWS")
        print (user_data)
        print (user_data["primary_email"])
        print ("Natalie whatever")
        # try:
        #     
        #     print ("hello hello")
        #     ldap_handle.simple_bind_s(user_dn,password)
        #     # The success of this tests the user's password
        #except ldap.INVALID_CREDENTIALS:
        #    raise falcon.HTTPUnauthorized()
        #except ldap.LDAPError as e:
        #    raise falcon.HTTPInternalServerError(description="Ldap failurze: " + str(e))
        
        priv_key = rsa_key_data["private_key"]
        token = create_token(priv_key,userid,user_data["display_name"],
                              user_data["primary_email"],15)
        resp.text = token
        resp.content_type = falcon.MEDIA_TEXT
        resp.status = falcon.HTTP_CREATED
   



class PubKeyHandler():
    def on_get(self,req,resp):
        resp.text = rsa_key_data["public_key_pem"]
        resp.content_type = falcon.MEDIA_TEXT
        resp.status = falcon.HTTP_OK
