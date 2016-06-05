import re
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import base

class OFDActive(base.BasePEOC):

    data = []

    def __init__(self):
        super().__init__()
        pass

    def parse(self):
        try:
            r = requests.get('http://webapp.pulsepoint.org/recent_incidents.php?agencyid=07212&tz=240')
            soup = BeautifulSoup(r.text, 'lxml-xml')
            rows = soup.findAll('row')
            correlation = ['dispatch_time', 'type', 'address', 'units', 'geo_lat_lon', 'description']

            for row in rows:
                cells = row.findAll('cell')
                i = 0
                tmp = {}
                tmp_date = ''
                address_str = ''
                for cell in cells:
                    if i == 0:
                        tmp_time = cell.text.strip()[:19]
                        t = datetime.strptime(tmp_time, '%m/%d/%Y %H:%M:%S')
                        tmp[correlation[i]] = t
                    if i >= 1:
                        tmp[correlation[i]] = cell.text.strip()
                    if i == 3:
                        tmp[correlation[i]] = cell.text.strip().split(', ')
                    if i == 5:
                        tmp['callno'] = self.generateCallNo(tmp['dispatch_time'], tmp['address'], tmp['units'])

                    i = i + 1
                if len(tmp) > 0:
                  self.data.append(tmp)

            return self.data
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    t = OFDActive()
    for elm in t.parse():
        print(elm['callno'])
