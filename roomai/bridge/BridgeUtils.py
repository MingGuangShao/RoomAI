#!/bin/python
import roomai.common
from functools import cmp_to_key


class Direction:
    north = 0
    east  = 1
    south = 2
    west  = 3

point_str_to_rank  = {'A':12, 'K':11, 'Q':10, 'J':9, '10':8, '9':7, '8':6, '7':5, '6':4, '5':3, '4':2, '3':1, '2':0}
point_rank_to_str  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: '10', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
suit_str_to_rank   = {'Spade':3, 'Heart':2, 'Diamond':1, 'Club':0}
suit_rank_to_str   = {3: 'Spade', 2: 'Heart', 1: 'Diamond', 0: 'Club'}

class BridgePokerCard(roomai.common.PokerCard):
    '''
     A poker card used in Bridge\n
     The suit ranks in the common poker card(roomai.common.PokerCard) and the Bridge poker card(roomai.bridge.BridgePokerCard) are different: \n
     The common poker card: 'Spade': 0, 'Heart':1, 'Diamond':2, 'Club':3
     The Bridge poker card:'Spade': 0, 'Heart': 1, 'Diamond': 2, 'Club':3
     '''

    def __init__(self, point, suit=None):
        real_point_int = 0
        real_suit_int = 0
        if suit is None:
            kv = point.split("_")
            real_point_int = point_str_to_rank[kv[0]]
            real_suit_int = suit_str_to_rank[kv[1]]
        else:
            real_point_int = point
            if isinstance(point, str):
                real_point_int = point_str_to_rank[point]
            real_suit_int = suit
            if isinstance(suit, str):
                real_suit_int = suit_str_to_rank[suit]

        self.__point__      = point_rank_to_str[real_point_int]
        self.__suit__       = suit_rank_to_str[real_suit_int]
        self.__point_rank__ = real_point_int
        self.__suit_rank__  = real_suit_int
        self.__key__        = "%s_%s" % (self.__point__, self.__suit__)

    def __deepcopy__(self, memodict={}, newinstance=None):
        return AllBridgePokerCards[self.key]

    @classmethod
    def lookup(cls, key):
        return AllBridgePokerCards[key]

AllBridgePokerCards = dict()
for point_str in point_str_to_rank:
    for suit_str in suit_str_to_rank:
            AllBridgePokerCards["%s_%s" % (point_str, suit_str)] = BridgePokerCard("%s_%s" % (point_str, suit_str))


contract_suit_to_rank       = {'NotTrump':4,'Spade':3, 'Heart':2, 'Diamond':1, 'Club':0}
contract_point_to_rank      = {'A':1, '7':7, '6':6, '5':5, '4':4, '3':3, '2':2}