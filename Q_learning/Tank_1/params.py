MAIN_PARAMS = {
    "EPISODES": 20000,
    "MEAN_EPISODE": 50,
    "MAX_TIME": 200,
    "RENDER": False,
    "MAX_MEAN_REWARD": 20,  # minimum reward before saving model
}

AGENT_PARAMS = {
    "N_TANKS": 1,
    "SS_POSITION": 0.5,
    "VALVE_START_POSITION": 0.2,
    "ACTION_DELAY": [5],
    "INIT_ACTION": 0,
    "VALVE_POSITIONS": 10,
    "EPSILON": [1],
    "EPSILON_MIN": [0.05],
    "EPSILON_DECAY": [0.995],
    "LEARNING_RATE": [0.0001],
    "HIDDEN_LAYER_SIZE": [[1]],
    "BATCH_SIZE": 5,
    "MEMORY_LENGTH": 10000,
    "OBSERVATIONS": 4,  # level, gradient, is_above 0.5, prevous valve position
    "GAMMA": 0.9,
    "SAVE_MODEL": [True],
    "LOAD_MODEL": [False],
    "TRAIN_MODEL": [True],
    "LOAD_MODEL_NAME": ["Network_[5, 5]HL0"],
    "LOAD_MODEL_PATH": "Q_learning/Tank_1/saved_networks/training_networks/",
    "SAVE_MODEL_PATH": "Q_learning/Tank_1/saved_networks/training_networks/",
}

# Model parameters Tank 1
TANK1_PARAMS = {
    "height": 10,
    "init_level": 0.5,
    "width": 10,
    "pipe_radius": 0.5,
    "max_level": 0.75,
    "min_level": 0.25,
}

TANK1_DIST = {
    "add": True,
    "pre_def_dist": True,
    "nom_flow": 1,  # 2.7503
    "var_flow": 0.1,
    "max_flow": 2,
    "min_flow": 0.7,
    "add_step": False,
    "step_time": int(MAIN_PARAMS["MAX_TIME"] / 2),
    "step_flow": 2,
    "max_time": MAIN_PARAMS["MAX_TIME"],
}

TANK_PARAMS = [TANK1_PARAMS]
TANK_DIST = [TANK1_DIST]
