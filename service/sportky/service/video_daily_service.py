'''
Created on 28.2.2013

@author: Jan Janco
'''

from sportky.service.service import Service, transactional
from db.models.raw import VideoDaily
from db.helpers.query_helper import QueryHelper

#import random
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql import func

class VideoDailyService(Service):
    '''
    Service handling the daily video
    '''
    
    def __init__(self):
        Service.__init__(self)

    @transactional
    def save(self, video_daily):
        if (video_daily.vdid == None):
            self._orm.add(video_daily)
            self._orm.commit()

    @transactional
    def fetch(self, vdid):
        return self._orm.query(VideoDaily).filter(VideoDaily.vdid == vdid).one()

    @transactional
    def fetch_list(self, filter, pagination, sorter):
        qh = QueryHelper(VideoDaily, filter, pagination, sorter)
        return (qh.execute(self._orm.query(VideoDaily)),qh)
    
    @transactional
    def fetch_latest(self, count):
        '''
        Fetch last active videos  
        '''
        return self._orm.query(VideoDaily).filter(VideoDaily.date < func.now()).order_by(desc(VideoDaily.date)).limit(count).all()

    @transactional
    def fetch_for_date(self, date):
        '''
        Fetch daily video for given date
        '''
        return self._orm.query(VideoDaily).filter(VideoDaily.date == date).one()
