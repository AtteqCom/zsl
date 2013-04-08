'''
Created on 12.12.2012

@author: Martin Babka
'''
import abc

class IdHelper:
    @abc.abstractmethod
    def gather_page(self, page_key):
        pass

    @abc.abstractmethod
    def fill_page(self, page_key, data):
        pass

    @abc.abstractmethod
    def check_key(self, key):
        pass

    @abc.abstractmethod
    def check_page(self, page_key):
        pass

    @abc.abstractmethod
    def save(self, key, value):
        pass

    @abc.abstractmethod
    def create_key(self, value):
        pass

    @abc.abstractmethod
    def create_key(self, value):
        pass

    @abc.abstractmethod
    def create_page_key(self, value, page_no):
        pass
