from parsers.OrangeCountyFireRescue import OCFRActive
from parsers.OrlandoFireDepartment import OFDActive
from datetime import datetime
import time

ocfr = OCFRActive()
ofd = OFDActive()

while True:
    print("Parsing %s" % datetime.now())
    ocfr_data = ocfr.parse()
    ocfr.put(ocfr_data)

    ofd_data = ofd.parse()
    ofd.put(ofd_data)
    time.sleep(60)
