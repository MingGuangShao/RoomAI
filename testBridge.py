#!/bin/python
import unittest
import roomai.bridge
import roomai
import roomai.common
from functools import cmp_to_key

class BridgeTester(unittest.TestCase):
    def testInit(self):
        env = roomai.bridge.BridgeEnv()
        env.init()

    def testForward(self):
        env = roomai.bridge.BridgeEnv()
        infos, public_state, person_states, private_state = env.init()
        xxx = 0
        self.assertEqual(len(infos),4)
        for i in range(4):
            self.assertEqual(len(person_states[i].hand_cards_dict.keys()), 52 / 4)

        self.assertNotEqual(len(person_states[public_state.turn].available_actions),0)
        self.assertEqual(len(person_states[public_state.turn].available_actions), 36)

    def testAction(self):
        action = roomai.bridge.BridgeAction.lookup("bidding_bid_A_Heart")
        self.assertEqual(action.stage, "bidding")
        self.assertEqual(action.bidding_option,"bid")
        self.assertEqual(action.bidding_contract_point, "A")
        self.assertEqual(action.bidding_contract_suit,"Heart")
        self.assertEqual(action.playing_card,None)
        xxx = 0
        print (xxx)


    def testAGame(self):
        env = roomai.bridge.BridgeEnv()
        allcards = list(roomai.bridge.AllBridgePokerCards.values())
        allcards.sort(key = cmp_to_key(roomai.common.PokerCard.compare))
        infos, public_state, person_states, private_state = env.init({"allcards":allcards, "start_turn":0})
        for i in range(4):
            print (i,person_states[i].hand_cards_dict, len(person_states[i].hand_cards_dict))
            self.assertEqual(len(person_states[i].hand_cards_dict),13)
        self.assertEqual(public_state.turn, 0)

        #### bidding stage
        action = roomai.bridge.BridgeAction.lookup("bidding_bid_A_Heart")
        infos, public_state, person_states, private_state = env.forward(action)
        action = roomai.bridge.BridgeAction.lookup("bidding_pass")
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)
        self.assertEqual(public_state.stage, "playing")
        self.assertEqual(public_state.turn,0)

        #### playing_stage
        count = 0
        while env.public_state.is_terminal == False:
            action  = list(env.person_states[env.public_state.turn].available_actions.values())[0]
            count  += 1
            env.forward(action)
        self.assertEqual(count,13 * 4)
        self.assertTrue(env.public_state.scores[0] == 0)
        self.assertTrue(env.public_state.scores[1] > 0)
        self.assertEqual(env.public_state.scores[1],350)


    def testAGame1(self):
        env = roomai.bridge.BridgeEnv()
        allcards = list(roomai.bridge.AllBridgePokerCards.values())
        allcards.sort(key = cmp_to_key(roomai.common.PokerCard.compare))
        infos, public_state, person_states, private_state = env.init({"allcards":allcards, "start_turn":0})
        for i in range(4):
            print (i,person_states[i].hand_cards_dict, len(person_states[i].hand_cards_dict))
            self.assertEqual(len(person_states[i].hand_cards_dict),13)
        self.assertEqual(public_state.turn, 0)

        #### bidding stage
        action = roomai.bridge.BridgeAction.lookup("bidding_bid_A_Heart")
        infos, public_state, person_states, private_state = env.forward(action)
        action = roomai.bridge.BridgeAction.lookup("bidding_double")
        infos, public_state, person_states, private_state = env.forward(action)
        action = roomai.bridge.BridgeAction.lookup("bidding_pass")
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)
        self.assertEqual(public_state.stage, "playing")
        self.assertEqual(public_state.turn,0)
        self.assertEqual(public_state.playing_magnification,2)

        #### playing_stage
        count = 0
        while env.public_state.is_terminal == False:
            action  = list(env.person_states[env.public_state.turn].available_actions.values())[0]
            count  += 1
            if count == 13 * 4:
                xx = 0
            env.forward(action)


        self.assertEqual(count,13 * 4)
        self.assertTrue(env.public_state.scores[0] == 0)
        self.assertTrue(env.public_state.scores[1] > 0)
        self.assertEqual(env.public_state.scores[1],100 + 200 * 2 + (7-3) * 300)


if __name__ == "__main__":
    import time
    start = time.time()
    for iter in range(1000):
        env = roomai.bridge.BridgeEnv()
        allcards = list(roomai.bridge.AllBridgePokerCards.values())
        allcards.sort(key = cmp_to_key(roomai.common.PokerCard.compare))
        infos, public_state, person_states, private_state = env.init({"allcards":allcards, "start_turn":0})

        #### bidding stage
        action = roomai.bridge.BridgeAction.lookup("bidding_bid_A_Heart")
        infos, public_state, person_states, private_state = env.forward(action)
        action = roomai.bridge.BridgeAction.lookup("bidding_double")
        infos, public_state, person_states, private_state = env.forward(action)
        action = roomai.bridge.BridgeAction.lookup("bidding_pass")
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)

        #### playing_stage
        count = 0
        while env.public_state.is_terminal == False:
            action  = list(env.person_states[env.public_state.turn].available_actions.values())[0]
            env.forward(action)

    end = time.time()
    print (end-start)
