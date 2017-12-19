#!/bin/python
import roomai.common

AllSevenKingPatterns = dict()
###
###numCards
AllSevenKingPatterns["p_0"] = ("p_0", 0) ## check
AllSevenKingPatterns["p_1"] = ("p_1", 1)
AllSevenKingPatterns["p_2"] = ("p_2", 2)
AllSevenKingPatterns["p_3"] = ("p_3", 3)
AllSevenKingPatterns["p_4"] = ("p_4", 4)


point_str_to_rank  = {'7':14, 'R':13, 'r':12, '5':11,  '2':10,  '3':9,  'A':8,  'K':7,\
                      'Q':6,  'J':5,   'T':4,   '9':3,   '8':2,   '6':1,   '4':0}
point_rank_to_str  = {14:'7', 13:'R', 12:'r',  11:'5', 10:'2',  9:'3',  8:'A',   7:'K',\
                       6:'Q',  5:'J',   4:'T',   3:'9',   2:'8',   1:'6',  0:'4'}
suit_str_to_rank   = {'Spade':3, 'Heart':2, 'Diamond':1, 'Club':0,  'ForKing':4}
suit_rank_to_str   = {3:'Spade', 2: 'Heart', 1: 'Diamond', 0:'Club', 4:'ForKing'}

#point_str_to_rank  = {'2':0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12, 'r':13,'R':14}
#point_rank_to_str  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A', 13:'r',14:'R'}
#suit_str_to_rank   = {'Spade': 3, 'Heart': 2, 'Club': 1, 'Diamond':0,'ForKing':4}
#suit_rank_to_str   = {3:'Spade', 2:'Heart', 1:'Club', 0:'Diamond',4:'ForKing'}

class SevenKingPokerCard(roomai.common.PokerCard):
    '''
    A poker card used in SevenKing game\n
    The suit ranks in the common poker card(roomai.common.PokerCard) and the SevenKing poker card(roomai.SevenKing.SevenKingPokerCard) are different: \n
    The common poker card: 'Spade': 'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3,  'ForKing':4\n
    The SevenKing poker card:'Spade': 3, 'Heart': 2, 'Club': 1, 'Diamond':0, 'ForKing':4\n
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
        return AllSevenKingPokerCards[self.key]

    @classmethod
    def lookup(cls, key):
        return AllSevenKingPokerCards[key]


AllSevenKingPokerCards = dict()
for point_str in roomai.common.common.point_str_to_rank:
    if point_str != 'r' and point_str != "R":
        for suit_str in roomai.common.common.suit_str_to_rank:
            if suit_str != "ForKing":
                AllSevenKingPokerCards["%s_%s" % (point_str, suit_str)] = SevenKingPokerCard("%s_%s" % (point_str, suit_str))
AllSevenKingPokerCards["r_ForKing"] = SevenKingPokerCard("r_ForKing")
AllSevenKingPokerCards["R_ForKing"] = SevenKingPokerCard("R_ForKing")
