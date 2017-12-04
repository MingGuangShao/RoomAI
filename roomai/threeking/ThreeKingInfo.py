#!/bin/python
import roomai.common
from roomai.threeking import ThreeKingPorkerCard

class ThreeKingPublicState(roomai.common.AbstractPublicState):
	def __init__(self):
		super(ThreeKingPublicState,self).__init__()
		self.__stage__			        = None
		self.__state__			        = None
		self.__lord_id__	            = None
		self.__num_players__	        = None
		self.__players__	            = None
		self.__num_discard_cards__	    = None
		self.__discard_cards__		    = None
		self.__num_deposit_cards__	    = None
		self.__deposit_cards__		    = None
		self.__num__equipment_cards__	= None
		self.__equipment_cards__		= None
		self.__num_fate_zone_cards__	= None
		self.__fate_zone_cards__		= None
		self.__num_hand_cards__			= None
        self.__num_keep_cards__         = None
        self.__is_fold__                = None
        self.__num_fold__               = None
		self.__license_action__			= None
		
		
		def __get__stage__(self): return self.__stage__
		stage = property(__get_stage__, doc="There are two stage in ThreeKing. In the first stage(stage = 0), the player gets the same number of the poker cards after he takes an action (some actions)."+ "In the second stage (stage=1), the player doesn't get the suplemment.")
		
		def __get_state__(self):
			if self.__state__ is None:
				return None
			return tuple(self.__state__)
		state = property(__get_state__, doc=" There are six states in ThreeKing for each player. state=['LiuBei',0]"

		def __get_lord_id__(self): return self.__lord_id__
		lord_id = property(__get_lord_id__, doc="lord_id= 1")

		def __get_players__(self):
			if self.__palyers__ is None:
				return None
			return tuple(self.__players__)
		players = property(__get_players__, doc="[]")

		def __get_num_players__(self): return self.__num_players__
		num_players = property(__get_num_players__, doc="num_players = 4 denotes the number of players in this game")
		
		def __get_discard_cards__(self):
			if self.__discard_cards__ is None:
				return None
			return tuple(self.__discard_cards__)
		discard_cards = property(__get_discard_cards__, doc="discard_cards = [roomai.threeking.ThreeKingPokerCards.lookup(\" \"), ...]")

		def __get_num_discard_cards__(self): return self.__num_discard_cards__
		num_discard_cards = property(__get_num_discard_cards__, doc="num_discard_cards = 10")

		def __get_deposit_cards__(self):
			if self.__deposit_cards__ is None:
				return None
			return tuple(self.__deposit_cards__)
		deposit_cards = property(__get_deposit_cards__, doc="deposit_cards = [roomai.threeking.ThreeKingPokerCards.lookup(\" \"), ...]")

		def __get_num_deposit_cards__(self): return self.__num_deposit_cards__
		num_deposite_cards = property(__get_num_deposit_cards__, doc="num_deposite_cards = 10")

		def __get_equipment_cards__(self):
			if self.__equipment_cards__ is None:
				return None
			return tuple(self.__equipment_cards__)
		equipment_cards = property(__get_equipment_cards__, doc="quipment_cards = [[roomai.threeking.ThreeKingPokerCards.lookup(\" \"), ...],[roomai.threeking.ThreeKingPokerCards.lookup(\" \"), ...]] denotes the players0......")

		def __get_num_equipment_cards__(self):
			if self.__num_equipment_cards__ is None:
				return None
			return tuple(self.__num_equipment_cards__)
		num_equipment_cards = property(__get_num_equipment_cards__, doc="num_equipment_cards = [3,5,2] denotes the player0 has 3 cards in equipment zone.")

		def __get_fate_zone_cards__(self):
			if self.__fate_zone_cards__ is None:
				return None
			return tuple(self.__fate_zone_cards__)
			fate_zone_cards = property(__get_fate_zone_cards__, doc="fate_zone_cards = [[roomai.threeking.ThreeKingPokerCards.lookup(\" \"), ...],[roomai.threeking.ThreeKingPokerCards.lookup(\" \"), ...]] denotes the players0......")

		def __get_num_fate_zone_cards__(self):
			if self.__num_fate_zone_cards__ is None:
				return None
			return tuple(self.__num_fate_zone_cards__)
			num_fate_zone_cards = property(__get_num_fate_zone_cards__, doc="num_fate_zone_cards = [0,1,0] denotes the player0 has 0 card in fate zone, player1 has ...")
	
		def __get_num_hand_cards__(self):
			if self.__num_hand_cards__ is None:
				return None
			return tuple(self.__num_hand_cards__)
		num_hand_cards = property(__get_num_hand_cards__, doc="num_hand_cards = [3,5,2] denotes the players0 3 cards in hand, player1 has ...")

		def __get_num_keep_cards__(self):
			if self.__num_keep_cards__ is None:
				return None
			return tuple(self.__num_keep_cards__)
		num_keep_cards = property(__get_num_keep_cards__, doc="num_keep_cards = 12 denotes 12 cards in keep zone ...")
        
        def __get_is_fold__(self):
            if self.__is_fold__ is None:
                return None
            return tuple(self.__is_fold__)
        is_fold = property(__get_is_fold__, doc="is_fold is an array of which player has take the fold action."

        def __get_num_fold__(self):
            return self.__num_fold__
        num_fold = property(__get_num_fold__, doc="The number of players who has taken the fold action"

		def __get_license_action__(self):
       		return self.__license_action__
    	license_action = property(__get_license_action__, doc="Generally, the player need takes an action with the same pattern as the license action...")




class ThreeKingPrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state of ThreeKing
    '''
    def __init__(self):
        super(ThreeKingPrivateState,self).__init__()
        self.__keep_cards__   = []

    def __get_keep_cards__(self):
        return tuple(self.__keep_cards__)
    keep_cards = property(__get_keep_cards__, doc="The keep cards")

    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = ThreeKingPrivateState()
        newinstance                = super(ThreeKingPrivateState,self).__deepcopy__(newinstance = newinstance)
        newinstance.__keep_cards__ =  [card.__deepcopy__() for card in self.keep_cards   ]
        return newinstance



		
class ThreekingPersonState(roomai.common.AbstractPersonState):
	'''
	The person state of ThreeKing
	'''
	def __init__(self):
		super(ThreeKingPersonState,self).__init__()
		self.__role_id__ 	            = None
		self.__hand_cards__		        = []
		self.__hand_cards_keyset__		= set()
		self.__hand_cards_key__			= ""
	
	def __get_role_id__(self): return self.__role_id__
	role_id  = property(__get_role_id__, doc="role_id = 0")

	def __get_hand_cards__(self):
		return tuple(self.__hand_cards__)
	hand_cards = property(__get_hand_cards__, doc="hand_cards = [roomai.threeking.ThreeKingPokerCards.lookup(\" \"), ...]")
	
	def __get_hand_cards_key__(self):
		return self.__hand_cards_key__
	hand_cards_key = property(self.__get_hand_cards_keyset__, doc="hand_cards_key = \" \"")
	
	def __get_hand_cards_keyset__(self):
		return frozenset(self.__hand_cards_keyset__)
	hand_cards_keyset = property(__get_hand_cards_keyset__, doc="hand_cards_keyset={\" \"}")

	
	def __add_card__(self, c):
		self.__hand_cards__.append(c)
		self.__hand_cards_keyset__.add(c.key)

		for j in range(len(self.__hand_cards)-1,0,-1):
			if ThreeKingPokerCard.compare(self.__hand_cards__[j - 1], self.__hand_cards__[j]) > 0:
				tmp = self.__hand_cards__[j]
				self.__hand_cards__[j] = self.__hand_cards__[j-1]
				self.__hand_cards__[j-1] = tmp
			else:
				break

		self.__hand_cards_key = ",".join([c.key for c in self.__hand_cards__])

	def __add_cards__(self, cards):
	    len1 = len(self.__hand_cards__)
	    for c in cards:
			self.__hand_cards__.append(c)
			self.__hand_cards_keyset__.add(c.key)
	    len2 = len(self.__hand_cards__)

	    for i in range(len1, len2-1):
			for j in range(i,0,-1):
		    	if ThreeKingPokerCard.compare(self.__hand_cards__[j-1], self.__hand_cards__[j]) > 0:
					tmp = self.__hand_cards__[j]
					self.__hand_cards__[j] = self.__hand_cards__[j-1]
					self.__hand_cards__[j-1] = tmp
		    	else:
					break
		self.__hand_cards_key__ = ",".join([c.key for c in self.__hand_cards__])


	def __del_card__(self, c):
    	self.__hand_cards_keyset__.remove(c.key)

        tmp = self.__hand_cards__
        self.__hand_cards__ = []
        for i in range(len(tmp)):
        	if c.key == tmp[i].key:
            	continue
            self.__hand_cards__.append(tmp[i])
        self.__hand_cards_key__ = ",".join([c.key for c in self.__hand_cards__])


	def __del_cards__(self, cards):
    	for c in cards:
        	self.__hand_cards_keyset__.remove(c.key)

        tmp = self.__hand_cards__
        self.__hand_cards__ = []
        for i in range(len(tmp)):
        	if tmp[i].key not in self.__hand_cards_keyset__:
            	continue
        	self.__hand_cards__.append(tmp[i])
        self.__hand_cards_key__ = ",".join([c.key for c in self.__hand_cards__])





