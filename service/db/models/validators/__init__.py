# coding: utf-8

from wtforms import Form, TextField, validators, DateField
from sportky.service.video_daily_service import VideoDailyService
from datetime import date,datetime
from injector import inject

class SportClubForm(Form):
    homepage = TextField('homepage', [validators.Optional(), validators.URL()])

class VideoDailyForm(Form):
    
#    @inject(video_daily_service=VideoDailyService)
#    def __init__(self, video_daily_service, formdata=None, obj=None, prefix='', **kwargs):
#        Form.__init__(self,formdata,obj,prefix,**kwargs)
#        self._video_daily_service = video_daily_service
#        print 'parametre {0} | {1} | {2} | {3} | {4}'.format(self,video_daily_service,formdata,obj,prefix)
        
    name = TextField('name', [validators.Required()])
    date = DateField('date', [validators.Required()], format='%d. %m. %Y')
    description = TextField('description', [validators.Required()])
    embedded_code = TextField('embedded_code', [validators.Required()])

#    def validate_date(self,field):
#        video_daily_db = self._video_daily_service.fetch_for_date(field.data)
#        
#        if not video_daily_db == None:
#            raise ValidationError(u'Pre zadaný dátum už existuje video dňa.')
