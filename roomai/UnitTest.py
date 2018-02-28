import sys
sys.path.append("..")

from roomai.threeking import *;
import random

if __name__ == "__main__":

    env = ThreeKingEnv()
    params = dict()
    env.init(params)
    print "instance enc: ", env
    #print all method and f in env
    for i in dir(env):
        print i

    print "params in env: ", env.__params__.keys()
    print "players info in env: ", env.__params__["players_info"]
    print "num players in env: ", env.__params__["num_players"]
    print "lord id in public_state: ", env.public_state.__lord_id__
    print "num of hand cards in public_state: ",env.public_state.__num_hand_cards__

