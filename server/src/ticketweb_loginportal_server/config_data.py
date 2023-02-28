import sys
import json
import os
from cryptography.hazmat.primitives import serialization

if sys.base_prefix != sys.prefix:
    _etc_path = sys.prefix + "/etc"
else:
    _etc_path = "/etc"




def _get_config_data_all():
    ldap_file = os.path.join(_etc_path,"ticketweb/loginportal/server-config.json")

    f = open(ldap_file,"r")
    ldap_data = json.load(f)
    f.close()
    return ldap_data


config_data = _get_config_data_all()


print(config_data)

ldap_data = config_data["ldap"]



def _init_rsa_key_data():
    key_file = os.path.join(_etc_path,"ticketweb","loginportal","secret.pem")
    # I need to generate a table of of pairs.
    # first member of each pair is priv key, that i can use to encode with
    # second member is a serilisation of a public key that I can export through the web api
    # to an application server.
    # note that with these keys, pub keys are fully determinable from priv keys.
    # the files we are reading in are serializations of priv keys.

        # read in the priv-key serialisation (pem) file for that application
    f = open(key_file,"rb")
    private_key = serialization.load_pem_private_key(
                                                        f.read(),
                                                        password=None,
                                                    )
    f.close()
    pub_key = private_key.public_key()
    pub_key_bytes = pub_key.public_bytes(
                                            encoding=serialization.Encoding.PEM,
                                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                                        )
    pub_key_pem = pub_key_bytes.decode()
    result = {
                    "private_key": private_key,
                    "public_key_pem": pub_key_pem
            }
    return result




rsa_key_data = _init_rsa_key_data()



ldap_data = config_data["ldap"]



def _get_pw():
    password_exec = config_data["ldap"]["password_exec"]
    pw = os.popen(password_exec).read()
    return pw


service_account_pw = _get_pw()