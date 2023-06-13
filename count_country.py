from tqdm import tqdm
import gzip
import glob
import re
dstcnt = {}
fglog = glob.glob(b'fw/*.log.tar.gz')
sdate = 0
i = 0
dstcountry = None

# Read globbed log files one by one
for file in fglog:

  # Get total number of lines
  with gzip.open(file, 'rb') as f:
    tnol = sum(1 for line in f) - 1
    bar = tqdm(total = int(tnol))
  
  # Read one compressed file
  with gzip.open(file, 'rb') as f:
    strfile = str(file)
    strfile1 = strfile.split("'")
    strfile2 = strfile1[1].split('/')
    print('{}'.format(strfile2[1]))

    # Read one line
    for line in f:
  
      # Print state of progress
      rnol = tnol - i
      i += 1
      bar.update(1)

      if b'type="traffic"' in line:
        dcline = line.split(b'dstcountry')
        mlist = dcline[1].split(b'"')
        ctry = mlist[1].decode('utf-8')
        if ctry in dstcnt.keys():
          dstcnt[ctry] += 1
        else:
          dstcnt[ctry] = 1

# for development, sample data
dstcnt = {'Japan': 378806, 'United States': 236004, 'India': 13700, 'United Kingdom': 3258, 'Taiwan': 5754, 'Canada': 1026, 'Switzerland': 940, 'Germany': 4006, 'Australia': 3585, 'Singapore': 5515, 'France': 861, 'Netherlands': 986, 'Hong Kong': 3159, 'Russian Federation': 184, 'Spain': 1743, 'Ireland': 503, 'Finland': 143, 'Colombia': 4, 'Norway': 4, 'Italy': 6, 'Korea, Republic of': 1113, 'Austria': 18, 'Sweden': 21, 'Mexico': 3, 'Malaysia': 4, 'Luxembourg': 2, 'Denmark': 73, 'Belgium': 137, 'Brazil': 55, 'China': 67, 'Bulgaria': 3, 'Hungary': 12, 'United Arab Emirates': 5, 'Turkey': 3, 'Czech Republic': 11, 'Chile': 1, 'Argentina': 6, 'Ukraine': 2, 'Panama': 2, 'Reserved': 7, 'Indonesia': 4, 'New Zealand': 2, 'Poland': 4, 'South Africa': 4}

# pie chart

labels = []
sizes = []
colors = []
noe = 1 # number of elements
for key, value in dstcnt.items():
  labels.append(key)
  sizes.append(value)
  noe += 1

import random
def random_color():
  return '#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])

n = noe # number of elements
for j in range(n):
  colors.append(random_color())

import matplotlib.pyplot as plt
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.savefig("access-country-pie.png")

# bar graph

import os
import csv
import pandas as pd
import plotly.express as px
with open('output.csv', mode='w') as file:
  writer = csv.writer(file)
  writer.writerow(['country', 'count'])
  for key in dstcnt.keys():
    writer.writerow([key,dstcnt[key]])
df = pd.read_csv('output.csv')
os.remove('output.csv')

fig = px.bar(df, x = 'country', y = 'count' , title = 'fw-traffic')
fig.update_layout(width=1900,height=1000,margin=dict(l=50,r=50,b=40,t=60),yaxis=dict(range=[12000,400000]),xaxis=dict(dtick=1, autorange=True),title=dict(font = dict(size=20)))
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.write_image("access-country-bar-0.png")

fig1 = px.bar(df, x = 'country', y = 'count' , title = 'fw-traffic')
fig1.update_layout(width=1900,height=1000,margin=dict(l=50,r=50,b=40,t=60),yaxis=dict(range=[3000,6000]),xaxis=dict(dtick=1, autorange=True),title=dict(font = dict(size=20)))
fig1.update_layout(xaxis={'categoryorder':'total descending'})
fig1.write_image("access-country-bar-1-.png")

fig2 = px.bar(df, x = 'country', y = 'count' , title = 'fw-traffic')
fig2.update_layout(width=1900,height=1000,margin=dict(l=50,r=50,b=40,t=60),yaxis=dict(range=[200,1800]),xaxis=dict(dtick=1, autorange=True),title=dict(font = dict(size=20)))
fig2.update_layout(xaxis={'categoryorder':'total descending'})
fig2.write_image("access-country-bar-2.png")

fig3 = px.bar(df, x = 'country', y = 'count' , title = 'fw-traffic')
fig3.update_layout(width=1900,height=1000,margin=dict(l=50,r=50,b=40,t=60),yaxis=dict(range=[0,200]),xaxis=dict(dtick=1, autorange=True),title=dict(font = dict(size=20)))
fig3.update_layout(xaxis={'categoryorder':'total descending'})
fig3.write_image("access-country-bar-3.png")
