from tqdm import tqdm
import gzip
import glob
import re
from datetime import datetime
from decimal import Decimal
fortigatelogarchive = glob.glob(b'fw/*.log.tar.gz')
socialist_count = 0
democratic_count = 0
sdate = 0
i = 0

# Read the globbed log files one by one.
for file in fortigatelogarchive:

  # Make a name of output file.
  outfilename_array = file.split(b'_')
  outfilename = outfilename_array[0] + b'_stat.log'
  
  # Open the outfile
  outfile = open(outfilename,'w')
  
  # Write a header
  outfile.write('\n# Firewall traffic log that contains socialist state, communist nation, Authoritarian political states, and so on.\n')
  outfile.write('\n# Date, Time(nanosecond), src-ip, dst-ip, dst-port, dst-country\n')

  # Get the total number of lines.
  with gzip.open(file, 'rb') as f:
    tnol = sum(1 for line in f) - 1
    bar = tqdm(total = int(tnol))

  # Read one compressed file
  with gzip.open(file, 'rb') as f:

    # Read one line.
    for line in f:

      # Print the state of progress
      rnol = tnol - i
      i += 1
      bar.update(1)

      # If the string "type=traffic" is included, process it.
      if b'type="traffic"' in line:
        dcline = line.split(b'dstcountry')
        slist = dcline[0].split()
        mlist = dcline[1].split(b'"')

        if ( # Socialist, Communism, Feudalism.
          b'Russia' in mlist[1] 
          or b'democratic' in mlist[1] 
          or b'China' in mlist[1] 
          or b'Cuba' in mlist[1]
        ):
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
            
        else: # Democratic state
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
          continue

        # Collected items are compiled and output to the console.
        outfile.write("{},{},{},{},{},{}\n".format(sdate, stime, srcip, dstip, dstport, dstcountry))

# Statistics
outfile.write('\n# Statistics\n')
outfile.write("Democratic state access counts : {:,}\n".format(democratic_count))
outfile.write("Democratic access percentage : {:.3f}%\n".format((democratic_count / (democratic_count + socialist_count)) * 100))
outfile.write("Socialist state access counts : {:,}\n".format(socialist_count))
outfile.write("Socialist access percentage : {:.3f}%\n\n".format((socialist_count / (democratic_count + socialist_count)) * 100))
outfile.close()