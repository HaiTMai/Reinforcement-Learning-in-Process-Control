from models.tank_model.tank import Tank
from models.tank_model.disturbance import InflowDist
from visualize.window import Window
import matplotlib.pyplot as plt
from drawnow import drawnow
import numpy as np 
from params import SS_POSITION,TANK1_PARAMS,TANK1_DIST,TANK2_DIST,TANK2_PARAMS,\
    TBCC,OBSERVATIONS,RENDER,LIVE_REWARD_PLOT
class Environment():
    def __init__(self):
        
        self.model1 = Tank(
            height=TANK1_PARAMS['height'],
            radius=TANK1_PARAMS['width'],
            max_level=TANK1_PARAMS['max_level'],
            min_level=TANK1_PARAMS['min_level'],
            pipe_radius=TANK1_PARAMS['pipe_radius'],
            dist = TANK1_DIST
            ) 
        self.model2 = Tank(
            height=TANK2_PARAMS['height'],
            radius=TANK2_PARAMS['width'],
            max_level=TANK2_PARAMS['max_level'],
            min_level=TANK2_PARAMS['min_level'],
            pipe_radius=TANK2_PARAMS['pipe_radius'],
            dist = TANK2_DIST,
            prev_tank=self.model1
            ) 
        self.model = []
        self.model.append(self.model1)
        self.model.append(self.model2)
        
        self.action_delay= TBCC
        self.action_delay_counter = -OBSERVATIONS # Does not train on initial settings
        self.running = True
        self.episode = 0
        self.all_rewards = []
        self.terminated = False

        self.show_rendering= RENDER
        self.live_plot = LIVE_REWARD_PLOT
        if RENDER:
            self.window = Window(self.model)
        if LIVE_REWARD_PLOT:
            plt.ion()  # enable interactivity
            plt.figure(num="Rewards per episode")  # make a figure

    def get_next_state(self,z,state): 
        # models response to input change
        prev_q_out = 0
        next_state = []
        for i,tank in enumerate(self.model):
            dldt,prev_q_out = tank.get_dhdt(z[i],prev_q_out) 
            tank.change_level(dldt)

            # Check terminate state
            if tank.l < tank.min:
                self.terminated = True
                tank.l = tank.min
            elif tank.l > tank.max:
                self.terminated = True
                tank.l = tank.max
            if i == 0:
                next_state.append([tank.l/tank.h,(dldt+1)/2,0])
            else:
                next_state.append([tank.l/tank.h,(dldt+1)/2,z[i-1]])
                
        next_state = np.array(next_state)
        next_state = next_state.reshape(1,next_state.shape[0],next_state.shape[1])
        return self.terminated, next_state

            
    def reset(self):
        state = []
        self.terminated = False
        for tank in self.model:
            tank.reset() # reset to initial tank level
            if tank.add_dist:
                tank.dist.reset() # reset to nominal disturbance
            init_state = [tank.init_l/tank.h,0,0] #Level plus gradient
            state.append(init_state)
        state = np.array(state)
        state = state.reshape(1,state.shape[0],state.shape[1])
        return state,TBCC,state,[]

    def render(self,action):
        if RENDER:
            running = self.window.Draw(action)
            if not running:
                self.running = False

    def get_reward(self,state,terminated):
        reward = 0
        if terminated:
            return -10
        for sub_state in state[0]:
            if sub_state[0] > 0.25 and sub_state[0] < 0.75:
                reward +=1
        return reward
        
    def plot_rewards(self):
        plt.plot(self.all_rewards,label="Exploration rate: {} %".format(self.epsilon*100))
        plt.legend()

    def plot(self,all_rewards,epsilon):
        self.all_rewards = all_rewards
        self.epsilon = round(epsilon,4)
        try:
            drawnow(self.plot_rewards)
        except:
            print("Break")

