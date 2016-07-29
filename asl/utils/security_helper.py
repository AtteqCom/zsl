from asl.application.service_application import AtteqServiceFlask
from asl.utils.injection_helper import inject
import hashlib
from asl.utils.string_helper import generate_random_string

TOKEN_RANDOM = 'random_token'
TOKEN_HASHED = 'hashed_token'

TOKEN_SERVICE_SECURITY_CONFIG = 'SERVICE_SECURITY_TOKEN'


def generate_security_data():
    random_token = generate_random_string()
    return {TOKEN_RANDOM: random_token, TOKEN_HASHED: compute_token(random_token)}


def wrap_plain_data_as_secure(data):
    return {'security': generate_security_data(), 'data': data}


@inject(service_application=AtteqServiceFlask)
def compute_token(random_token, service_application):
    secure_token = service_application.config[TOKEN_SERVICE_SECURITY_CONFIG]
    sha1hash = hashlib.sha1()
    sha1hash.update(random_token + secure_token)
    return sha1hash.hexdigest().upper()


def verify_security_data(security):
    random_token = security[TOKEN_RANDOM]
    hashed_token = security[TOKEN_HASHED]
    return unicode(hashed_token) == unicode(compute_token(random_token))
