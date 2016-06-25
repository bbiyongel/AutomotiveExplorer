import random as random
import statistics
import numpy as np

class Mode(object):
    lowerLimit = 0.
    higherLimit = 0.
    length = 0.
    noise = 0.

    # constructor
    def __init__(self, lowerLimit, higherLimit, waveLength, noise):
        self.lowerLimit = lowerLimit
        self.higherLimit = higherLimit
        self.waveLength = waveLength
        self.noise = noise

    # def adjust_overlap(self, overlapLevel, value_ll, value_hl, value_len, value_ns):
    #      self.lowerLimit = self.lowerLimit +  overlapLevel * (value_ll - self.lowerLimit)
    #      self.higherLimit = self.higherLimit +  overlapLevel * (value_hl - self.higherLimit)
    #      self.length = self.length +  overlapLevel * (value_len - self.length)
    #      self.noise = self.noise +  overlapLevel * (value_ns - self.noise)

    def genrate_osilating_data(self, length, noise=0, overlap=0, targetLowerLimit = 0, targetHigherLimit = 0, targetWaveLength = 0):
        def get_closer(relativeValue, targetValue, level=0):
            if(level <= 1 and level >=0):
                relativeValue = relativeValue + level*(targetValue - relativeValue)
            else:
                print('warning: overlap level was not between 0 and 1. Level is considered to be zero.')
            return relativeValue

        lowerLimit = self.lowerLimit
        higherLimit = self.higherLimit
        waveLength = np.int(self.waveLength)
        if(overlap <=1 and overlap > 0):
            lowerLimit = get_closer(self.lowerLimit, targetLowerLimit, overlap)
            higherLimit = get_closer(self.higherLimit, targetHigherLimit, overlap)
            waveLength = np.int(get_closer(self.waveLength, targetWaveLength, overlap))

        len = length
        data = []
        while(len > 0):
            for i in range(min(waveLength, len)):
                data.extend([random.gauss(lowerLimit, self.noise)])
            len = len - min(waveLength, len)
            for i in range(min(waveLength, len)):
                data.extend([random.gauss(higherLimit, self.noise)])
            len = len - min(waveLength, len)

        return data

    # def genrate_uniform_data(self, length, noise=0, overlap=0):
    #     len = length
    #     data = []
    #     while(len > 0):
    #         data.extend([random.uniform(self.lowerLimit, self.higherLimit)])
    #     return data
