'''
Created on 12.12.2012

@author: Martin Babka
'''
import abc

def encoder_identity(x):
    return x

def decoder_identity(module_name, x):
    return x

class IdHelper:
    @abc.abstractmethod
    def gather_page(self, page_key, decoder = decoder_identity):
        pass

    @abc.abstractmethod
    def fill_page(self, page_key, data, timeout, encoder = encoder_identity):
        pass

    @abc.abstractmethod
    def check_page(self, page_key):
        pass

    @abc.abstractmethod
    def check_key(self, key):
        pass

    @abc.abstractmethod
    def get_key(self, key):
        pass

    @abc.abstractmethod
    def invalidate_key(self, key):
        pass

    @abc.abstractmethod
    def set_key(self, key, value, timeout):
        pass

    @abc.abstractmethod
    def create_key(self, value):
        pass
