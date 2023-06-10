import math
import gzip
import glob
import re
from datetime import datetime
from decimal import Decimal
logfile = glob.glob(b'fw/*.log.tar.gz')
socialist_count = 0
democratic_count = 0
sdate = 0
i = 0

# Print the header
#print('# Firewall traffic log that contains socialist state, communist nation, Authoritarian political states, and so on.')
#print('# Date, Time(nanosecond), src-ip, dst-ip, dst-port, dst-country')

# Read the globbed log files one by one.
for file in logfile:

  with gzip.open(file, 'rb') as f:
    # Get the total number of lines.
    tnol = sum(1 for line in f) - 1

  # Read one compressed file
  with gzip.open(file, 'rb') as f:

    # Read one line.
    for line in f:
      
      # Print the state of progress
      rnol = tnol - i
      i += 1

      # If the string "type=traffic" is included, process it.
      if b'type="traffic"' in line:
        dcline = line.split(b'dstcountry')
        slist = dcline[0].split()
        mlist = dcline[1].split(b'"')

        # Split by the country name that is socialist, communism, feudalism, state.
        if b'Russia' in mlist[1] or b'democratic' in mlist[1] or b'China' in mlist[1] or b'Cuba' in mlist[1]:
          socialist_count += 1
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
            
            # Progress indication
            print("There are {} % more cases left.".format(math.floor( rnol / tnol * 100 )))
        
        else:
          
          for item in slist:
            if b'eventtime' in item:
              jlist = item.split(b'=')
              epochtime = int(jlist[1].decode('utf-8'))
              dt = datetime.fromtimestamp(epochtime // 1000000000)
              sdate = dt.strftime('%Y/%m/%d')
              stime = dt.strftime('%H:%M:%S')
              stime += '.' + str(int(epochtime % 1000000000)).zfill(9)
              democratic_count += 1
              #print("Democratic : {} {} {}".format(democratic_count,sdate,stime))
              
              # Progress indication
              print("There are {} % more cases left.".format(math.floor( rnol / tnol * 100 )))
              
            continue
          continue

        # Collected items are compiled and output to the console.
        #print("{},{},{},{},{},{}".format(sdate, stime, srcip, dstip, dstport, dstcountry))
        #print("socialist : {}".format(socialist_count))

# Print statistics
print('# Total access count of communicate to democratic state')
print(democratic_count)
print('# The democratic percentage of all communications')
percentage = (democratic_count / (democratic_count + socialist_count)) * 100
print(percentage, ' %')
print('# Total access count of communicate to socialist state')
print(socialist_count)
print('# The socialist percentage of all communications')
percentage = (socialist_count / (democratic_count + socialist_count)) * 100
print(percentage, ' %')