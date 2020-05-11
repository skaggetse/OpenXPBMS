# COMPORT SETUP
sPort = '/dev/ttyUSB0'

# How many Batteries in string
batteries = 11

# Capacity of battery (Ah)
packCapacity = 120

# Current sensor
# Max current sensor offset at idle (A)
currentOffset = 0.3

# Resistance calculation trigger (A / second)
packRtrigger = 80.0

# Voltage limits for shutdown
hVoltLimit = 3600
lVoltLimit = 2800

# Remove UI
debug = False

# Read interval (s)
readInterval = 0.5

# Logging
path = '/home/pi/OpenXPBMS/RaspbPi/logs/'
loglevel = 'module' #'pack' or 'module'
nthlog = 1
