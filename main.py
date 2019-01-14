from models.environment import Environment
from models.Agent import Agent
from params import * # Parameters used in main
import os
import numpy as np 
import keyboard
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main():
    #============= Initialize variables ===========#
    
    environment = Environment()
    agent = Agent()
    # ================= Running episodes =================#
    running=True
    all_rewards = [] 
    for e in range(EPISODES):
        action_state,states,rewards,action_delay_counter,action = environment.reset() # Reset level in tank
        # Running through states in the episode
        for t in range(MAX_TIME):    
            if action_delay_counter >= environment.action_delay:
                action_state = states[-OBSERVATIONS:]
                # Remember last action and the result from that action
                agent.remember(action_state,action,np.sum(rewards[-environment.action_delay:]))
                action = agent.predict(action_state) 
                action_delay_counter = -1 

            action_delay_counter += 1
            # Save chosen action with state
            states.append(environment.get_next_state(action)) # play out the action
            rewards.append(environment.get_reward(states[-1]))
            # Check terminate state
            if states[-1] == "Terminated":
                if action_state is not None:
                    agent.remember(action_state,action,np.sum(rewards[-environment.action_delay:]))
                break 
            if environment.show_rendering:
                environment.render(action,states[-1])
            

        # Live plot rewards
        all_rewards.append(np.sum(rewards))
        if LIVE_REWARD_PLOT:
            if keyboard.is_pressed('c'):
                break
            else:
                environment.plot(all_rewards,e)
        if not environment.running:
            break
                
        
        
    print("##### SIMULATION DONE #####")
    print("Mean rewards for all episodes: {}".format(np.mean(all_rewards))) 
    print("Mean rewards for the last 10 episodes: {}".format(np.mean(all_rewards[-10:]))) 
    print("Rewards for the last episode: {}".format(all_rewards[-1]))

if __name__ == "__main__":
    main()