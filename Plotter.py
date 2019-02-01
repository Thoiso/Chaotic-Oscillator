#PLOT MAKER

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv

#%%
fil = r'C:\Users\drost\OneDrive\Bureaublad\Data-P project\verwerkte txt\poicare2.txt'

with open(fil,'r') as file:
    read=csv.reader(file, delimiter='\t')
    data=list(read)
file.closed

beginpunten = []
for i in range(len(data)):
    if data[i][0].strip() == '**BEGIN**':
        beginpunten.append(i)
    if data[i][0].strip() == '**END**':
        einde = i

dataSplits = {}
for i in range(len(beginpunten)):
    n1 = beginpunten[i] + 2
    if (i+1) < len(beginpunten):
        n2 = beginpunten[i+1] - 1
    else:
        n2 = einde -1
    
    nr = data[beginpunten[i]+1][3]
    data1 = [float(dat[0]) for dat in data[n1:n2]]
    data2 = [float(dats[1]) for dats in data[n1:n2]]
    dataSplits[nr] = [data1,data2]

#%%
for i in list(dataSplits.keys()):
    j = 2*np.pi*int(i)/999
    fase0 = [j]*100
    fase1 = np.linspace(0,1.01,100)
    data1 = dataSplits[i][0]
    data2 = dataSplits[i][1]
    
    fig = plt.figure(1)
    gridspec.GridSpec(15,15)
    
    plt.subplot2grid((15,15), (0,0), colspan=14, rowspan=15)
    plt.locator_params(axis='x', nbins=5)
    plt.title('Poincaré section')
    plt.xlabel('$\Theta$ (rad)')
    plt.ylabel('d$\Theta$/d$t$ (rad/s)')
    plt.xlim(-15, 15)
    plt.ylim(-18, 18)
    plt.scatter(data1,data2,s=0.1)
    
    i = i.strip()
    print(i)
    j = '0'*(3-len(i))
    j = j + i
    plt.subplot2grid((15,15), (0,14), colspan=1, rowspan=15)
    plt.tick_params(axis='y', which='both', labelleft=False, labelright=True)
    plt.title('φ')
    plt.xticks([])
    plt.ylim(0,2*np.pi)
    plt.grid()
    plt.plot(fase1,fase0,linewidth=5.0)
    plt.savefig(r'C:\Users\drost\OneDrive\Bureaublad\Data-P project\Gif poging 34\poicare' + j + '.png', dpi = 200 )
    plt.show()

