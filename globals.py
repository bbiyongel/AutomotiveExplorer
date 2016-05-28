import datetime
DATA_PATH = "C:/Users/mohbou/Desktop/MobilityFramework/data/"
PLOT_PATH = "C:/Users/mohbou/Desktop/MobilityFramework/plots/SIG_VS_ES_APP_BPP/arti_NoAgg_easy_duration/"

SIG_NAMES = {"23913":"AcceleratorPedalPos", "24707":"AmbientAirTemperature", "23676":"BrakePedalPos", "25273":"EngineCoolantTemperature", "23565":"EngineSpeed", "16617":"FuelRate", "24031":"RelSpdFrontLeft", "24030":"RelSpdFrontRight", "16772":"SelectedGear", "23644":"VehicleSpeed"}
EXTREME = {"23913":[], "24707":[1774.9687499999998], "23676":[96.80000000000001], "25273":[215.0, 4.0], "23565":[8191.875, 0.0], "16617":[3876.198645], "24031":[8.125, -2.0], "24030":[8.125, -5.9375], "16772":[-2.0], "23644":[255.97970999999998]}
# SIG_IDS = ["23913", "24707", "23676", "25273", "23565", "16617", "24031", "24030", "16772", "23644"]
# SIG_IDS = ["23644", "23565", "23913", "23676", "25273"]
SIG_IDS = ["23644", "23565", "23913", "23676"]

VEHICLE = "376"

DURATION = 10 * 60*1000 # milliseconds
MIN_SUBSEQUENCE_LEN = 10
DATED = False
K = 3




ARTIFICIAL = True

if not ARTIFICIAL:
	D_START_CLUSTERING = datetime.datetime(year=2013, month=12, day=1, hour=8, minute=0, second=0, microsecond=0)
	D_END_CLUSTERING = datetime.datetime(year=2013, month=12, day=15, hour=20, minute=0, second=0, microsecond=0)

	D_START_INIT_TRACKER = D_START_CLUSTERING
	D_END_INIT_TRACKER = D_END_CLUSTERING

	D_START_TRACKING = datetime.datetime(year=2013, month=12, day=2, hour=5, minute=0, second=0, microsecond=0)
	D_END_TRACKING = datetime.datetime(year=2013, month=12, day=2, hour=20, minute=0, second=0, microsecond=0)
	
else:
	D_START_CLUSTERING = datetime.datetime(year=2011, month=6, day=16, hour=5, minute=23, second=0, microsecond=0)
	D_END_CLUSTERING = datetime.datetime(year=2011, month=6, day=30, hour=20, minute=0, second=0, microsecond=0)

	D_START_INIT_TRACKER = D_START_CLUSTERING
	D_END_INIT_TRACKER = D_END_CLUSTERING

	D_START_TRACKING = datetime.datetime(year=2011, month=6, day=16, hour=5, minute=23, second=0, microsecond=0)
	D_END_TRACKING = datetime.datetime(year=2011, month=6, day=16, hour=20, minute=0, second=0, microsecond=0)
