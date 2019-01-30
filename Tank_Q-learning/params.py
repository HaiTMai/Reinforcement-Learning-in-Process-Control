
#=============== PARAMETERS ==================#

EPISODES = 500
MEAN_EPISODE=10
MAX_TIME = 300
SAVE_ANN_MODEL=False

# Model parameters
TANK_HEIGHT=5
TANK_RADIUS=2
TANK_PIPE_RADIUS=0.5 #m
INIT_LEVEL=0.5 # initial water level for each episode

# Choke parameters
TBCC = 1 # Time before choke change
HARD_MAX=0.9
SOFT_MAX=0.55
HARD_MIN = 0.1
SOFT_MIN = 0.45

# Disturbance params
ADD_INFLOW = True
DIST_DISTRIBUTION="gauss"
DIST_NOM_FLOW=0.4 # m^3/s
DIST_VARIANCE_FLOW= 0.1 # m^3/s
DIST_MAX_FLOW = DIST_NOM_FLOW + 3*DIST_VARIANCE_FLOW # 
DIST_MIN_FLOW=  DIST_NOM_FLOW - 3*DIST_VARIANCE_FLOW


# Agent parameters
SS_POSITION = 0.5*TANK_HEIGHT # steady state set position
VALVE_START_POSITION=0
OBSERVATIONS = 2 # Number of time steos observed
VALVE_POSITIONS= 10 # Number of valve positions 
GAMMA = 0    # discount rate
EPSILON = 1.0  # exploration rate

EPSILON_MIN = 0.001
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.05
NUMBER_OF_HIDDEN_LAYERS = [10,10]
BATCH_SIZE=20


# Render parameters
RENDER=False
LIVE_REWARD_PLOT= False
