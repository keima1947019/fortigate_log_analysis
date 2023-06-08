import gzip
import glob
import re
from datetime import datetime
from decimal import Decimal
logfile = glob.glob(b'fw/*.log.tar.gz')

# Read the globbed log files one by one.
for file in logfile:

  # Read one compressed file
  with gzip.open(file, 'rb') as f:

    # Read one line.
    for line in f:

      # If the string "type=traffic" is included, process it.
      if b'type="traffic"' in line:
        dcline = line.split(b'dstcountry')
        slist = dcline[0].split()
        mlist = dcline[1].split(b'"')

        # Split by the country name that is socialist, communism, feudalism, state.
        if b'Russia' in mlist[1] or b'democratic' in mlist[1] or b'China' in mlist[1] or b'Cuba' in mlist[1]:
          dstcountry = mlist[1].decode('utf-8')
        else:
          continue

        for item in slist:

          # Get event date and time from log.
          if b'eventtime' in item:
            jlist = item.split(b'=')
            epochtime = int(jlist[1].decode('utf-8'))
            dt = datetime.fromtimestamp(epochtime // 1000000000)
            stime = dt.strftime('%Y-%m-%d %H:%M:%S')
            stime += '.' + str(int(epochtime % 1000000000)).zfill(9)
            #print(stime,end='\t')

          # Get the dst ip.
          if b'dstip' in item:
            jlist = item.split(b'=')
            dstip = jlist[1].decode('utf-8')
            #print(type(dstip))

          # Get the dst ip.
          if b'srcip' in item:
            jlist = item.split(b'=')
            srcip = jlist[1].decode('utf-8')

        # Collected items are compiled and output to the console.
        print("{},{},{},{}".format(stime, srcip, dstip, dstcountry))

