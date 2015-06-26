# gets Aus public holidays from data.gov.au

import json
import urllib
import tempfile, os
import pytz
from datetime import date, datetime, timedelta
from icalendar import Calendar, Event, vCalAddress, vText

dtfmt = '%Y-%m-%d %H:%M:%S %Z (UTC%z)'
utc = pytz.utc
syd = pytz.timezone('Australia/Sydney')
dt = utc.localize(datetime.utcnow())
url = 'http://data.gov.au/api/action/datastore_search?resource_id=31eec35e-1de6-4f04-9703-9be1d43d405b'

try:
    phjs = json.load(urllib.urlopen(url))
except:
    print "Failed loading/parsing JSON from ", url
    quit()

cal = Calendar()
cal.add('prodid','-//NSW_PH@github.com//studiology//')
cal.add('version','2.0')
cal.add('comment','extracted from '+url+' at '+dt.astimezone(syd).strftime('%Y-%m-%d %H:%M:%S %Z (UTC%z)'))
def make_event(summary,dtstart,dtend,dtstamp,uid,description):
    event = Event()
    event.add('summary',summary)
    event.add('dtstart',dtstart)
    event.add('dtend',dtend)
    event.add('dtstamp',dtstamp)
    event.add('uid',uid)
    event.add('X-MICROSOFT-CDO-BUSYSTATUS','OOF')
    event.add('description',description)
    cal.add_component(event)

uid_base = phjs['result']['resource_id']
td = timedelta(days=1)

for hol in phjs['result']['records']:
    if ('NAT' in hol['Applicable To'] or 'NSW' in hol['Applicable To']):
        dt = datetime.strptime(hol["Date"],"%Y%m%d")
        d = dt.date()
        uid = "studiology_" + uid_base + "_" + str(hol['_id'])
        desc = hol['Information'] + '\n\n' + hol['More Information']
        make_event(hol['Holiday Name'],d,d+td,dt,uid,desc)

#write to disk
directory = tempfile.mkdtemp()
f = open(os.path.join(directory, 'nsw_public_holidays.ics'),'wb')
f.write(cal.to_ical())
f.close()
#print(cal.to_ical())
#yay?
