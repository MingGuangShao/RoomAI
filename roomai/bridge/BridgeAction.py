#!/bin/python
import roomai.common
import roomai.bridge

class BridgeAction(roomai.common.AbstractAction):
    '''
    The action of Bridge. There are two stages:1) bidding and 2) playing. 
    The example of the Bridge action's usages:\n
    \n\n
    ################ In the bidding stage, the action key looks like "bidding"_option_(point)_(suit). ################ \n
    ## The option is one of "bid","double","redouble" and "pass".\n
    ## When the option is "bid", the point and suit are the candidate point (one of "A","2","3","4","5","6" and "7")and suit (one of "NotTrump","Spade","Heart","Diamond" and "Club").
    ## When the option is "double" or "redouble" or "pass". No point and suit. The action key looks like bidding_option
    \n  
    >>action = roomai.bridge.BridgeAction.lookup("bidding_bid_A_Heart") ## We strongly recommend you to use the lookup fuction to get an action.\n
    >>action.key \n
    "bidding_bid_A_Heart"\n
    >>action.stage \n
    "bidding"
    >>action.bidding_option\n
    "bid"\n
    >>action.bidding_contract_point \n
    "A"\n
    >>action.bidding_contract_suit\n
    "Heart"\n
    \n
    >>action = roomai.bridge.BridgeAction.lookup("bidding_pass")\n
    >>action.bidding_option\n
    "pass"\n
    \n\n
    ################ In the playing stage, the action key looks like "playing"_point_suit.################  \n
    >> action = roomai.bridge.BridgeAction.lookup("playing_A_heart") ## We strongly recommend you to use the lookup fuction to get an action.\n
    >> action.key \n
    "playing_A_heart"\n
    >>action.stage \n
    "playing"
    >>action.playing_card.point\n
    "A"\n
    >>action.playing_card.point_rank\n
    12\n
    >>action.playing_card.suit\n
    "Heart"\n
    >>action.playing_card.suit_rank\n
    2\n
    '''

    def __init__(self, stage, bidding_option, bidding_point, bidding_suit, playing_pokercard):
        self.__stage__  = stage
        self.__bidding_option__               = bidding_option
        self.__bidding_contract_point__       = bidding_point
        self.__bidding_contract_suit__        = bidding_suit
        self.__playing_pokercard__            = playing_pokercard

        key = None
        if self.__stage__ == "bidding":
            if self.__bidding_option__ == "bid":
                key= "bidding_" + self.__bidding_option__+"_" + str(self.__bidding_contract_point__) + "_" + str(self.__bidding_contract_suit__)
            else:
                key = "bidding_" + self.__bidding_option__
        elif self.__stage__ == "playing":
            key = "playing_" + self.__playing_pokercard__.key
        else:
            raise ValueError("The stage param must be \"bidding\" or \"playing\"")

        super(BridgeAction, self).__init__(key=key)


    def __get_key__(self): return self.__key__
    key = property(__get_key__, doc="The key of the Bridge action. For example, \n"
                                     ">>action = roomai.bridge.BridgeAction.lookup(\"bidding_bid_1_Heart\")\n"
                                     ">>action.key\n"
                                    "\"bidding_bid_A_Heart\"\n"
                                    "## bidding means the bidding stage, bid means the bid option, A means the 1 card point, Heart means the card suit")

    def __get_stage__(self): return self.__stage__
    stage = property(__get_stage__, doc = "The stage of Bridge. For example, \n"
                                          ">>action = room.bridge_BridgeAction.lookup(\"playing_A_Heart\")\n"
                                          ">>action.stage\n"
                                          "\"playing\"")

    def __get_bidding_option__(self):   return self.__bidding_option__
    bidding_option = property(__get_bidding_option__, doc = "When stage = \"bidding\", the bidding_option is one of \"bid\",\"double\",\"redouble\" and \"pass\".\n"
                                                            "When stage = \"playing\", the bidding_option is always None")

    def __get_bidding_contract_point__(self):   return self.__bidding_contract_point__
    bidding_contract_point = property(__get_bidding_contract_point__, doc = "When stage = \"bidding\" and bidding_option = \"bid\", the bidding_contract_point is one of [\"A\",\"2\",\"3\",\"4\",\"5\",\"6\" and \"7\"].\n"
                                                           "When stage = \"bidding\" and bidding_option != \"bid\",the bidding_contract_point is always None\n"
                                                           "When stage = \"playing\", the bidding_contract_point is always None")

    def __get_bidding_contract_suit__(self):   return self.__bidding_contract_suit__
    bidding_contract_suit = property(__get_bidding_contract_suit__, doc = "When stage = \"bidding\" and bidding_option = \"bid\", the bidding_contract_suit is one of \"NotTrump\",\"Spade\",\"Heart\", \"Diamond\" and \"Club\".\n"
                                                          "When stage = \"bidding\" and bidding_option != \"bid\", the bidding_contract_suit is always None\n"
                                                          "when stage == \"playing\", the bidding_contract_suit is always None")

    def __get_playing_card__(self): return self.__playing_pokercard__
    playing_card = property(__get_playing_card__, doc="When stage == \"bidding\", the playing_card always be None\n"
                                            "When stage = \"playing\", the playing_card is the card in this Bridge action. For example, \n"
                                            ">>action = roomai.bridge.BridgeAction.lookup(\"playing_A_Heart\")\n"
                                            ">>action.playing_card.key \n"
                                            "\"A_Heart\"\n"
                                            ">>action.playing_card.point \n"
                                            "\"A\"\n"
                                            ">>action.playing_card.suit  \n"
                                            "\"Heart\"\n"
                                            ">>action.playing_card.point_rank \n"
                                            "12\n"
                                            ">>action.playing_card.suit_rank \n"
                                            "1")


    def __deepcopy__(self, memodict={}, newinstance = None):
        return AllBridgeActions[self.key]

    @classmethod
    def lookup(self, key):
        '''
        lookup an action with the key
        
        :param key: the key of the targeted action
        :return: the action with this key
        '''
        if key not in AllBridgeActions:
            stage = "bidding"
            bidding_option =  None
            bidding_point  =  None
            bidding_suit   =  None
            playing_card   =  None

            if "bidding" in key:
                stage  = "bidding"
                lines  = key.split("_")
                bidding_option = lines[1]
                if bidding_option == "bid":
                    bidding_point  = lines[2]
                    bidding_suit   = lines[3]
            elif "playing" in key:
                stage          = "playing"
                playing_card   = roomai.bridge.BridgePokerCard.lookup(key.replace("playing_", ""))
            else:
                raise ValueError("%s is an invalid key"%(key))

            AllBridgeActions[key] = BridgeAction(stage, bidding_option, bidding_point, bidding_suit, playing_card)
        return AllBridgeActions[key]


AllBridgeActions = dict()