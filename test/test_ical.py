import sys
#print(sys.path)
sys.path.append('') ##get import to look in the working dir.
from app import app

from ical.ical import ICal

def test_make_ical():
    with app.app_context():
        ical = ICal()
        assert ical.prodid == 'something'