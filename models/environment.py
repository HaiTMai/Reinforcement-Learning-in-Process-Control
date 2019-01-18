from models.tank_model.tank import Tank
from models.tank_model.disturbance import InflowDist
from visualize.window import Window
from params import *
import matplotlib.pyplot as plt
from drawnow import drawnow
import numpy as np 
class Environment():
    def __init__(self):
        self.model = Tank(TANK_HEIGHT,TANK_RADIUS) # get model
        self.dist = InflowDist(DIST_PIPE_RADIUS,DIST_NOM_FLOW,DIST_VARIANCE_FLOW)
        self.add_dist = ADD_INFLOW
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
            fig = plt.figure(num="Rewards per episode")  # make a figure

    def get_dhdt(self,action):
        if ADD_INFLOW:
            q_inn = self.dist.get_flow()
            q_inn = DIST_MIN_FLOW if q_inn < DIST_MIN_FLOW else q_inn
            q_inn = DIST_MAX_FLOW if q_inn > DIST_MAX_FLOW else q_inn
        else:
            q_inn = 0
        f,A_pipe,g,l,delta_p,rho,r = self.model.get_params(action) 
        return q_inn/(np.pi*r**2)-(f*A_pipe*np.sqrt(1*g*l+delta_p/rho))/(np.pi*r**2) # Eq: 1

    def get_next_state(self,action,state): 
        # models response to input change
        dldt = self.get_dhdt(action)

        # dl = self.model.get_dl_outflow(z=action)
        self.model.change_level(dldt)

        # Check terminate state
        if self.model.l < self.model.min:
            self.model.l = self.model.min 
            self.terminated = True
        elif self.model.l > self.model.max:
            self.model.l = self.model.max
            self.terminated = True
        next_state = state[1:] + [self.model.l]
        return self.terminated, next_state

            
    def reset(self):
        self.model.reset() # reset to initial tank level
        self.dist.reset() # reset to nominal disturbance
        self.terminated = False
        init_state = OBSERVATIONS*[self.model.init_l]
        return init_state, None ,init_state,0
        # state,next_state,action,rewards,action_delay_counter

    def render(self,action,next_state):
        if RENDER:
            running = self.window.Draw(action,next_state)
            if not running:
                self.running = False
    def get_reward(self,state,terminated,t):
        if terminated: # sums up the rest of the episode time
            reward = -MAX_TIME*(state[-1]-SS_POSITION)**2
            #reward = -(MAX_TIME-t)*(state[-1]-SS_POSITION)**2
            return reward
        reward = -(state[-1] - SS_POSITION)**2 # MSE
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

