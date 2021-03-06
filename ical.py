"""A simple wrapper class for the icalendar package"""

from icalendar import Calendar, Event
from datetime import datetime
from shotglass2.shotglass import get_site_config
from shotglass2.takeabeltof.date_utils import getDatetimeFromString

class ICal(Calendar):
    def __init__(self,**kwargs):
        site_config = get_site_config()
        super().__init__(self)
        self.add('version','2.0')
        self.add('calscale','GREGORIAN')
        self.add('prodid',kwargs.get('prodid',site_config['HOST_NAME'].lower()))
        calendar_name = kwargs.get('calendar_name',None)
        if not calendar_name:
            self.add('x-priamry-calendar','TRUE')
        else:
            # give the calendar a name
            self.add('x-wr-calname',calendar_name)
            self.add('name',calendar_name)
            
                    
    def add_event(self,uid,start,end,summary,**kwargs):
        """Ad an event to the calendar"""
        if isinstance(start,str):
            start = getDatetimeFromString(start)
        if isinstance(end,str):
            end = getDatetimeFromString(end)
        ev = Event()
        ev.add('uid',uid)
        ev.add('dtstart',start)
        ev.add('dtend',end)
        ev.add('summary',summary)
        
        datestamp = kwargs.pop('dtstamp',datetime.utcnow())
        ev.add('DTSTAMP',datestamp)
        
        for key, value in kwargs.items():
         if value:
             ev.add(key,value)
             
        self.add_component(ev)
         
         
    def get(self):
        # return the calendar as ical text
        if not self.is_empty():
            return self.to_ical()
        else:
            return ''
