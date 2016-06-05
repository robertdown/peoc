from base import BasePEOC
from datetime import datetime
import os
import time
import iso8601

test = BasePEOC()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getWhitespace(item, length):
    if len(item) > length:
        item = item[:length]
    else:
        item = item + (" " * (length - len(item)))[:length]
    return item

while True:
    data = test.get()
    cls()
    print(bcolors.ENDC+"UPDATED: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    header = "| "+getWhitespace("DISPATCH TIME", 17) +"| "+ getWhitespace("UNITS RESPONDING", 40) +"| "+getWhitespace("DESCRIPTION", 35) +"| "+"ADDRESS"
    print(header)
    rows, columns = os.popen('stty size', 'r').read().split()
    print("-" * int(columns))
    for elm in data:
        dispatch_day = elm['dispatch_time'].strftime('%d')
        current_day = datetime.now().strftime('%d')
        day = "today" if dispatch_day == current_day else "yesterday"
        dispatch_time = elm['dispatch_time'].strftime("%R "+day)
        if elm['type'] == 'FIRE':
            color = bcolors.FAIL
        else:
            color = bcolors.OKBLUE
        try:
            units = elm['units']
        except KeyError as e:
            units = []

        unitStr = ""
        for unit in units:
            unitStr = unit + " " + unitStr

        printStr = "| "+getWhitespace(dispatch_time, 17) +"| "+ getWhitespace(unitStr, 40) +"| "+getWhitespace(elm['description'], 35) +"| "+elm['address']
        print(color + printStr)
        # print("-" * len(printStr))

    time.sleep(60)



