from params import MAIN_PARAMS, AGENT_PARAMS, TANK_DIST

MAIN_PARAMS["RENDER"] = True
MAIN_PARAMS["LIVE_REWARD_PLOT"] = False

AGENT_PARAMS["EPSILON"] = [0] * 6
AGENT_PARAMS["SAVE_MODEL"] = [False] * 6
AGENT_PARAMS["LOAD_MODEL"] = [True] * 6
AGENT_PARAMS["TRAIN_MODEL"] = [False] * 6
AGENT_PARAMS["MODEL_NAME"] = ["Network_[5, 5]HL"] * 6
AGENT_PARAMS["Z_VARIANCE"] = [0] * 6


# for i in range(1,AGENT_PARAMS["N_TANKS"]):
#     TANK_DIST[i]["add"] = True
#     TANK_DIST[i]["var_flow"] = 0
#     TANK_DIST[i]["nom_flow"] = 0
#     TANK_DIST[i]["add_step"] = False
#     TANK_DIST[i]["pre_def_dist"] = False
