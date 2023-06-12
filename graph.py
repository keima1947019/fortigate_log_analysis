'''
# 円グラフ

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # フォントに関するモジュール
import numpy as np
fp = FontProperties(fname='851MkPOP_101.ttf') # フォント

#labels = ['キノコ', 'どちらかといえばキノコ', 'どちらかといえばタケノコ', 'タケノコ']
#sizes = [15, 30, 45, 10]
#explode = [0, 0.5, 0, 0]
labels = ['民衆主義国家', '社会主義国家']
sizes = [7161358, 5080]
explode = [0, 0]

fig, ax = plt.subplots()
patches, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90, labeldistance=0.7, pctdistance=0.5, wedgeprops={'linewidth': 1, 'edgecolor':"0.8"})
ax.axis('equal') # 面積比=割合
plt.setp(autotexts, size=12)
plt.setp(texts, fontproperties=fp)
plt.savefig("traffic.png")

# ヒストグラム

import numpy as np
import matplotlib.pyplot as plt

list = []
for _ in range(10000):
    list.append(np.random.randint(1, 7, size=10).sum())

plt.hist(list, 20, color="b", rwidth=0.8)
plt.savefig("traffic.png")

'''

# 棒グラフ

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # Modules related to fonts
from matplotlib.ticker import ScalarFormatter # Module on axis formats
fp = FontProperties(fname='851MkPOP_101.ttf') # fonr file definition

left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
height = [1888034127, 2073363421, 2299541939, 2555948654, 3041593413, 3711800786, 4452766336, 5282371928, 6084907596, 6866880431, 7659291953]
labels = ['1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(left, height, width=0.2, color='0.5',
edgecolor='k', linewidth=2, tick_label=labels, hatch='/')
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True)) # Vertical axis in exponential format
plt.title("Total World Population",fontproperties=fp) # font definition by fontproperties
plt.xlabel("year",fontproperties=fp)
plt.ylabel("total population",fontproperties=fp)
plt.savefig("traffic.png")

