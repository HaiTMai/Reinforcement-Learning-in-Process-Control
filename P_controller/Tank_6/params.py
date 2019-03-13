MAIN_PARAMS = {
    "Episodes": 1,
    "Mean_episodes": 20,
    "Max_time": 200,
    "RENDER": False,
    "LIVE_REWARD_PLOT": False,
}
# Agent parameters
AGENT1_PARAMS = {
    "SS_POSITION": 0.5,  # steady state set position
    "VALVE_START_POSITION": 0.5,
    "ACTION_DELAY": 5,
    "INIT_POSITION": 0.5,
    "KC": 0.16,
}

AGENT2_PARAMS = {
    "SS_POSITION": 0.5,  # steady state set position
    "VALVE_START_POSITION": 0.5,
    "ACTION_DELAY": 5,
    "INIT_POSITION": 0.5,
    "KC": 0.10,
}

TANK1_PARAMS = {
    "height": 10,
    "init_level": 0.5,
    "width": 3,
    "pipe_radius": 0.5,
    "max_level": 0.9,
    "min_level": 0.1,
}

TANK1_DIST = {
    "add": True,
    "nom_flow": 1,  # 2.7503
    "var_flow": 0.1,
    "max_flow": 2,
    "min_flow": 0.7,
    "add_step": False,
    "step_time": int(MAIN_PARAMS["Max_time"] / 2),
    "step_flow": 2,
}

TANK2_PARAMS = {
    "height": 10,
    "init_level": 0.5,
    "width": 3,
    "pipe_radius": 0.5,
    "max_level": 0.9,
    "min_level": 0.1,
}

TANK2_DIST = {
    "add": False,
    "nom_flow": 1,  # 2.7503
    "var_flow": 0.1,
    "max_flow": 1.3,
    "min_flow": 0.7,
    "add_step": False,
    "step_time": int(MAIN_PARAMS["Max_time"] / 2),
    "step_flow": 2,
}
TANK3_DIST, TANK4_DIST, TANK5_DIST, TANK6_DIST = (
    TANK2_DIST,
    TANK2_DIST,
    TANK2_DIST,
    TANK2_DIST,
)
TANK3_PARAMS, TANK4_PARAMS, TANK5_PARAMS, TANK6_PARAMS = (
    TANK2_PARAMS,
    TANK2_PARAMS,
    TANK2_PARAMS,
    TANK2_PARAMS,
)
AGENT3_PARAMS, AGENT4_PARAMS, AGENT5_PARAMS, AGENT6_PARAMS = (
    AGENT2_PARAMS,
    AGENT2_PARAMS,
    AGENT2_PARAMS,
    AGENT2_PARAMS,
)

AGENT_PARAMS_LIST = [
    AGENT1_PARAMS,
    AGENT2_PARAMS,
    AGENT3_PARAMS,
    AGENT4_PARAMS,
    AGENT5_PARAMS,
    AGENT6_PARAMS,
]
TANK_PARAMS_LIST = [
    TANK1_PARAMS,
    TANK2_PARAMS,
    TANK3_PARAMS,
    TANK3_PARAMS,
    TANK3_PARAMS,
    TANK3_PARAMS,
]
TANK_DIST_LIST = [
    TANK1_DIST,
    TANK2_DIST,
    TANK3_DIST,
    TANK4_DIST,
    TANK5_DIST,
    TANK6_DIST,
]
