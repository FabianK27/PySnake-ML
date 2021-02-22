import random

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

import numpy as np
import matplotlib.pyplot as plt

from models import deepQNetwork
import constants
import pygame
from pySnakeML import gameLoopML
from replayMemory import *
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train():
    
    if constants.headless:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

    # init a network and a replay buffer and an optimizer
    dqn = deepQNetwork(num_actions=constants.num_actions, input_channles=constants.scenes_toNet).float().to(device)
    opt = optim.RMSprop(dqn.parameters()) # could change optimizers later
    replayMem = replayMemory(constants.replayBufferCapacity)
    # define a list to keep track of training success
    finalLength =  []

    action = random.randrange(0, constants.num_actions) # first action is random
    # main epoch loops
    for epoch in range(constants.num_epochs):
        print("running episode " + str(epoch))
        # initiate a game instance
        gLoop = gameLoopML(constants.windowWidth, constants.windowHeight, str(epoch))
        #initiate state buffers
        state = [gLoop.get_screen(), gLoop.get_screen()]
        next_state = [gLoop.get_screen(), gLoop.get_screen()]
        # enter game loop
        steps_done = 0
        while(steps_done < constants.MAX_STEPS):
            steps_done += 1
            next_state[0] = state[1] #update next state to before movement 
            #perform step
            reward, gameOver = gLoop.step(action)
            #update next state to current screen after movement
            next_state[1] = gLoop.get_screen()
            #add to replay buffer
            replayMem.push(torch.cat((state[0], state[1]), 1), action, torch.cat((next_state[0], next_state[1]), 1), reward, gameOver)
            # make next state current state
            state[0] = next_state[0]
            state[1] = next_state[1]
            #get next action
            action = dqn.get_action(torch.cat((state[0], state[1]), 1))
            # train model
            optimize(dqn, opt, replayMem)
            # start next game if over
            if gameOver:
                finalLength.append(gLoop.snake.getLength())
                print("game ended with length: " + str(finalLength[-1]))
                break
        
        del gLoop

    #print results and save model weights
    print(finalLength)
    torch.save(dqn.state_dict(), './snake_NN.pth')

    pygame.quit()

def optimize(network, optimizer, memory):
    if (len(memory) < constants.BATCH_SIZE):
        return
    #sample a batch
    exp_batch = memory.sample(constants.BATCH_SIZE)
    # generate training set from batch
    inputs = torch.zeros(constants.BATCH_SIZE, device=device) # Q(state, action) values assigned by network
    targets = torch.zeros(constants.BATCH_SIZE, device=device) # reward + maxarg Q(next_state, action) 

    for i, transition in enumerate(exp_batch):
        # calculate Q(state) values
        q_vals = network(transition.state.float()).to(device)
        #select value corresponding to action taken
        q_state_action = q_vals[0][transition.action] # q_vals has batch dimension
        inputs[i] = q_state_action
        # calc best q value for next state
        next_state_pred = network(transition.next_state.float()).detach().cpu().numpy().ravel()
        next_q_val = np.max(next_state_pred)

        if transition.isDead:
            targets[i] = transition.reward
        else:
            targets[i] = transition.reward + constants.GAMMA * next_q_val

    loss = F.smooth_l1_loss(inputs, targets)
    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    #for param in network.parameters():
      #  param.grad.data.clamp_(-1, 1)
    optimizer.step()

    
