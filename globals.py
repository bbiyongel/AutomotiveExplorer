PATH = "C:/Users/mohbou/Desktop/MobilityFramework/data/"
VEHICLE = "375"

# SIG_IDS = ["23565", "23644"]
# SIG_NAMES = ["EngineSpeed", "VehicleSpeed"]

SIG_IDS = ["23913", "24707", "23676", "25273", "23565", "16617", "24031", "24030", "16772", "24376", "23644"]
SIG_NAMES = ["AcceleratorPedalPos", "AmbientAirTemperature", "BrakePedalPos", "EngineCoolantTemperature", "EngineSpeed", "FuelRate", "RelSpdFrontLeft", "RelSpdFrontRight", "SelectedGear", "SteeringWheelAngle", "VehicleSpeed"]
EXTREME = {"23913":[], "24707":[1774.9687499999998], "23676":[96.80000000000001], "25273":[215.0, 4.0], "23565":[8191.875, 0.0], "16617":[3876.198645], "24031":[8.125, -2.0], "24030":[8.125, -5.9375], "16772":[-2.0], "24376":[], "23644":[255.97970999999998]}

import datetime
D_START = datetime.datetime(year=2013, month=12, day=1, hour=9, minute=0, second=0, microsecond=0)
D_END = datetime.datetime(year=2013, month=12, day=30, hour=9, minute=0, second=0, microsecond=0)
DURATION = 15 * 60*1000 # milliseconds
