import sys
#print(sys.path)
sys.path.append('') ##get import to look in the working dir.
from app import app
from datetime import datetime, timedelta
from ical.ical import ICal

def sample_result():
    return 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:test product\r\nCALSCALE:GREGORIAN\r\nNAME:sample_cal\r\nX-WR-CALNAME:sample_cal\r\nBEGIN:VEVENT\r\nSUMMARY:My Event\r\nDTSTART;VALUE=DATE-TIME:20200323T190359\r\nDTEND;VALUE=DATE-TIME:20200323T200359\r\nDTSTAMP;VALUE=DATE-TIME:20200322T190359Z\r\nUID:my_UID\r\nDESCRIPTION:Something to say...\r\nURL:http://github.com\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n'

def test_make_ical():
    with app.app_context():
        ical = ICal(calendar_name='sample_cal',prodid="test product")
        assert ical.is_empty() == False
        ical.add_event(
            "my_UID",
            datetime(2020,3,23,19,3,59),
            datetime(2020,3,23,20,3,59),
            'My Event',
            dtstamp = datetime(2020,3,22,19,3,59),
            description = "Something to say...",
            url = 'http://github.com',
            )
        # convert the bytes to str 
        assert ical.get().decode("utf-8") == sample_result()
        