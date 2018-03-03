import sys
sys.path.append("..")

from roomai.threeking import *;
from roomai.threeking.ThreeKingPlayers import *;
import random


if __name__ == "__main__":

    players = [Player() for i in range(8)]
    env = ThreeKingEnv()
    ThreeKingEnv.compete(env, players)



