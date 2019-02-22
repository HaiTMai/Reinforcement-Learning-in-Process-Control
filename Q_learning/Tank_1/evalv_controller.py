# Add the ptdraft folder path to the sys.path list
# sys.path.append("C:/Users/eskil/Google Drive/Skolearbeid/5. klasse/Master")
from models.environment import Environment
from models.Agent import Agent
from evalv_params import MAIN_PARAMS, AGENT_PARAMS, TANK_PARAMS, TANK_DIST
import os
import matplotlib.pyplot as plt
import numpy as np
import keyboard
from rewards import get_reward_2 as get_reward

plt.style.use("ggplot")


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def main():
    # ============= Initialize variables and objects ===========#
    environment = Environment(TANK_PARAMS, TANK_DIST, MAIN_PARAMS)
    agent = Agent(AGENT_PARAMS)
    actions = []
    h = []
    d = []
    # disturbance = []
    # ================= Running episodes =================#
    state, next_state, episode_reward = environment.reset()
    h.append(state)
    for _ in range(MAIN_PARAMS["MAX_TIME"]):
        action = agent.act(state)  # get action choice from state
        z = agent.action_choices[
            action
        ]  # convert action choice into valve position
        actions.append(z)
        terminated, next_state = environment.get_next_state(
            z, state
        )  # Calculate next state with action
        d.append(environment.tank.dist.flow)
        reward = get_reward(
            next_state, terminated
        )  # get reward from transition to next state

        # Store data
        episode_reward.append(reward)
        agent.remember(state, action, next_state, reward, terminated)

        state = next_state
        h.append(state)
        if environment.show_rendering:
            environment.render(z)
        if terminated:
            break
        # End for

        if keyboard.is_pressed("ctrl+x"):
            break

        if not environment.running:
            break
    print(np.sum(episode_reward))
    _, (ax1, ax2, ax3) = plt.subplots(3, sharex=False, sharey=False)

    l1, = ax1.plot(h[:-1], color="peru")
    ax1.set_ylim(0, 1)
    l2, = ax2.plot(actions[1:], color="firebrick")
    ax2.set_ylim(0, 1.01)
    l3, = ax3.plot(d[:-1], color="dimgray")

    plt.legend([l1, l2, l3], ["Tank height", "Valve position", "Disturbance"])
    plt.tight_layout()
    plt.xlabel("Time")
    plt.show()


if __name__ == "__main__":
    print("#### SIMULATION EVALUATION STARTED ####")
    print("  Max time in each episode: {}".format(MAIN_PARAMS["MAX_TIME"]))
    main()
