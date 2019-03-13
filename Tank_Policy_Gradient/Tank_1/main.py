from models.environment import Environment
from models.Agent import Agent
import numpy as np
import keyboard
import os
import matplotlib.pyplot as plt
from params import (
    BATCH_SIZE,
    EPISODES,
    MAX_TIME,
    LIVE_REWARD_PLOT,
    RENDER,
    N_TANKS,
)

plt.style.use("ggplot")


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def main():
    # ============= Initialize variables ===========#
    environment = Environment()
    agent = Agent()
    # ================= Running episodes =================#
    episode_reward = []
    _, state, reward, actions, terminateds = [0, 0], [], [], [], []

    for e in range(EPISODES):
        environment.episode = e
        state.append(environment.reset())  # Reset level in tank
        # Running through states in the episode
        for _ in range(MAX_TIME):
            prob, action = agent.act(state[-1])
            terminated, next_state = environment.get_next_state(
                action, state[-1]
            )
            agent.drs.append(environment.get_reward(next_state, terminated))
            state.append(next_state)
            terminateds.append(terminated)
            if environment.show_rendering:
                environment.render(action)
            if terminated:
                break
        # adv = agent.remember(state,actions,reward,terminateds,adv)

        episode_reward.append(np.sum(agent.drs))
        agent.GP_replay(e)

        state, _, _, terminateds = [], [], [], []
        agent.status(episode_reward, e)
        if keyboard.is_pressed("ctrl+x"):
            break

        # Live plot rewards

        if keyboard.is_pressed("ctrl+x"):
            break
        if LIVE_REWARD_PLOT:
            environment.plot(episode_reward, agent.epsilon)
        if not environment.running:
            break

    print("##### {} EPISODES DONE #####".format(e + 1))
    plt.ioff()
    plt.clf()
    plt.plot(episode_reward)
    plt.ylabel("Episodic reward")
    plt.xlabel("Episode")
    plt.show()


if __name__ == "__main__":
    print("#### SIMULATION STARTED ####")
    print("  Max number of episodes: {}".format(EPISODES))
    print("  Max time in each episode: {}".format(MAX_TIME))
    print("  Max reward in each episode: {}".format(MAX_TIME * N_TANKS))
    print("  {}Rendring simulation ".format("" if RENDER else "Not "))
    main()