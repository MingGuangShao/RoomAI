#!/bin/python
import random

from algorithms import CRMAlgorithm
from algorithms import CRMPlayer
from roomai.kuhn import Example_KuhnPokerAlwaysBetPlayer
from roomai.kuhn import KuhnPokerEnv
from roomai.kuhn import KuhnPokerRandomPlayer


class KuhnPokerCRMPlayer(CRMPlayer):
    """
    """
    def __init__(self):
        """

        """
        self.state                     = []
        self.regrets                   = dict()
        self.strategies                = dict()

    def update_strategies(self, state, actions, targets):
        """

        Args:
            state:
            actions:
            targets:
        """
        for i in range(len(actions)):
            state_action = "%s_%s"%(state, actions[i].key)
            self.strategies[state_action] = targets[i]

    def get_strategies(self, state, actions):
        """

        Args:
            state:
            actions:

        Returns:

        """
        probs = [1.0 for i in range(len(actions))]
        for  i in range(len(actions)):
            state_action = "%s_%s" % (state, actions[i].key)
            if state_action not in self.strategies:
                probs[i] = 1.0 / len(actions)
            else:
                probs[i] = self.strategies[state_action]
        return probs

    def update_regrets(self, state, actions, targets):
        """

        Args:
            state:
            actions:
            targets:
        """
        for i in range(len(actions)):
            state_action = "%s_%s"%(state, actions[i].key)
            self.regrets[state_action] = targets[i]

    def get_regrets(self, state, actions):
        """

        Args:
            state:
            actions:

        Returns:

        """
        regrets = [0 for i in range(len(actions))]
        for i in range(len(actions)):
            state_action = "%s_%s" % (state, actions[i].key)
            if state_action not in self.regrets:
                regrets[i] = 0
            else:
                regrets[i] = self.regrets[state_action]
        return regrets

    def gen_state(self,info):
        """

        Args:
            info:

        Returns:

        """
        card = info.person_state.card
        history = info.public_state.action_list
        return "%d_%s" % (card, "".join(history))

    def receive_info(self, info):
        """

        Args:
            info:
        """
        self.state             = self.gen_state(info)
        self.available_actions = info.person_state.available_actions.values()

    def take_action(self):
        """

        Returns:

        """
        probs = self.get_strategies(self.state, self.available_actions)
        sum1  = sum(probs)
        for i in range(len(self.available_actions)):
            probs[i] /= sum1

        r    = random.random()
        sum1 = 0
        for i in range(len(probs)):
            sum1 += probs[i]
            if sum1 > r:
                return self.available_actions[i]

        return self.available_actions[len(self.available_actions)-1]


    def reset(self):
        """

        """
        pass

if __name__ == "__main__":
    env     = KuhnPokerEnv()
    player  = KuhnPokerCRMPlayer()
    algo    = CRMAlgorithm()
    for i in range(10000):
        algo.dfs(env = env, player=player, p0 = 1, p1 = 1, deep = 0)

    print player.regrets
    print player.strategies
    player.is_train = False

    player_random = KuhnPokerRandomPlayer()
    sum_scores = [0.0,0.0]
    num        = 0
    for i in range(10000):
        scores = KuhnPokerEnv.compete(env,[player, player_random])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num           += 1
    for i in range(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores


    player_alwaysbet = Example_KuhnPokerAlwaysBetPlayer()
    sum_scores = [0.0,0.0]
    num        = 0
    for i in range(10000):
        scores = KuhnPokerEnv.compete(env,[player, player_alwaysbet])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num           += 1
    for i in range(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores

    sum_scores = [0.0, 0.0]
    num = 0
    for i in range(10000):
        scores = KuhnPokerEnv.compete(env, [player_random, player_alwaysbet])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num += 1
    for i in range(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores
