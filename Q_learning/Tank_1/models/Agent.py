from collections import deque
import torch
from Q_learning.Tank_1.models.Network import NetWork
import numpy as np 
import random
import itertools
class Agent():
    def __init__(self,AGENT_PARAMS): 
        "Parameters are set in the params.py file"

        self.state_size = AGENT_PARAMS['OBSERVATIONS']
        self.action_size = AGENT_PARAMS['VALVE_POSITIONS']
        self.action_choices = self._get_action_choices(self.action_size)
        self.memory_size = AGENT_PARAMS['MEMORY_LENGTH']
        self.memory =deque(maxlen=self.memory_size)
        self.gamma = AGENT_PARAMS['GAMMA'] 
        self.epsilon = AGENT_PARAMS['EPSILON'] if AGENT_PARAMS['TRAIN_MODEL'] else AGENT_PARAMS['EPSILON_MIN'] 
        self.epsilon_min =AGENT_PARAMS['EPSILON_MIN']
        self.epsilon_decay = AGENT_PARAMS['EPSILON_DECAY']
        self.learning_rate = AGENT_PARAMS['LEARNING_RATE']
        self.train_model = AGENT_PARAMS['TRAIN_MODEL']
        self.load_model = AGENT_PARAMS['LOAD_MODEL']
        self.save_model_bool = AGENT_PARAMS['SAVE_MODEL']
        self.batch_size = AGENT_PARAMS['BATCH_SIZE']
        self.buffer = 0
        self.buffer_thres = AGENT_PARAMS['BUFFER_THRESH']
        self.Q_eval, self.Q_next = self._build_ANN(
            self.state_size,
            AGENT_PARAMS['HIDDEN_LAYER_SIZE'],
            self.action_size,
            learning_rate=self.learning_rate
        )
        
    
    def _get_action_choices(self,action_size):
        "Create a list of the valve positions ranging from 0-1 with acrion_size positiong"
        valve_positions= []
        for i in range(action_size):
            valve_positions.append((i)/(action_size-1))
        return np.array(list(reversed(valve_positions)))

    def _build_ANN(self,input_size,hidden_size,action_size,learning_rate):  
        "Creates or loads a ANN valve function approximator"  
        Q_eval = NetWork(input_size,hidden_size,action_size,learning_rate)
        Q_next = NetWork(input_size,hidden_size,action_size,learning_rate)
        return Q_eval, Q_next

    def remember(self, state, action, next_state,reward,done):
        "Stores instances of each time step"
        if self.train_model:
            next_state=np.array(next_state)
            # next_state=next_state.reshape(1,next_state.size)
            # if len(self.memory)> self.memory_size:
            # self.memory[random.randint(0,self.memory_size)] = [state, action, reward,next_state,done]
            # else:
            self.memory.append(np.array([state, action, reward, next_state,done]))
            self.buffer += 1

    def act_greedy(self,state):
        "Predict the optimal action to take given the current state"
        
        choice = self.Q_eval.forward(state)
        action = torch.argmax(choice).item()
        return action
         
    def act(self, states):
        "Agent uses the state and gives either an action of exploration or explotation"
        
        if np.random.rand() <= self.epsilon: # Exploration 
            random_action = random.randint(0,self.action_size-1)
            return random_action
        return self.act_greedy(states) # Exploitation

    def is_ready(self):
        "Check if enough data has been collected"
        
        if not self.train_model: #Model has been set to not collect data
            return False
        if len(self.memory)< self.batch_size:
            return False
        if self.buffer < self.buffer_thres:
            return False
        return True

    def Qreplay(self,e):
        "Train the model to improve the predicted value of consecutive recurring states, Off policy Q-learning with batch training"
        
        self.Q_eval.zero_grad()
        minibatch = np.array(random.sample(self.memory, self.batch_size))
        states = np.stack(minibatch[:,0])
        actions = np.stack(minibatch[:,1])
        rewards = np.stack(minibatch[:,2])
        next_states = np.stack(minibatch[:,3])
        terminated = np.stack(minibatch[:,4])
        

        self.Q_eval.zero_grad()
        Qpred = self.Q_eval.forward(states).to(self.Q_eval.device)
        Qnext = self.Q_next.forward(next_states).to(self.Q_next.device) 

        maxA = Qnext.max(1)[1]#.to(self.Q_eval.device) 
        rewards = torch.tensor(rewards,dtype=torch.float32).to(self.Q_eval.device)
        Q_target = Qpred.clone()
        for i,Qnext_a in enumerate(maxA):
            if not terminated[i]:
                Q_target[i,actions[i]]=rewards[i]#+self.gamma*torch.max(Qnext[i,Qnext_a])
            else:
                Q_target[i,actions[i]]=rewards[i]
         
        # + self.gamma*torch.max(Qnext[0,0,:])
        
        
        y_test = Q_target.clone()
        y_pred = Qpred.clone()
        loss = self.Q_eval.loss(y_pred, y_test).to(self.Q_eval.device)
        loss.backward()
        
        self.Q_eval.optimizer.step()
        self.decay_exploration()

    def decay_exploration(self):
        "Lower the epsilon valvue to favour greedy actions"

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save_model(self,mean_reward,max_mean_reward):
        "Save the model given a better model has been fitted"

        if mean_reward >= max_mean_reward:
            pass
                # model_name = "/ANN_"+ str(NUMBER_OF_HIDDEN_LAYERS)+"HL"
                # model_path = "Q_learning/1_Tank/saved_ANN_models" + model_name+ ".h5"
                # self.ANN_model.save(model_path)
                # print("ANN_Model was saved")
                # max_mean_reward = mean_reward
        return max_mean_reward