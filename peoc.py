import re
import requests
from bs4 import BeautifulSoup
import base

class OCFRActive(base.BasePEOC):

    data = []

    def __init__(self):
        super().__init__()
        pass

    def parse(self):
        r = requests.get('http://www.orangecountyfl.net/EmergencySafety/FireRescueActiveCalls.aspx#.Vpmb6vFk6F7')
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find(id='dnn_ctr6845_WebCAD_lstvwCalls4Svc_itemPlaceholderContainer')
        rows = table.findAll('tr')
        correlation = ['callno', 'dispatch_time', 'description', 'type', 'unit', 'street_no', 'street_name']

        for row in rows:
            cells = row.findAll('td')
            i = 0
            tmp = {}
            tmp_date = ''
            address_str = ''
            for cell in cells:
              if i > 1 and i < 5:
                  tmp[correlation[i]] = cell.text.strip()
              if i == 1:

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
