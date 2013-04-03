'''
Created on 12.12.2012

@author: Martin Babka
'''
import abc

class IdHelper:
    @abc.abstractmethod
    def gather_page(self, key, page_no):
        pass

    @abc.abstractmethod
    def fill_page(self, key, page_no, data):
        pass

    @abc.abstractmethod
    def check_key(self, key):
        pass

    @abc.abstractmethod
    def check_page(self, key, page_no):
        pass

    @abc.abstractmethod
    def save(self, key, value):
        pass

    @abc.abstractmethod
    def create_key(self, value):
        pass
