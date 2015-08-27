import numpy as np
import random
import matplotlib.pyplot as plt
 
class WaveEmitter:
    """ This class is for simulating a sound emitter """
    
    spec = []
    signal = []
    signalLen = 0
    x = 0
    y = 0
    
    SOUND_SPEED = 100.0
    
    def __init__(self, x = 0, y = 0):
        self.spec = self.randPureTonesSpectrum(1)
        self.updateSignal()
        self.x = x
        self.y = y
    
    # changes the signal to a user defined signal and updates
    def setSpec(self, s):
        self.spec = s
        self.updateSignal()
    
    # uses the spectrum to update the signal
    def updateSignal(self):
        self.signal = np.fft.irfft(self.spec)
        self.signalLen = len(self.signal)
    
    #gets the signal at the t'th point in time accounting for distance
    def A(self, mic, t): 
        d = self.distance(mic)
        # add extra time to account for distance
        dt = d / self.SOUND_SPEED
        i = int(t + dt) % self.signalLen
        return self.signal[i] / (d**2)
        
        
    # function for calculating coordinate distance
    def distance(self, o):
        return ((self.x - o.x)**2 + (self.y - o.y)**2)**.5
        
    
    # for generating a simple spectrum of a signal
    def randPureTonesSpectrum(self, numTones):
        s = np.zeros(512)
        for n in range(0, numTones):
            i = random.randint(0, 511)
            s[i] += 512
        return s
    
    # and if you want to pick the tones, this takes an array as frequencies
    # as an argument
    # TODO add parameters to adjust amplitude and phase shift
    def pureToneSpectrum(self, f):
        s = np.zeros(512)
        for phi in f:
            s[phi] += 512
        return s



class NoiseEmitter:
    
    x = 0
    y = 0

    def __init__(self, x = 0, y = 0, scale = 1):
        self.x = x
        self.y = y
        self.scale = scale
    
    def A(self, mic, t):
        d = self.distance(mic)
        return random.random() * self.scale / (d**2)

    # function for calculating coordinate distance
    def distance(self, o):
        return ((self.x - o.x)**2 + (self.y - o.y)**2)**.5



class Microphone:
    """ This class is for simulating a sound receiver """
    
    x = 0
    y = 0
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y



#mic = Microphone(0, 0)
#e = WaveEmitter(1, 1)
#o = NoiseEmitter(2, 2 , 1)
#e.setSpec(e.pureToneSpectrum([5, 10, 20]))


#data = np.zeros(1024)
#for n in range(0, 1024):
   #data[n] = e.A(mic, n) + o.A(mic, n)
   
#plt.plot(data)
#plt.show()