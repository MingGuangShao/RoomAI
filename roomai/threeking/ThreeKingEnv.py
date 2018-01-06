import roomai.common
from roomai.threeking import ThreeKingPublicState
from roomai.threeking import ThreeKingPrivateState
from roomai.threeking import ThreeKingPublicState
from roomai.threeking import ThreeKingAction
from roomai.threeking import ThreeKingPokerCard
from roomai.threeking import AllThreeKingPatterns
from roomai.threeking import AllThreeKingPokerCards
import random

import roomai.threeking

logger = roomai.get_logger()

class ThreeKingEnv(roomai.common.AbstractEnv):
    '''
    The ThreeKing game environment
    '''
    def init(self, params = dict()):
        '''
        Initialization the ThreeKing game environment with the initialization params.
        The initialization is a dict with some options
        1) allcards: the order of all poker cards appearing 
        2) record_history: whrther to record all history states. if you need call the backward function, please set it to True.
        #3) player_name: players(heros) name
        #4) player_role: players(heros) role
        3) players_info: players (heros) name and role
        #An example of the initialization param is {"player_name":['','','',''],"player_role":['','','',''],"record_history":True}
        AN example of the initialization param is {"players_info":[['','','','',],['','','','']],"record_history":True}
        '''
        #player_name and player_role and parameter is valid
        #implement you code!

        if "players" in params:
            self.__params__["players_info"] = params["palyers_info"]
            self.__params__["num_players"] = len(params["players_info][0])"
        else:
            self.__params__["players_info"] = [['LiuBei','MaChao','ZhaoYun','SiMaYi','ZhangLiao','XuChu','XiaHouDun','SunSHangXiaNG'],['lord','minister','minister','rebel','rebel','rebel','spy','spy']]

            self.__params__["num_players"] = 8

        
        if "allcards" in params:
            allcards = [c.__deepcopy__() for c in params["allcards"]]
        else:
            allcards = [c.__deepcopy__() for c in AllThreeKingPokerCards.values()]
            random.shuffle(allcards)
        self.__params__["allcards"] = allcards

        if "record_history" in params:
            self.__params__["record_history"] = params["record_history"]
        else:
            self.__params__["record_history"] = False


        
        self.public_state = ThreeKingPublicState()
        self.private_state = ThreeKingPrivateState()
        self.person_state = [ThreeKingPersonState() for i in range(self.__params__["num_players"])]

        self.public_state_history = []
        self.private_state_history = []
        self.person_states_history = []

        ##private_state
        self.private_state.__keep_cards__ = allcards ## it means?
        
        for i in range(self.__params__["num_players"l]):
            tmp = []
            for j in range(4):
            # in this part, some an hero can get more cards
            # implement your code!
                c = self.private_state.__keep__cards__.pop()
                tmp.append(c)
            self.person_states[i].__add_cards__(tmp)

        ##public_state
        self.public_state.__turn__                  = #implement code here!
        self.public_state.__is_terminal__           = False
        self.public_state.__previous_id__           = None
        self.public_state.__previous_action__       = None
        self.public_state.__licenes_action__        = ThreeKingAction.lookup("")

        self.public_state.__stage__                 = 0#implement code here!
        self.public_state.__state__                 = [self.__params__["players"][0][0],0]
        self.public_state.__lord_id__               = #implement code here!
        self.public_state.__num_players__           = self.__params__["num_players"]
        self.public_state.__players__               = #implement code here! each player is an object
        self.public_state.__num_discard_cards__     = 0
        self.public_state.__num_deposit_cards__     = 0
        self.public_state.__num_equipment_cards__   = 0
        self.public_state.__num_fate_zone_cards__   = 0
        self.public_state.__num_hand_cards__        = [len(person_state.hand_cards) for person_state in self.person_states]
        self.public_state.__num_keep_cards__        = len(self.private_state.keep_cards)
        self.public_state.__is_fold__               = [False for i in range(self.public_state.num_players)]
        self.public_state.__num_fold__              = 0

        ##person_state
        #change the code! and implement code here!
        for i in range(self.__params__["num_players"]):
            self.person_states[i].__role_id__    = i
            if i == self.public_state.trun:
                self.person_states[i].__avaliable_actions__ =  ThreeKingEnv.avaliable_actions(self.public_states, self.person_states[i]) 
            
        self.__gen_history__()
        infos = self.gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    def forward(self, action):
        '''
        The ThreeKing game environment steps with the action taken by the current player
        :param action:
        :return:
        '''
        pu = self.public_state
        pr = self.private_state
        pes = self.person_state
        trun = pu.turn

        if self.is_action_valid(action, pu, pes[turn]) == False: #implement code here!
            raise ValueError("The (%s) is an invalid action " % (action.key))
        
        if self.is_next_state() == True:
            #implement your code here!
        
        self.change_state()#implement you code here!
        '''
        ThreeKingSkills.NANMAN(pu,action)#
        '''


