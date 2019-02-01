# -*- coding: utf-8 -*-
"""
Poincare calculator
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import itertools
import matplotlib.cm as cm
#%%
files = open(r'C:\Users\drost\OneDrive\Bureaublad\Data-P project\verwerkte txt\poicare.txt', 'w+')
files2 = open(r'C:\Users\drost\OneDrive\Bureaublad\Data-P project\verwerkte txt\poicare2.txt', 'w+')
# File location
loc=r'D:\Documenten\Drive\! Delen tussen drives\Uni\Natuurkunde\Chaotische oscilator project\txt bestandjes dag 3\Chaos_15g_65mm_085Hz_810V_lang5.txt'
# Read the file in list format
with open(loc,'r') as file: 
    read=csv.reader(file, delimiter='\t')
    data0=list(read)
file.closed

### Parameter information
# Now, we search for the buffer frequency (cycles per second),
data1=list(itertools.chain.from_iterable(data0))
data1[data1.index('f')+1]
f=float(data1[data1.index('f')+1].replace(',','.'))
print('Buffer cycles per second:', f)
# buffer size
Nb=int(data1[data1.index('B')+1])
# the combination gives us the step size
dt=1/(Nb*f)

# read the DAC output a.f.o. time
bufb=data1.index('Channel')+3
bufe=data1.index('Output Data')-4
buft=dt*np.array(list(map(int,data1[bufb:bufe+3:3])))
bufV=np.array(list(map(float,data1[bufb+1:bufe+3+1:3])))

plt.plot(buft,bufV)
plt.xlabel('$t$ (s)')
plt.ylabel('DAC Voltage (V)')


### Angle information
# Check how many channel regions are present
Nr=int(data1[data1.index('Nr')+1])
print('Number of channel regions:', Nr)

# User specified region (<=Nr)
region=1
if region>Nr:
    print('region index exceeds number of regions')

### Search for channel information for selected region
# standard, averaging of angle and angular velocity is performed over the full
# region range. If you want to limit the range, then manually adjust the 
# values for rb and re
# offset can be used to choose a different section of the total number of channels
# Number of channels should be at least 2, because of calculation of dthetadt 
r='r'+str(region)
    
offsets = np.arange(0,999,2)
for offs in offsets:
    offs=offs
    rb=int(data1[data1.index(r)+1])+offs
    print('Region start:', rb)
    re=int(data1[data1.index(r)+2])+offs+5
    print('Region end:', re)
    
    # Number of cycles
    Nc=int(data1[data1.index('N')+1])
    
    ### Data selection
    # First, create data block
    datab=data1.index('Cycle')+6
    datae=data1.index('***END')-6
    data=np.array(list(map(float,data1[datab:datae])))
    
    theta=np.zeros(Nc)
    dthetadt=np.zeros(Nc)
    n=1
    
    offset = (offs/999)*2*np.pi
    
    for i in np.arange(len(data)):
        if data[i]==float(n) and data[i+1]==float(rb):
            lth=np.unwrap(data[i+2:i+6*(re-rb+1):6])
            theta[n-1]=np.mean(lth)
            dthetadt[n-1]=np.mean(np.diff(lth)/dt)
            n=n+1
    
    files.write('**BEGIN**\n')
    files.write('Offset \t %f \t num \t %i \n' %(offset,offs))
    
    if offs % 10 == 0:
        files2.write('**BEGIN** \n')
        files2.write('Offset \t %f \t num \t %i \n' %(offset,offs))
        
    for i in range(len(dthetadt)):
        if theta[i] != 0 and dthetadt[i] != 0:
            files.write('%f \t %f \n' %(theta[i], dthetadt[i]))
            if offs % 10 == 0:
                files2.write('%f \t %f \n' %(theta[i], dthetadt[i]))

    print('klaar met offs: %.f \n' %(offs))
files.write('**END**')
files.close()  
files2.write('**END**')
files2.close()   