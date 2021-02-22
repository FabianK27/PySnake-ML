import pygame
import constants
from pySnakeML import gameLoopML
import time
from models import randomNN
import matplotlib.pyplot as plt
import numpy as np
from models import deepQNetwork
import torch
from train import *


if __name__ == "__main__":
    print("ENTRY POINT")

    train()

    