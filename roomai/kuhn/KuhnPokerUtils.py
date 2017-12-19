#!/bin/python
import roomai.common
import copy


class KuhnPokerChanceAction(roomai.common.AbstractAction):
    '''
    The KuhnPoker action used by the chance player. Example of usages:\n
    >> import roomai.kuhn\n
    >> action = roomai.kuhn.KuhnPokerChanceAction("0,1")\n
    >> action.key \n
    "0,1"
    >> action.number_for_player0\n
    0\n
    >> action.number_for_player1\n
    1
    '''

    def __init__(self, key):
        super(KuhnPokerChanceAction, self).__init__(key)
        self.__key__ = key
        n1_n2        = key.split(",")
        self.__number_for_player0 = int(n1_n2[0])
        self.__number_for_player1 = int(n1_n2[1])

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the KuhnPokerChance action, for example, \"0,1\"")

    def __get_number_for_player0__(self):
        return self.__number_for_player0
    number_for_player0 = property(__get_number_for_player0__, doc = "The number of the players[0]")

    def __get_number_for_player1__(self):
        return self.__number_for_player1
    number_for_player1 = property(__get_number_for_player1__, doc = "The number of the players[1]")

    @classmethod
    def lookup(cls, key):
        return AllKuhnChanceActions[key]

    def __deepcopy__(self, memodict={}, newinstance=None):
        return KuhnPokerChanceAction.lookup(self.key)

AllKuhnChanceActions = {"0,1": KuhnPokerChanceAction("0,1"), \
                        "1,0": KuhnPokerChanceAction("1,0"),\
                        "0,2": KuhnPokerChanceAction("0,2"), \
                        "2,0": KuhnPokerChanceAction("2,0"), \
                        "1,2": KuhnPokerChanceAction("1,2"), \
                        "2,1": KuhnPokerChanceAction("2,1"),}

class KuhnPokerAction(roomai.common.AbstractAction):
    '''
    The KuhnPoker action used by the normal players. There are only two actions: bet and check. Examples of usages: \n
    >> import roomai.kuhn\n
    >> action = roomai.kuhn.KuhnPokerAction.lookup("bet")\n
    >> action.key\n
    "bet"\n
    >> action = roomai.kuhn.KuhnPokerAction.lookup("check")\n
    >> action.key\n
    "check"\n
    '''
    def __init__(self, key):
        super(KuhnPokerAction,self).__init__(key)
        self.__key__ = key

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the KuhnPoker action, \"bet\" or \"check\".")

    @classmethod
    def lookup(cls, key):
        return AllKuhnActions[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        return KuhnPokerAction.lookup(self.key)

AllKuhnActions = {"bet":KuhnPokerAction("bet"),"check":KuhnPokerAction("check")}

class KuhnPokerPublicState(roomai.common.AbstractPublicState):
    '''
    The public state class of the KuhnPoker game
    '''
    def __init__(self):
        super(KuhnPokerPublicState,self).__init__()
        self.__first__                      = 0
        self.__epoch__                      = 0
        self.__action_history__                = []

    def __get_first__(self):    return self.__first__
    first = property(__get_first__, doc="players[first] is expected to take an action")

    def __get_epoch(self):  return self.__epoch__
    epoch = property(__get_epoch)


    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = KuhnPokerPublicState()
        newinstance = super(KuhnPokerPublicState, self).__deepcopy__(newinstance=newinstance)
        newinstance.__first__ = self.first
        newinstance.__epoch__ = self.epoch
        return newinstance

class KuhnPokerPrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state class of KuhnPoker
    '''

    def __deepcopy__(self, memodict={}, newinstance = None):
        return AKuhnPokerPrivateState
AKuhnPokerPrivateState = KuhnPokerPrivateState()

class KuhnPokerPersonState(roomai.common.AbstractPersonState):
    '''
    The person state of KuhnPoker
    '''
    def __init__(self):
        super(KuhnPokerPersonState,self).__init__()
        self.__number__ = 0

    def __get_number__(self):   return self.__number__
    number = property(__get_number__,doc="The number given by the game enviroment. The value of this number is in {0,1,2}. The larger number, the higher win rate")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
           newinstance = KuhnPokerPersonState()
        return super(KuhnPokerPersonState, self).__deepcopy__(newinstance)