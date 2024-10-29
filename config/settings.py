import os

# Database Configuration
db_dir = "/home/g1/Documents/Dynamic-RideSharing-Pooling-Simulator/db/data/db.sqlite3"
DB_HOST_PATH = f"sqlite:///{db_dir}"

# Use 'localhost:5000' as a default if OSRM_HOSTPORT is not set
OSRM_HOSTPORT = os.getenv("OSRM_HOSTPORT", "localhost:5000")

if not OSRM_HOSTPORT:
    raise EnvironmentError("OSRM_HOSTPORT environment variable is not set.")

# Verify database availability
if not os.path.exists(db_dir):
    raise FileNotFoundError(f"Database not found: {db_dir}")

# Log and Data Directories
DEFAULT_LOG_DIR = "logs/tmp"
DATA_DIR = "data"

# Map and Bounding Box Configuration
CENTER_LATITUDE = 40.75
CENTER_LONGITUDE = -73.90
LAT_WIDTH = 18.0 / 60  # degrees
LON_WIDTH = 18.0 / 60  # degrees

MIN_LAT = CENTER_LATITUDE - LAT_WIDTH / 2.0
MIN_LON = CENTER_LONGITUDE - LON_WIDTH / 2.0
MAX_LAT = CENTER_LATITUDE + LAT_WIDTH / 2.0
MAX_LON = CENTER_LONGITUDE + LON_WIDTH / 2.0

BOUNDING_BOX = [[MIN_LAT, MIN_LON], [MAX_LAT, MAX_LON]]
DELTA_LON = 21.0 / 3600  # degrees
DELTA_LAT = 16.0 / 3600  # degrees

# Calculate Map Dimensions
MAP_WIDTH = int(LON_WIDTH / DELTA_LON) + 1
MAP_HEIGHT = int(LAT_WIDTH / DELTA_LAT) + 1

# Simulation Timings
TIMESTEP = 60  # seconds
MIN_DISPATCH_CYCLE = 60 * 7.5
MAX_DISPATCH_CYCLE = 60 * 10
GLOBAL_STATE_UPDATE_CYCLE = 60 * 5

# Validate consistency of dispatch cycles
assert MIN_DISPATCH_CYCLE <= MAX_DISPATCH_CYCLE, \
    "Minimum dispatch cycle cannot be greater than the maximum dispatch cycle."

OFF_DURATION = 60 * 60  # 1 hour
PICKUP_DURATION = 60 * 1  # 1 minute
MIN_WORKING_TIME = 3600 * 20
MAX_WORKING_TIME = 3600 * 21
ENTERING_TIME_BUFFER = 3600 * 4  # 4 hours
DESTINATION_PROFILE_TEMPORAL_AGGREGATION = 3 #hours
DESTINATION_PROFILE_SPATIAL_AGGREGATION = 5 #(x, y) coordinates

# Not in use for now
DEMAND_AMPLIFICATION_FACTOR = 1.0