if "IPython" not in globals():
    try:
        import IPython
        IPython.get_ipython().magic("matplotlib tk")
    except:
        pass

from sklearn.metrics import silhouette_score, adjusted_rand_score, adjusted_mutual_info_score
from Visualize import Visualize
import warnings
import random
from Mode import Mode
import matplotlib.pyplot as plt
#import matplotlib.pylab as plt
import statistics as st
import numpy as np
import SignalReaderArtificial
import app
import Clustering
import globals as gb

if __name__ == '__main__':
    warnings.simplefilter(action = "ignore", category = FutureWarning)
    random.seed(1234)
    viz = Visualize()

    modesNum = [2] # Clusters
    duration = [60] # Duration window
    patternOverlap = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.] # Patterns similarity (difficulty)
    noise = [3.] # Noise level

    countryside_lowerLimit = 40#50
    countryside_higherLimit = 40#75
    countryside_waveLength = 100
    countryside_noise = 2

    highway_lowerLimit = 70
    highway_higherLimit = 70
    highway_waveLength = 100
    Highway_noise = 3

    period = gb.DURATION#3600*2 # 2 hours #60* random.randint(3*60, 5*60) #total period of simulation
    countryside_length = 200 #60 * random.randint(30, 2*60)
    highway_length = 100 # 60 * random.randint(30, 60)

    MODE_NAMES = ["b","g"]
    FSP_ari = []; SSP_ari = []; FSP_ami = []; SSP_ami = []; FSP_ho = []; SSP_ho = []; FSP_com = []; SSP_com = []; FSP_vm = []; SSP_vm = []

    countryside_mode = Mode(countryside_lowerLimit, countryside_higherLimit, countryside_waveLength, countryside_noise)
    highway_mode = Mode(highway_lowerLimit, highway_higherLimit, highway_waveLength, Highway_noise)

    VS = []
    ground_truth = []
    color_gt = []
    remain_time = period
    meanLowerLimit = st.mean([countryside_lowerLimit, highway_lowerLimit])
    meanHigherLimit = st.mean([countryside_higherLimit, highway_higherLimit])
    meanWaveLength = st.mean([countryside_waveLength, highway_waveLength])
    while remain_time > 0:
        region = random.choice([0,1])
        if region == 0: # country side
            l = min(remain_time, countryside_length)
            VS += countryside_mode.genrate_osilating_data(l, noise[0], patternOverlap[0], meanLowerLimit, meanHigherLimit, meanWaveLength)
            ground_truth.extend([region]*l)
            color_gt += [MODE_NAMES[region]]*l
            remain_time = remain_time - l
        if region == 1:
            l = min(remain_time, highway_length)
            VS += highway_mode.genrate_osilating_data(l, noise[0], patternOverlap[0], meanLowerLimit, meanHigherLimit, meanWaveLength)
            ground_truth.extend([region]*l)
            color_gt += [MODE_NAMES[region]]*l
            remain_time = remain_time - l

    #plt.scatter(range(len(VS)), VS, c=ground_truth); plt.show()

    plt.clf()
    #sss=500000
    TIME = range(len(VS))
    #plt.scatter(TIME[:sss],VS[:sss],color=ground_truth)
    plt.scatter(TIME,VS,color=color_gt)
    plt.xlim((-100,len(VS)+100))
    plt.tight_layout()
    # plt.show()

    FEATURES = ["mean"]
    SR = SignalReaderArtificial.SignalReaderArtificial(signame="VS",sigvalues=VS,modes=ground_truth)
    app = app.App([SR])
    DATA, AXES_INFO = app.build_features_data()
    #windowRanges = [xx[1][0][0] for xx in AXES_INFO]
    clust = Clustering.Clustering(DATA, scale=True, features=None).gmm(k=2) # kmeans, dpgmm, gmm
    app.init_clust_tracker(clust, AXES_INFO)

    STATS,RESULTS = app.tracking(path=gb.PLOT_PATH, )
    times_fsp,axes_fsp,labels_fsp,times_ssp,axes_ssp,labels_ssp = RESULTS
    (ari_fps, ari_sps), (ami_fps, ami_sps), (ho_fps, ho_sps), (com_fps, com_sps), (vm_fps, vm_sps) = STATS
    FSP_ari.append(ari_fps); SSP_ari.append(ari_sps)
    FSP_ami.append(ami_fps); SSP_ami.append(ami_sps)
    FSP_ho.append(ho_fps); SSP_ho.append(ho_sps)
    FSP_com.append(com_fps); SSP_com.append(com_sps)
    FSP_vm.append(vm_fps); SSP_vm.append(vm_sps)
    cl_fsp = [MODE_NAMES[xx] for xx in labels_fsp]
    plt.scatter(TIME,[130]*len(TIME),color=cl_fsp,marker="|",s=20)
    plt.text(0,120,"clustering")
    plt.scatter(TIME,[110]*len(TIME),color=[MODE_NAMES[xx] for xx in labels_ssp],marker="|",s=20)
    plt.text(0,107,"tracking")


    print("FINISH.")
    input()