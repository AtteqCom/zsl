# coding: utf-8

import wtforms.validators
from time import strptime
#from symbol import except_clause

class validators:
    class Optional(wtforms.validators.Optional):
        def __init__(self, strip_whitespace=True):
            wtforms.validators.Optional.__init__(self, strip_whitespace)

    class Required(wtforms.validators.Required):
        def __init__(self, message=u'Toto pole je povinné.'):
            wtforms.validators.Required.__init__(self, message)

    class URL(wtforms.validators.URL):
        def __init__(self, require_tld=True, message=u'Neplatná URL adresa. URL adresa musí začínať s "http://". Napríklad "http://www.zoznam.sk"'):
            wtforms.validators.URL.__init__(self, require_tld, message)

    class Date(object):
        '''
        validator - skontroluje, ci dany string je datum v zadanom formate a ci je dany datum platny
        '''
        def __init__(self, format, message=u'Nesprávny formát dátumu alebo neplatný dátum.', stop_after_fail = False):
            self.format = format
            self.message = message
            self.stop_after_fail = stop_after_fail

        def __call__(self, form, field):
            try:
                strptime(field.data, self.format)
            except ValueError:
                if self.stop_after_fail:
                    raise wtforms.validators.StopValidation(self.message)
                else:
                    raise wtforms.validators.ValidationError(self.message)

    class Length(wtforms.validators.Length):
        def __init__(self, min=-1, max=-1, message=None):
            if message:
                msg = message
            else:
                msg = u''
                if min > -1:
                    msg += u'Minimálny počet znakov textu: %(min)d. '
                if max > -1:
                    msg += u'Maximálny počet znakov textu: %(max)d.'

            wtforms.validators.Length.__init__(self,min,max,msg)

    class Regexp(wtforms.validators.Regexp):
        def __init__(self, regex, flags=0, message=u'Nesprávny formát dát.'):
            wtforms.validators.Regexp.__init__(self, regex, flags, message)