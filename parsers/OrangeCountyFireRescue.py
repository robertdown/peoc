import re
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import base

class OCFRActive(base.BasePEOC):

    data = []

    def __init__(self):
        super().__init__()
        pass

    def parse(self):
        try:
            r = requests.get('http://www.orangecountyfl.net/EmergencySafety/FireRescueActiveCalls.aspx')
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find(id='dnn_ctr6845_WebCAD_lstvwCalls4Svc_itemPlaceholderContainer')
            rows = table.findAll('tr')
            correlation = ['callno', 'dispatch_time', 'description', 'type', 'units', 'street_no', 'street_name']

            for row in rows:
                cells = row.findAll('td')
                i = 0
                tmp = {}
                tmp_date = ''
                address_str = ''
                for cell in cells:
                    if i >= 0 and i < 5:
                        tmp[correlation[i]] = cell.text.strip()
                    if i == 1:
                        n = datetime.today()
                        t = datetime.strptime(cell.text.strip(), '%H:%M:%S')
                        now_time = n.strftime('%H:%M:%S')
                        d_time = t.strftime('%H:%M:%S')
                        if d_time > now_time:
                            delta = timedelta(1)
                            n = (n-delta)
                        parsed = datetime(n.year, n.month, n.day, t.hour, t.minute, t.second)
                        tmp[correlation[i]] = parsed
                    if i == 4:
                        units = cell.text.strip().split(" ")
                        tmp[correlation[i]] = units
                    if i == 5:
                        address_str = cell.text.strip()
                    if i == 6:
                        address_str = address_str + " " + cell.text.strip()
                        tmp["address"] = address_str
                    if i == 7:
                        continue

                    i = i + 1
                if len(tmp) > 0:
                  self.data.append(tmp)

            return self.data
        except Exception as e:
            print(e)
            pass
