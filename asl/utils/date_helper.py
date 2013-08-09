'''
Created on 10.7.2013

@author: Martin Babka
'''

def format_datetime_portable(ts):
    return '{0.year:{1}}-{0.month:{1}}-{0.day:{1}}T{0.hour:{1}}:{0.minute:{1}}:{0.second:{1}}'.format(ts, '02')

def format_date_portable(ts):
    return '{0.year:{1}}-{0.month:{1}}-{0.day:{1}}'.format(ts, '02')
