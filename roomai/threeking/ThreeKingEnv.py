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
        '''
        #player_name and player_role and parameter is valid
        #implement you code!

        if "players" in params:
            self.__params__["players_info"] = params["palyers_info"]
            self.__params__["num_players"] = len(params["players_info])"
        else:
            self.__params__["players_info"] = [['LiuBei','lord'],['MaChao','minister'],['ZhaoYun','minister'],['SiMaYi','rebel'],['ZhangLiao','rebel'],['XuChu','rebel'],['XiaHouDun','spy'],['SunSHangXiaNG','spy']]

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
        self.person_state_history = []

        ##private_state
        self.private_state.__keep_cards__ = allcards ## it means?##check more!!!
        
        for i in range(self.__params__["num_players"l]):
            tmp = []
            for j in range(4):
            # in this part, some an hero can get more cards
            # implement your code!
                c = self.private_state.__keep__cards__.pop() ## check more !!!
                tmp.append(c)
            self.person_states[i].__add_cards__(tmp)

        ##init public_state
        self.public_state.__stage__                 = True

        self.public_state.__previous_id__           = -1 #-1
        self.public_state.__previous_skill__        = None
        self.public_state.__previous_action__       = None
        self.public_state.__licenes_action__        = ThreeKingAction.lookup("")# it means ??????
        self.public_state.__lord_id__               = i  for i in range(self.__params__['num_players']) if self.__params__['player_info'][i][1] == 'lord'
        self.public_state.__num_players__           = self.__params__["num_players"]
        self.public_state.__num_discard_cards__     = 0
        self.public_state.__num_deposit_cards__     = 0
        self.public_state.__num_equipment_cards__   = 0
        self.public_state.__num_fate_zone_cards__   = 0
        self.public_state.__num_hand_cards__        = [len(person_state.hand_cards) for person_state in self.person_states]
        self.public_state.__num_keep_cards__        = len(self.private_state.keep_cards)

        # init self.public_state.__turn__        
        self.public_state.__turn__                  = self.public_state.__lord__id__

        # init self.public_state.__state__
        for info in self.__params__["players_info"]:
            name            = info[0]
            alive           = 1
            peroid          = 0 if info[1] == 'lord' else -1
            hp              = get_hp(name)#implement your code here!
            max_hp          = hp
            sex             = get_sex(name)#implement your code here!
            attack          = get_attack_distance(name)
            defend          = get_defend_distance(name)
            
            tmp             = {'name':name,'alive':alive,'state':state,'hp':hp,'sex':sex,'attack':attack,'defend':defend}

            self.public_state.__state__.append(tmp)
            
        # init self.person_state.__role__
        for i in range(self.__params__["num_players"]):
            self.person_states[i].__role__    = self.__params__["players_info"][i][1]

            if i == self.public_state.trun:
                self.person_states[i].__avaliable_actions__ =  ThreeKingEnv.avaliable_actions(self.public_states, self.person_states[i]) 
            
        self.__gen_history__()# it means?
        infos = self.gen_infos__()# it means?

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
        
        self.change_state()#implement you code here!
        '''
        ThreeKingSkills.take_action(pu,pr,pes,action)# action is an object
        '''

    def complete(cls, env, players):
        '''
        use the game environment to hold a complete for the players
        
        :param env: The game environment 
        :param players: The players
        :return: scores for the players
        '''
        mun_players = len(players)
        infos, public_state, person_states, private_state = env.init()#implement your code here

        for i in range(env.__params__["num_players"]):
            players[i].receive_info(infos[i])

        while public_state.stage == False:
            turn    = public_state.turn
            action  = players[turn].take_action()
            infos, public_state, person_states, private_state = env.forward(action)

            for i in range(env.__params__["num_players"]):
                players[i].receive_info(infos[i])

        #return implement code here!
