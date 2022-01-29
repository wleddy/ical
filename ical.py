"""A simple wrapper class for the icalendar package"""

from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
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
             if key == 'reminder' and isinstance(value,(dict,bool)):
                 """Insert a reminder stanza
                     The value for 'reminder may be a dict or True or False
                     
                     if the key 'reminder' contains an empty dict or True the
                     remnder will be set to the default of 30 minutes
                     before the event start
                     
                     The reminder 'trigger' value may be a number of minutes, or a timedelta
                     
                     If the value of 'reminder' is False, no reminder is set.
                 """

                 if value == False:
                     break
                 if value == True:
                     value = {}   
                 
                 al = Alarm()
                 rem = timedelta(minutes=-30) #30 minute default remindor
                 if 'trigger' in value:
                     if isinstance(value['trigger'],timedelta):
                         rem = value['trigger']
                     elif isinstance(value['trigger'],(int,float)):
                         rem = timedelta(minutes=abs(value['trigger'])*-1)
                         
                 al.add('TRIGGER',rem)
                 al.add('ACTION',value.get('action','DISPLAY').upper())
                 al.add('TITLE',value.get('title','Reminder').title())
                 ev.add_component(al)
             else:
                 # a 'normal' value
                 ev.add(key,value)
                 
        
        self.add_component(ev)
        
         
    def get(self):
        # return the calendar as ical text
        if not self.is_empty():
            return self.to_ical()
        else:
            return ''
