import soundfile as sf
import numpy as np
import math
import scipy

def loadFile( fileName ):
    sig, sampleRate = sf.read( fileName )
    return sig, sampleRate

def getSpectrogram(signal, frameTime, sampleRate):
    spec = []
    interval = int(sampleRate * frameTime)
    frames = int(len(signal) / interval)
    for f in range(0, frames - 1):
        segment = signal[f * interval : (f + 1) * interval]
        spec.append(fftp.rfft(segment))
    return spec

# computes short time fourier transform
# WARNING: discards phase data
def stft(x, fs, framesz = .05, hop = .025):
    framesamp = int(framesz*fs)
    hopsamp = int(hop*fs)
    w = scipy.hanning(framesamp)
    X = scipy.array([np.fft.rfft(w*x[i:i+framesamp]) 
                     for i in range(0, len(x)-framesamp, hopsamp)])
    return np.real(X)

# computes the mean spectrum from a spectrogram
def meanSpectrum(spec):
    l = len(spec[0])
    meanSpec = np.zeros(l)
    for s in spec:
        meanSpec = np.add(meanSpec, s)
    return np.divide(meanSpec, l)

# array of P(x) values for a probability mass function
def pmf(sample, bins = 1000):
    n = len(sample)
    N = 1.0/n #for dividing stuff later
    sMin = min(sample)
    sMax = max(sample)
    rng = sMax - sMin
    p = np.zeros(bins)
    for x in sample:
        i = int((x - sMin) * (bins - 1) /rng)
        p[i] += N
    return p

# computes Ht or Hf for the Acoustic Entropy Index
def shannon(pf):
    n = len(pf)
    ln = np.log2(n) # saves us a calculation in the for loop
    S = 0
    for x in pf:
        if x != 0:
            S += x * np.log2(x) / ln
    return 0 - S

# uses Ht and Hf to calculate the Acoustic Entropy Index of a sound sample
def calculateAEI(x, hz):
    spec = stft(x, hz)
    Ht = shannon(pmf(x))
    Hf = shannon(pmf(meanSpectrum(spec)))
    return Ht * Hf

def calculateACI(spec):
    bins = len(spec[0]) #number of frequency bins
    sumdk = np.zeros(bins)
    sumIk = np.zeros(bins)
    for t in range(0, len(spec) -1):
        dk = np.absolute( np.subtract(spec[t], spec[t+1]) )
        sumdk = np.add(sumdk, dk)
        sumIk = np.add(sumIk, spec[t])
    ACI = np.divide(sumdk, sumIk)
    return np.sum(ACI)


        
#arr, hz = loadFile( "sample.wav" )
#spec = getSpectrogram(arr, .01, hz)
#print calculateBandAverage(spec)