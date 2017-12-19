#!/bin/python
import random
import math
import copy
import roomai.kuhn.KuhnPokerUtils
import roomai.common
logger = roomai.get_logger()

class KuhnPokerEnv(roomai.common.AbstractEnv):
    '''
    The KuhnPoker game environment
    '''


    #@override
    def init(self, params=dict()):
        '''
        Initialize the KuhnPoker game environment
        
        :param params: the initialization params
        :return: infos, public_state, person_states, private_state 
        '''
        self.__params__ = dict()

        if "record_history" in params:
            self.__params__["record_history"] = params["record_history"]
        else:
            self.__params__["record_history"] = False

        if "start_turn" in params:
            self.__params__["start_turn"] = params["start_turn"]
        else:
            self.__params__["start_turn"] = int(random.random() * 2)

        self.__params__["num_players"] = 3

        if "num_players" in params:
            logger.warning("KuhnPoker is a game of two players and the number of players always be 3 (2 normal players, and 1 chance player). Ingores the \"num_players\" option")


        self.all_available_action = dict()
        self.all_available_action[roomai.kuhn.KuhnPokerUtils.KuhnPokerAction("check").key] = roomai.kuhn.KuhnPokerAction.lookup("check")
        self.all_available_action[roomai.kuhn.KuhnPokerUtils.KuhnPokerAction("bet").key]   = roomai.kuhn.KuhnPokerAction.lookup("bet")

        self.private_state = roomai.kuhn.KuhnPokerUtils.KuhnPokerPrivateState()
        self.public_state  = roomai.kuhn.KuhnPokerUtils.KuhnPokerPublicState()
        self.person_states = [roomai.kuhn.KuhnPokerUtils.KuhnPokerPersonState() for i in range(3)]


        self.public_state.__turn__             = 2
        self.public_state.__first__            = self.public_state.turn
        self.public_state.__epoch__            = 0
        self.public_state.__action_history__   = []
        self.public_state.__is_terminal__      = False
        self.public_state.__scores__           = None
        self.person_states[0].__id__          = 0
        self.person_states[0].__number__      = -1
        self.person_states[1].__id__          = 1
        self.person_states[1].__number__      = -1
        self.person_states[2].__id__          = 3
        self.person_states[2].__number__      = -1

        self.person_states[self.public_state.turn].__available_actions__ = roomai.kuhn.KuhnPokerUtils.AllKuhnChanceActions

        self.__gen_history__()
        infos = self.__gen_infos__()

        
        return  infos, self.public_state, self.person_states, self.private_state

    #@override
    def forward(self, action):
        """
        The KuhnPoker game environment steps with the action taken by the current player

        :param action
        :returns:infos, public_state, person_states, private_state
        """

        ####### forward with the chance action ##########
        if isinstance(action, roomai.kuhn.KuhnPokerChanceAction) == True:
            self.public_state.__action_history__.append((2,action))
            self.person_states[0].__number__ = action.number_for_player0
            self.person_states[1].__number__ = action.number_for_player1
            self.person_states[self.public_state.turn].__available_actions__ = dict()
            self.public_state.__turn__ = self.__params__["start_turn"]
            self.person_states[self.public_state.turn].__available_actions__ = self.available_actions(self.public_state, self.person_states[self.public_state.turn])
            self.__gen_history__()
            return self.__gen_infos__(), self.public_state, self.person_states, self.private_state



        self.person_states[self.public_state.turn].__available_actions__ = dict()
        self.public_state.__action_history__.append((self.public_state.turn,action))
        self.public_state.__epoch__                                     += 1
        self.public_state.__turn__                                       = (self.public_state.turn+1)%2


        if self.public_state.epoch == 1:
            self.public_state.__is_terminal__ = False
            self.public_state.__scores__      = []
            self.person_states[self.public_state.turn].__available_actions__ = self.all_available_action

            self.__gen_history__()
            infos = self.__gen_infos__()
            return infos, self.public_state, self.person_states, self.private_state

        elif self.public_state.epoch == 2:
            scores = self.__evalute_two_round__()
            if scores is not None:
                self.public_state.__is_terminal__ = True
                self.public_state.__scores__      = scores

                self.__gen_history__()
                infos = self.__gen_infos__()
                return infos,self.public_state, self.person_states, self.private_state
            else:
                self.public_state.__is_terminal__ = False
                self.public_state.__scores__      = []
                self.person_states[self.public_state.turn].__available_actions__ = self.all_available_action

                self.__gen_history__()
                infos                         = self.__gen_infos__()
                return infos,self.public_state, self.person_states, self.private_state

        elif self.public_state.epoch == 3:
            self.public_state.__is_terminal__ = True
            self.public_state.__scores__     = self.__evalute_three_round__()

            self.__gen_history__()
            infos                         = self.__gen_infos__()
            return infos,self.public_state, self.person_states, self.private_state

        else:
            raise Exception("KuhnPoker has 3 turns at most")


    #@Overide
    @classmethod
    def compete(cls, env, players):
        '''
        Use the game environment to hold a compete for the players

        :param env: The game environment
        :param players: The players
        :return: scores for the players
        '''

        if len(players) != 2:
            raise  ValueError("The number of the players in Kuhn is two")

        new_players = players + [roomai.kuhn.KuhnPokerChancePlayer()]

        infos, public_state, person_state, private_state = env.init()
        for i in range(len(new_players)):
            new_players[i].receive_info(infos[i])

        while public_state.is_terminal == False:
            turn = infos[-1].public_state.turn
            action = new_players[turn].take_action()
            infos,public_state, person_state, private_state = env.forward(action)
            for i in range(len(new_players)):
                new_players[i].receive_info(infos[i])

        return public_state.scores

    @classmethod
    def available_actions(self, public_state, person_state):
        if len(public_state.action_history) == 0:
            return roomai.kuhn.KuhnPokerUtils.AllKuhnChanceActions
        else:
            return roomai.kuhn.KuhnPokerUtils.AllKuhnActions

    def __higher_number_player__(self):
        if self.person_states[0].number > self.person_states[1].number:
            return 0
        else:
            return 1

    def __evalute_two_round__(self):
        win    = self.__higher_number_player__()
        first  = self.public_state.first
        scores = [0, 0];
        actions = [id_action[1] for id_action in self.public_state.action_history]

        if actions[0] == "check" and \
           actions[1] == "bet":
            return None
        
        if actions[0] == actions[1] and \
           actions[0] == "check":
            scores[win]   = 1;
            scores[1-win] = -1
            return scores;

        if actions[0] == "bet" and \
           actions[1] == "check":
            scores[first]   = 1;
            scores[1-first] = -1
            return scores;

        if actions[0] == actions[1] and \
           actions[0] == "bet":
            scores[win]   = 2
            scores[1-win] = -2
            return scores;


    def __evalute_three_round__(self):
        first   = self.public_state.first 
        win     = self.__higher_number_player__()
        scores  = [0, 0]

        if self.public_state.action_history[2][1].key == "check":
            scores[1 - first] = 1;
            scores[first]     = -1
        else:
            scores[win]   = 2;
            scores[1-win] = -2
        return scores;
       
