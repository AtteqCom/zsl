"""
:mod:`zsl.utils.security_helper`
-------------------------------------

Helper module with function dealing with security.
"""

from __future__ import unicode_literals

from builtins import str
import hashlib

from zsl import Config, inject
from zsl.utils.string_helper import generate_random_string

TOKEN_RANDOM = 'random_token'
TOKEN_HASHED = 'hashed_token'

TOKEN_SERVICE_SECURITY_CONFIG = 'SERVICE_SECURITY_TOKEN'


def generate_security_data():
    """Generate security token - a random token and its hashed version salted
    with a secret.

    :return: random and hashed token
    :rtype: dict(str, str)
    """
    random_token = generate_random_string()
    return {TOKEN_RANDOM: random_token, TOKEN_HASHED: compute_token(random_token)}


def wrap_plain_data_as_secure(data):
    """Wrap task data with security token.

    :param data: data to be wrapped
    :return: wrapped data with security token
    :rtype: dict
    """
    return {'security': generate_security_data(), 'data': data}


@inject(config=Config)
def compute_token(random_token, config):
    """Compute a hash of the given token with a preconfigured secret.

    :param random_token: random token
    :type random_token: str
    :return: hashed token
    :rtype: str
    """
    secure_token = config[TOKEN_SERVICE_SECURITY_CONFIG]
    sha1hash = hashlib.sha1()
    sha1hash.update(random_token + secure_token)
    return sha1hash.hexdigest().upper()


def verify_security_data(security):
    """Verify an untrusted security token.

    :param security: security token
    :type security: dict
    :return: True if valid
    :rtype: bool
    """
    random_token = security[TOKEN_RANDOM]
    hashed_token = security[TOKEN_HASHED]
    return str(hashed_token) == str(compute_token(random_token))
