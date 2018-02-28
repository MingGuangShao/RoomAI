#!/bin/python

import roomai.threeking
from roomai.threeking import ThreekingAction
from roomai.threeking import ThreekingPokerCard


class Player(roomai.common.AbstractPlayer):
    '''
    '''
    def take_action(self):
        '''
        define a policy to play the game
        return an action object
        '''
        #implement your code here
        #a = strategy(self.avaliable_actions.values()) 
        #return ThreeKingAction.lookup(a)

    def receive_info(self, info):
        '''
        '''
        self.public_state = info.public_state
        self.avaliable_actions = info.person_state.avaliable_actions

    def reset(self):
        '''
        '''
        pass
