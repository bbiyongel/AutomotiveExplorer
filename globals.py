import datetime
import time
SIG_NAMES = {"23913":"AcceleratorPedalPos", "24707":"AmbientAirTemperature", "23676":"BrakePedalPos", "25273":"EngineCoolantTemperature", "23565":"EngineSpeed", "16617":"FuelRate", "24031":"RelSpdFrontLeft", "24030":"RelSpdFrontRight", "16772":"SelectedGear", "23644":"VehicleSpeed"}
EXTREME = {"23913":[], "24707":[1774.9687499999998], "23676":[96.80000000000001], "25273":[215.0, 4.0], "23565":[8191.875, 0.0], "16617":[3876.198645], "24031":[8.125, -2.0], "24030":[8.125, -5.9375], "16772":[-2.0], "23644":[255.97970999999998]}
DATA_PATH = "C:/Users/mohbou/Desktop/MobilityFramework/data/"
MIN_SUBSEQUENCE_LEN = 10

# -----------------------------------------------------------------
# SIG_IDS = ["23913", "24707", "23676", "25273", "23565", "16617", "24031", "24030", "16772", "23644"]
SIG_IDS = ["23644", "23565", "23913", "23676"]

VEHICLE = "376"

DURATION = 15 * 60*1000 # milliseconds
K = 3
PROBA_TYPE = "empirical"
# PROBA_TYPE = "normal"
# PROBA_TYPE = "multivariate"

ARTIFICIAL = True
PLOT_PATH = "C:/Users/mohbou/Desktop/MobilityFramework/plots/TEST/"+".".join(SIG_IDS)+"-"+VEHICLE+"-Art"+str(ARTIFICIAL)+"-K"+str(K)+"-"+PROBA_TYPE+"-D"+str(DURATION/(60*1000))+"---"+str(time.time())+"/"

# -----------------------------------------------------------------
if not ARTIFICIAL:
	DATED = True
	
	D_START_CLUSTERING = datetime.datetime(year=2013, month=12, day=1, hour=8, minute=0, second=0, microsecond=0)
	D_END_CLUSTERING = datetime.datetime(year=2013, month=12, day=30, hour=20, minute=0, second=0, microsecond=0)

	D_START_INIT_TRACKER = D_START_CLUSTERING
	D_END_INIT_TRACKER = D_END_CLUSTERING

	D_START_TRACKING = datetime.datetime(year=2013, month=12, day=2, hour=5, minute=0, second=0, microsecond=0)
	D_END_TRACKING = datetime.datetime(year=2013, month=12, day=3, hour=20, minute=0, second=0, microsecond=0)
	
else:
	DATED = False
	D_START_CLUSTERING = datetime.datetime(year=2011, month=6, day=16, hour=5, minute=23, second=0, microsecond=0)
	D_END_CLUSTERING = datetime.datetime(year=2011, month=6, day=30, hour=20, minute=0, second=0, microsecond=0)

	D_START_INIT_TRACKER = D_START_CLUSTERING
	D_END_INIT_TRACKER = D_END_CLUSTERING

	D_START_TRACKING = datetime.datetime(year=2011, month=6, day=16, hour=5, minute=23, second=0, microsecond=0)
	D_END_TRACKING = datetime.datetime(year=2011, month=6, day=17, hour=20, minute=0, second=0, microsecond=0)
