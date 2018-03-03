#!/bin/python

import roomai.threeking
from roomai.threeking import ThreeKingAction
from roomai.threeking import ThreeKingPokerCard


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
        # For Unit Test
        a = "Sha,SHA_7_spade_0,MaChao" 
        return ThreeKingAction.lookup(a)

    def receive_info(self, info):
        '''
        '''
        #question? why self.public_state
        self.public_state = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        '''
        '''
        pass
