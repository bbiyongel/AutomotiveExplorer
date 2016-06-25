from Visualize import Visualize
import warnings
import random
from Mode import Mode
import matplotlib.pylab as plt
import statistics as st


if __name__ == '__main__':
    warnings.simplefilter(action = "ignore", category = FutureWarning)
    random.seed(1234)
    viz = Visualize()

    modesNum = [2] # Clusters
    duration = [60] # Duration window
    patternOverlap = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.] # Patterns similarity (difficulty)
    noise = [3.] # Noise level

    countryside_lowerLimit = 50
    countryside_higherLimit = 75
    countryside_waveLength = 4
    countryside_noise = 0.1

    highway_lowerLimit = 70
    highway_higherLimit = 90
    highway_waveLength = 4
    Highway_noise = 0.2

    period = 120 #60* random.randint(3*60, 5*60) #total period of simulation
    countryside_length = 20 #60 * random.randint(30, 2*60)
    highway_length = 10 # 60 * random.randint(30, 60)

    countryside_mode = Mode(countryside_lowerLimit, countryside_higherLimit, countryside_waveLength, countryside_noise)
    highway_mode = Mode(highway_lowerLimit, highway_higherLimit, highway_waveLength, Highway_noise)

    VS = []
    ground_truth = []
    remain_time = period
    meanLowerLimit = st.mean([countryside_lowerLimit, highway_lowerLimit])
    meanHigherLimit = st.mean([countryside_higherLimit, highway_higherLimit])
    meanWaveLength = st.mean([countryside_waveLength, highway_waveLength])
    while remain_time > 0:
        region = random.choice([0,1])
        if region == 0: # country side
            l = min(remain_time, countryside_length)
            VS += countryside_mode.genrate_osilating_data(l, noise[0], patternOverlap[3], meanLowerLimit, meanHigherLimit, meanWaveLength)
            ground_truth.extend([region]*l)
            remain_time = remain_time - l
        if region == 1:
            l = min(remain_time, highway_length)
            VS += highway_mode.genrate_osilating_data(l, noise[0], patternOverlap[3], meanLowerLimit, meanHigherLimit, meanWaveLength)
            ground_truth.extend([region]*l)
            remain_time = remain_time - l

    plt.scatter(range(len(VS)), VS, c=ground_truth); plt.show()

    print("FINISH.")
    input()