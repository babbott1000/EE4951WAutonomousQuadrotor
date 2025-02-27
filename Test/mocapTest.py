from vicon_dssdk.ViconDataStream import *
from time import sleep


# ========= CONSTANTS =========
MS_PER_SECOND = 1000


# ======= CONFIGRUATION ========
CONNECTION_TIMEOUT_MS = 100
LOOP_PERIOD_S = 250 / MS_PER_SECOND
CONNECTION_BUCKET_THRESHOLD = 10
VICON_HOSTNAME = "localhost"
DRONE_NAMES = [ ("Drone", "Drone") ]

# ====== GLOBAL VARIABLES ======
client = Client()

leaky_bucket = 0

while leaky_bucket < CONNECTION_BUCKET_THRESHOLD:
    while client.IsConnected():
        leaky_bucket = max(0, leaky_bucket - 1)
        client.GetFrame()
        for drone in DRONE_NAMES:
            pos, occluded = client.GetSegmentGlobalTranslation(drone[0], drone[1])
            rot, _ = client.GetSegmentGlobalRotationQuaternion(drone[1], drone[1])
            if occluded:
                print("Drone is not visible")
            else:
                print(f"Current drone position is {tuple([float('{:.1f}'.format(p)) for p in pos])} and rotation is {tuple([float('{:.4f}'.format(r)) for r in rot])}")
        sleep(LOOP_PERIOD_S)
    else:
        print(f"No connection to client, attempting to connect to {VICON_HOSTNAME}")
        leaky_bucket += 1
        client.SetConnectionTimeout(CONNECTION_TIMEOUT_MS)
        client.Connect(VICON_HOSTNAME)
        client.EnableSegmentData()
        if client.IsConnected():
            print(f"Connection to {VICON_HOSTNAME} successful")

print("Could not establish connection to client")