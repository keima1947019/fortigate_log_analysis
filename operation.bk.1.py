import gzip
import glob
import re
from datetime import datetime
from decimal import Decimal
logfile = glob.glob(b'fw/*.log.tar.gz')

# Print the header
print('# Firewall traffic log that contains socialist state, communist nation, Authoritarian political states, and so on.')
print('# Date, Time(nanosecond), src-ip, dst-ip, dst-port, dst-country')

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

          for item in slist:

            # Get event date and time from log.
            if b'eventtime' in item:
              jlist = item.split(b'=')
              epochtime = int(jlist[1].decode('utf-8'))
              dt = datetime.fromtimestamp(epochtime // 1000000000)
              sdate = dt.strftime('%Y/%m/%d')
              stime = dt.strftime('%H:%M:%S')
              stime += '.' + str(int(epochtime % 1000000000)).zfill(9)

            # Get the dst ip.
            if b'dstip' in item:
              jlist = item.split(b'=')
              dstip = jlist[1].decode('utf-8')

            # Get the dst ip.
            if b'srcip' in item:
              jlist = item.split(b'=')
              srcip = jlist[1].decode('utf-8')
            
            # Get the dst port
            if b'dstport' in item:
              jlist = item.split(b'=')
              dstport = jlist[1].decode('utf-8')
        
        else:
          continue

        # Collected items are compiled and output to the console.
        print("{},{},{},{},{},{}".format(sdate, stime, srcip, dstip, dstport, dstcountry))

