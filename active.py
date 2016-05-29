from base import BasePEOC

test = BasePEOC()
data = test.get()

for elm in data:
    print(elm['unit']+"\t"+elm['description']+"\t"+elm['dispatch_time'])
