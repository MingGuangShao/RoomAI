#!/bin/python
#coding=utf8

import roomai
import roomai.common
logger = roomai.get_logger()



######################################################################### Basic Concepts #####################################################
class AbstractPublicState(object):
    '''
    The abstract class of the public state. The information in the public state is public to every player
    '''
    def __init__(self):
        self.__turn__            = None
        self.__action_history__  = []

        self.__is_terminal__     = False
        self.__scores__          = None

    def __get_turn__(self): return self.__turn__
    turn = property(__get_turn__, doc = "The players[turn] is expected to take an action.")

    def __get_action_history__(self):   return tuple(self.__action_history__)
    action_history = property(__get_action_history__, doc = "The action_history so far. For example, action_history = [(0, roomai.kuhn.KuhnAction.lookup(\"check\"),(1,roomai.kuhn.KuhnAction.lookup(\"bet\")]")

    ''' 
    def __get_previous_id__(self):  return self.__previous_id__
    previous_id = property(__get_previous_id__,doc = "The players[previous_id] took an action in the previous epoch. In the first epoch, previous_id is None")

    def __get_previous_action(self):    return self.__previous_action__
    previous_action = property(__get_previous_action, doc = "The players[previous_id] took previous_action in the previous epoch. In the first epoch, previous_action is None")
    '''

    def __get_is_terminal__(self):   return  self.__is_terminal__
    is_terminal = property(__get_is_terminal__,doc = "is_terminal = True means the game is over. At this time, scores is not None, scores = [float0,float1,...] for player0, player1,... For example, scores = [-1,2,-1].\n"
                                                     "is_terminal = False, the scores is None.")

    def __get_scores__(self):   return self.__scores__
    scores = property(__get_scores__, doc = "is_terminal = True means the game is over. At this time, scores is not None, scores = [float0,float1,...] for player0, player1,... For example, scores = [-1,3,-2].\n"
                                            "is_terminal = False, the scores is None.")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = AbstractPublicState()

        newinstance.__turn__           = self.__turn__
        newinstance.__action_history__ = list(self.__action_history__)
        '''
        newinstance.__previous_id__= self.__previous_id__
        if self.__previous_action__ is not None:
            newinstance.__previous_action__ = self.previous_action.__deepcopy__()
        else:
            newinstance.__previous_action__ = None
        '''


        newinstance.__is_terminal__ = self.is_terminal
        if self.scores is None:
            newinstance.__scores__ = None
        else:
            newinstance.__scores__ = [score for score in self.scores]
        return newinstance

class AbstractPrivateState(object):
    '''
    The Abstract class of the private state. The information in the private state is hidden from every player
    '''
    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is  None:
            return AbstractPrivateState()
        else:
            return newinstance


class AbstractPersonState(object):
    '''
    The abstract class of the person state. The information in the person state is public to the corresponding player and hidden from other players
    '''
    def __init__(self):
        self.__id__ = 0
        self.__available_actions__ = dict()

    def __get_id__(self):   return self.__id__
    id = property(__get_id__, doc="The id of player w.r.t this person state")

    def __get_available_actions__(self):  return FrozenDict(self.__available_actions__)
    available_actions = property(__get_available_actions__, doc="All valid actions for the player expected to take an action. The person state w.r.t no-current player contains empty available_actions")


    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is  None:
            newinstance = AbstractPersonState()
        newinstance.__id__ = self.__id__
        newinstance.__available_actions__ = dict(self.available_actions)
        return newinstance

class Info(object):
    '''
    The class of information sent by env to a player. The Info class contains the public state and the corresponding person state 
    '''
    def __init__(self):
        self.__public_state__       = AbstractPublicState()
        self.__person_state__       = AbstractPersonState()


    def __get_public_state__(self):
        return self.__public_state__
    public_state = property(__get_public_state__, doc="The public state in the information")

    def __get_person_state__(self):
        return self.__person_state__
    person_state = property(__get_person_state__, doc="The person state in the information")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = Info()
        newinstance.__public_state__  = self.__public_state.__deepcopy__()
        newinstance.__personc_state__ = self.__person_state.__deepcopy__()
        return newinstance

class AbstractAction(object):
    '''
    The abstract class of an action. 
    '''
    def __init__(self, key):
        self.__key__ = key

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the action. Every action in RoomAI has a key as its identification."
                                    " We strongly recommend you to use the lookup function to get an action with the specified key")

    @classmethod
    def lookup(self, key):
        '''
        Get an action with the specified key. 
        We strongly recommend you to use the lookup function to get an action with the specified key, rather than use the constructor function.
        
        :param key: the specified key
        :return:  the action with the specified key
        '''
        raise NotImplementedError("Not implemented")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = AbstractAction()
        newinstance.__key = self.__key
        return newinstance




class AbstractPlayer(object):
    '''
    The abstract class of a player
    '''
    def receive_info(self, info):
        '''
        Receive information 
        
        :param:info: the information produced by a game environments
        :raises: NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        """
        :returns: The action produced by this player
        """
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        '''
        reset for a new game 
        '''
        raise NotImplementedError("The reset function hasn't been implemented")


class RandomPlayer(AbstractPlayer):
    '''
    The RandomPlayer is a player, who randomly takes an action.
    The RandomPlayer is as a common baseline
    '''
    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions

    def take_action(self):
        import random
        idx = int(random.random() * len(self.available_actions))
        return list(self.available_actions.values())[idx]

    def reset(self):
        pass



class AbstractEnv(object):
    '''
    The abstract class of game environment
    '''

    def __init__(self):
        self.__params__ = dict()
        self.__public_state_history__  = []
        self.__person_states_history__ = []
        self.__private_state_history__ = []

        self.public_state  = AbstractPublicState()
        self.person_states = [AbstractPersonState()]
        self.private_state = AbstractPrivateState()



    def __gen_infos__(self):

        num_players = len(self.person_states)
        __infos__   = [Info() for i in range(num_players)]

        for i in range(num_players):
            __infos__[i].__person_state__ = self.person_states[i]#.__deepcopy__()
            __infos__[i].__public_state__ = self.public_state#.__deepcopy__()

        return tuple(__infos__)


    def __gen_history__(self):

        if "record_history" not in self.__params__ or self.__params__["record_history"] == False:
            return

        self.__public_state_history__.append(self.public_state.__deepcopy__())
        self.__private_state_history__.append(self.private_state.__deepcopy__())
        self.__person_states_history__.append([person_state.__deepcopy__() for person_state in self.person_states])

    def init(self, params =dict()):
        '''
        Initialize the game environment 
        
        :param params:  
        :return:  infos, public_state, person_states, private_state, other_chance_actions
        '''

        raise ("The init function hasn't been implemented")

    def forward(self, action):
        """
        The game environment steps with the action taken by the current player
        
        :param action, chance_action
        :returns:infos, public_state, person_states, private_state, other_chance_actions
        """
        raise NotImplementedError("The forward hasn't been implemented")


    def backward(self):
        '''
        The game goes back to the previous states

        :returns:infos, public_state, person_states, private_state
        :raise:Env has reached the initialization state and can't go back further.
        '''

        if "record_history" not in self.__params__ or self.__params__["record_history"] == False:
            raise ValueError("Env can't backward when params[\"record_history\"] = False. If you want to use this backward function, please env.init({\"record_history\":true,...})")

        if len(self.__public_state_history__) == 1:
            raise ValueError("Env has reached the initialization state and can't go back further. ")
        self.__public_state_history__.pop()
        self.__private_state_history__.pop()
        self.__person_states_history__.pop()

        p = len(self.__public_state_history__) - 1
        self.public_state  = self.__public_state_history__[p].__deepcopy__()
        self.private_state = self.__private_state_history__[p].__deepcopy__()
        self.person_states = [person_state.__deepcopy__() for person_state in self.__person_states_history__[p]]

        infos  = self.__gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = AbstractEnv()
        newinstance.__params__ = dict(self.__params__)
        newinstance.private_state = self.private_state.__deepcopy__()
        newinstance.public_state  = self.public_state.__deepcopy__()
        newinstance.person_states = [pe.__deepcopy__() for pe in self.person_states]

        newinstance.__private_state_history__ = [pr.__deepcopy__() for pr in self.__private_state_history__]
        newinstance.__public_state_history__  = [pu.__deepcopy__() for pu in self.__public_state_history__]
        newinstance.__person_states_history__ = []
        if len(self.person_states) > 0:
            for i in range(len(self.person_states)):
                newinstance.__person_states_history__.append([pe.__deepcopy__() for pe in self.__person_states_history__[i]])

        return newinstance


    ### provide some util functions
    @classmethod
    def compete(cls, env, players):
        '''
        Use the game environment to hold a compete for the players
        
        :param env: The game environment
        :param players: The players
        :return: scores for the players
        '''
        raise NotImplementedError("The round function hasn't been implemented")

    @classmethod
    def is_action_valid(cls, action, public_state, person_state):
        '''
        Is the action valid given the public state and the person state
        
        :param action: 
        :param public_state: 
        :param person_state: 
        :return: A boolean variable indicating whether is the action valid 
        '''
        raise  NotImplementedError("The is_action_valid function hasn't been implemented")

    @classmethod
    def available_actions(self, public_state, person_state):
        '''
        Generate all valid actions given the public state and the person state
        
        :param public_state: 
        :param person_state: 
        :return: A dict(action_key, action) contains all valid actions
        '''
        raise NotImplementedError("The available_actions function hasn't been implemented")

############################################################### Some Utils ############################################################################

point_str_to_rank  = {'2':0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12, 'r':13, 'R':14}
point_rank_to_str  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A', 13: 'r', 14: 'R'}
suit_str_to_rank   = {'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3,  'ForKing':4}
suit_rank_to_str   = {0:'Spade', 1: 'Heart', 2: 'Diamond', 3:'Club', 4:'ForKing'}
class PokerCard(object):
    '''
    A Poker Card. 
    A Poker Card has a point (2,3,4,....,K,A,r,R) and a suit (Spade, Heart, Diamond, Club, ForKing). 
    Different points have different ranks, for example the point 2 's rank is 0, and the point A 's rank is 12. 
    Different suits have different ranks too.
    The "ForKing" suit is a placeholder used for the card with the point "r" or "R"
    A Poker Card has a key (point_suit). We strongly recommend you to get a poker card by using the class function lookup with the key.
    Examples of the class usages:
    >> import roomai.common
    >> card = roomai.common.PokerCard.lookup("2_Spade")
    >> card.point 
    2
    >> card.suit
    Spade
    >> card.point_rank
    0
    >> card.suit_rank
    0
    >> card.key
    "2_Spade"
    '''
    def __init__(self, point, suit = None):
        point1 = 0
        suit1  = 0
        if suit is None:
            kv = point.split("_")
            point1 = point_str_to_rank[kv[0]]
            suit1  = suit_str_to_rank[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_rank[point]
            suit1  = suit
            if isinstance(suit, str):
                suit1 = suit_str_to_rank[suit]

        self.__point__  = point_rank_to_str[point1]
        self.__suit__   = suit_rank_to_str[suit1]
        self.__point_rank__ = point1
        self.__suit_rank__  = suit1
        self.__key__        = "%s_%s" % (self.__point__, self.__suit__)


    def __get_point_str__(self):
        return self.__point__
    point = property(__get_point_str__, doc="The point of the poker card")

    def __get_suit_str__(self):
        return self.__suit__
    suit = property(__get_suit_str__, doc="The suit of the poker card")

    def __get_point_rank__(self):
        return self.__point_rank__
    point_rank = property(__get_point_rank__, doc="The point rank of the poker card")

    def __get_suit_rank__(self):
        return self.__suit_rank__
    suit_rank = property(__get_suit_rank__, doc="The suit rank of the poker card")

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the poker card")


    @classmethod
    def lookup(cls, key):
        '''
        lookup a PokerCard with the specified key
        
        :param key: The specified key
        :return: The PokerCard with the specified key
        '''
        return AllPokerCards[key]

    @classmethod
    def compare(cls, pokercard1, pokercard2):
        '''
        Compare two poker cards with their point ranks and suit ranks.
        The poker card with the higher point rank has the higher rank.
        With the same point rank, the poker card with the higher suit rank has the higher rank.
        
        :param pokercard1: 
        :param pokercard2: 
        :return: A number, which is >0 when the poker card1 has the higher rank than the poker card2, =0 when their share the same rank, <0 when the poker card1 has the lower rank than the poker card2
        
        '''
        pr1 = pokercard1.point_rank
        pr2 = pokercard2.point_rank

        if pr1 != pr2:
            return pr1 - pr2
        else:
            return pokercard1.suit_rank - pokercard2.suit_rank


    def __deepcopy__(self,  memodict={}, newinstance = None):
        return   AllPokerCards[self.key]


AllPokerCards = dict()
AllPokerCards_Without_King = dict()
for point in point_str_to_rank:
    if point != 'r' and point != "R":
        for suit in suit_str_to_rank:
            if suit != "ForKing":
                AllPokerCards["%s_%s" % (point, suit)] = PokerCard("%s_%s" % (point, suit))
                AllPokerCards_Without_King["%s_%s" % (point, suit)] = PokerCard("%s_%s" % (point, suit))
AllPokerCards["r_ForKing"] = (PokerCard("r_ForKing"))
AllPokerCards["R_ForKing"] = (PokerCard("R_ForKing"))


def version():
    '''

    :return: The version of RoomAI 
    '''
    version = "0.1.1"
    print("roomai-%s" % version)
    return ("roomai-%s" % version)


class FrozenDict(dict):
    def __setitem__(self, key, value):
        raise NotImplementedError("The FrozenDict doesn't support the __setitem__ function")

