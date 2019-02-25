# Add the ptdraft folder path to the sys.path list
# sys.path.append("C:/Users/eskil/Google Drive/Skolearbeid/5. klasse/Master")
from models.environment import Environment
from models.Agent import Agent
from params import MAIN_PARAMS, AGENT_PARAMS, TANK_PARAMS, TANK_DIST
import os
import matplotlib.pyplot as plt
import numpy as np
import keyboard
from rewards import get_reward_2 as get_reward

plt.style.use("ggplot")


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def main():
    # ============= Initialize variables and objects ===========#
    max_mean_reward = 100
    environment = Environment(TANK_PARAMS, TANK_DIST, MAIN_PARAMS)
    agent = Agent(AGENT_PARAMS)
    mean_episode = MAIN_PARAMS["MEAN_EPISODE"]
    episodes = MAIN_PARAMS["EPISODES"]
    all_rewards = []
    all_mean_rewards = []

    # ================= Running episodes =================#
    for e in range(episodes):
        states, episode_reward = environment.reset()  # Reset level in tank
        agent.reset(states)

        for t in range(MAIN_PARAMS["MAX_TIME"]):
            action = agent.act(states[-1])  # get action choice from state
            z = agent.get_z(action)

            terminated, next_state = environment.get_next_state(
                z, states[-1]
            )  # Calculate next state with action
            reward = get_reward(
                next_state, terminated
            )  # get reward from transition to next state

            # Store data
            episode_reward.append(np.sum(reward))

            agent.remember(states, next_state, reward, terminated, t)

            states.append(next_state)

            if environment.show_rendering:
                environment.render(z)
            if terminated:
                break

        all_rewards.append(np.sum(np.array(episode_reward)))

        # Print mean reward and save better models
        if e % mean_episode == 0 and e != 0:
            mean_reward = np.mean(all_rewards[-mean_episode:])
            all_mean_rewards.append(mean_reward)
            print(
                "rewards the last {} of {}/{} episodes : {} explore: {}".format(
                    mean_episode,
                    e,
                    episodes,
                    mean_reward,
                    round(agent.epsilon, 2),
                )
            )
            if agent.save_model_bool:
                max_mean_reward = agent.save_model(mean_reward, max_mean_reward)
            # Train model
            if agent.is_ready():
                agent.Qreplay(e)

        if keyboard.is_pressed("ctrl+x"):
            break

        if environment.live_plot:
            environment.plot(all_rewards, agent.epsilon)
        if not environment.running:
            break

    print("##### {} EPISODES DONE #####".format(e + 1))
    print("Max rewards for all episodes: {}".format(np.max(all_rewards)))
    plt.ioff()
    plt.clf()
    x_range = np.arange(0, e - e % mean_episode, mean_episode)
    plt.plot(x_range, all_mean_rewards)
    plt.ylabel("Mean rewards of last {} episodes".format(mean_episode))
    plt.show()


if __name__ == "__main__":
    print("#### SIMULATION STARTED ####")
    print("  Max number of episodes: {}".format(MAIN_PARAMS["EPISODES"]))
    print("  Max time in each episode: {}".format(MAIN_PARAMS["MAX_TIME"]))
    print(
        "  {}Rendring simulation ".format(
            "" if MAIN_PARAMS["RENDER"] else "Not "
        )
    )
    main()
