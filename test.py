import numpy as np
import matplotlib.pyplot as plt
from indices import *
from soundsim import *

###############################################################################
#
## Normal ACI test
#
#mic = Microphone(0, 0)
#e = WaveEmitter(1, 1)
#o = NoiseEmitter(2, 2 , 1)
#e.setSpec(e.pureToneSpectrum([5, 10, 20]))

#eData = np.zeros(1024)
#oData = np.zeros(1024)
#for n in range(0, 1024):
   #eData[n] = e.A(mic, n)
   #oData[n] = o.A(mic, n)
   
#eSpec = getSpectrogram(eData, .25, 64)
#oSpec = getSpectrogram(oData, .25, 64)

#print "ACI of normal sinusoid: " + str(calculateACI(eSpec))
#print "ACI of white noise: " + str(calculateACI(oSpec))

###############################################################################
#
## Test for my histogram method w/ ACI
#
#signal, hz = loadFile( "guitar.wav" )

#x = [c[0] for c in signal]
#samples = len(x)
#b = hz / 2 #half second blocks
#blocks = samples / b

#data = []

#for n in range(0, blocks):
    #sub = x[n * b: (n + 1) * b]
    #spec = stft(sub, hz)
    #ACI = calculateACI(spec)
    #data.append(ACI)
    #print str(n * 1.0 / blocks) 
    
#plt.hist(data, bins = 250)
#plt.show()

###############################################################################

signal, hz = loadFile( "317.wav" )
x = [c[0] for c in signal]
aei = calculateAEI(x, hz)
print "AEI: " + str(aei)