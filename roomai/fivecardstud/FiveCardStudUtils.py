#!/bin/python
import roomai.common

                                                    #0     1           2       3           4                                    5
                                                    #name, isStraight, isSameSuit, isNumRelated, [SizeOfPair1, SizeOfPair2,..](desc), rank
FiveCardStudAllCardsPattern = dict()
FiveCardStudAllCardsPattern["Straight_SameSuit"] = ["Straight_SameSuit", True, True, False, [], 100]
FiveCardStudAllCardsPattern["4_1"]               = ["4_1", False, False, True, [4, 1], 98]
FiveCardStudAllCardsPattern["3_2"]               = ["3_2", False, False, True, [3, 2], 97]
FiveCardStudAllCardsPattern["SameSuit"]          = ["SameSuit", False, True, False, [], 96]
FiveCardStudAllCardsPattern["Straight_DiffSuit"] = ["Straight_DiffSuit", True, False, False, [], 95]
FiveCardStudAllCardsPattern["3_1_1"]             = ["3_1_1", False, False, True, [3, 1, 1], 94]
FiveCardStudAllCardsPattern["2_2_1"]             = ["2_2_1", False, False, True, [2, 2, 1], 93]
FiveCardStudAllCardsPattern["2_1_1_1"]           = ["2_1_1_1", False, False, True, [2, 1, 1, 1], 92]
FiveCardStudAllCardsPattern["1_1_1_1_1"]         = ["1_1_1_1_1", False, False, True, [1, 1, 1, 1, 1], 91]

point_str_to_rank  = {'2':0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
point_rank_to_str  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
suit_str_to_rank   = {'Spade': 3, 'Heart': 2, 'Club': 1, 'Diamond':0}
suit_rank_to_str   = {3:'Spade', 2:'Heart', 1:'Club', 0:'Diamond'}

class FiveCardStudPokerCard(roomai.common.PokerCard):
    '''
    A poker card used in FiveCardStud game
    The difference in the common poker card(roomai.common.PokerCard) and the fivecardstud poker card(roomai.fivecardstud.FiveCardStudPokerCard) is: they have different suit rank
    The common poker card: 'Spade': 'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3,  'ForKing':4
    The FiveCardStud poker card:'Spade': 3, 'Heart': 2, 'Club': 1, 'Diamond':0
    Besides, there aren't r and R in FiveCardStud
    '''

    def __init__(self, point, suit = None):
        real_point_int = 0
        real_suit_int  = 0
        if suit is None:
            kv = point.split("_")
            real_point_int = point_str_to_rank[kv[0]]
            real_suit_int  = suit_str_to_rank[kv[1]]
        else:
            real_point_int = point
            if isinstance(point, str):
                real_point_int = point_str_to_rank[point]
            real_suit_int  = suit
            if isinstance(suit, str):
                real_suit_int = suit_str_to_rank[suit]

        self.__point__      = point_rank_to_str[real_point_int]
        self.__suit__       = suit_rank_to_str[real_suit_int]
        self.__point_rank__ = real_point_int
        self.__suit_rank__  = real_suit_int
        self.__key__        = "%s_%s" % (self.__point__, self.__suit__)


    def __deepcopy__(self, memodict={}, newinstance = None):
        return FiveCardStudAllPokerCards[self.key]

    @classmethod
    def lookup(cls, key):
        return FiveCardStudAllPokerCards[key]


FiveCardStudAllPokerCards = dict()
for point_str in roomai.common.common.point_str_to_rank:
    if point_str != 'r' and point_str != "R":
        for suit_str in roomai.common.common.suit_str_to_rank:
            if suit_str != "ForKing":
                FiveCardStudAllPokerCards["%s_%s"%(point_str,suit_str)] = FiveCardStudPokerCard("%s_%s"%(point_str,suit_str))
#FiveCardStudAllPokerCards["r_ForKing"] = (FiveCardStudPokerCard("r_ForKing"))
#FiveCardStudAllPokerCards["R_ForKing"] = (FiveCardStudPokerCard("R_ForKing"))
