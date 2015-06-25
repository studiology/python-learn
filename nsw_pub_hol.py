# gets Aus public holidays from data.gov.au

import json
import urllib
from datetime import date
from datetime import datetime

url = 'http://data.gov.au/api/action/datastore_search?resource_id=31eec35e-1de6-4f04-9703-9be1d43d405b'

try:
    phjs = json.load(urllib.urlopen(url))
except:
    print "Failed loading JSON from ", url
    quit()

for hol in phjs['result']['records']:
    if ('NAT' in hol['Applicable To'] or 'NSW' in hol['Applicable To']):
        d = datetime.strptime(hol["Date"],"%Y%m%d")
        if d > datetime.now():
            print d.strftime('%a %Y-%m-%d'), hol['Holiday Name']
        else:
            print d.strftime('%a %Y-%m-%d'), hol['Holiday Name'], '*** MISSED IT ***'

