# NN test simulation, returns random inputs
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

class randomNN:
    def __init__(self, numPos):
        self.numPos = numPos
    def returnAction(self):
        return random.randrange(0, self.numPos)

class deepQNetwork(nn.Module):
    def __init__(self, num_actions, input_channles):
        super(deepQNetwork, self).__init__()
        self.num_actions = num_actions

        self.conv1 = nn.Conv2d(input_channles, 16, kernel_size=5, stride=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        # calculate linear outputs
        self.linearLayer = nn.Linear(x.size(2)*x.size(3)*32, self.num_actions)

        return self.linearLayer(x.view(x.size(0), -1))

    def get_action(self, state):
        with torch.no_grad():
            q_vals = self.forward(state.float())
        # for now always return greedy action, later add epsilon random exploring
        return torch.argmax(q_vals).item()


