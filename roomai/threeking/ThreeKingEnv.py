import roomai.common
from roomai.threeking import ThreeKingPublicState
from roomai.threeking import ThreeKingPrivateState
from roomai.threeking import ThreeKingPersonState
from roomai.threeking import ThreeKingAction
from roomai.threeking import ThreeKingPokerCard
from roomai.threeking import AllThreeKingPokerCards
from roomai.threeking.ThreeKingSkills import *
import random

import roomai.threeking

logger = roomai.get_logger()

player_info = {'LiuBei':(4,1,['RenDe','JiJiang']),'MaChao':(4,1,['MaShu','TieQi']),'ZhaoYun':(4,1,['LongDan','YaJiao']),'SiMaYi':(3,1,['FanKui','GuiCai']),'ZhangLiao':(4,1,['TuXi']),'XuChu':(4,1,['LuoYi']),'XiaHouDun':(4,1,['GangLie','QingJian']),'SunSHangXiaNG':(3,0,['JieYin','XiaoJi'])}


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

        self.__params__ = dict()

        if "players" in params:
            self.__params__["players_info"] = params["palyers_info"]
            self.__params__["num_players"] = len(params["players_info"])
        else:
            self.__params__["players_info"] = [['LiuBei','lord'],['MaChao','minister'],['ZhaoYun','minister'],['SiMaYi','rebel'],['ZhangLiao','rebel'],['XuChu','rebel'],['XiaHouDun','spy'],['SunSHangXiaNG','spy']]

            self.__params__["num_players"] = 8

        
        if "allcards" in params:
            #allcards = [c.__deepcopy__() for c in params["allcards"]]
            allcards = [c for c in params["allcards"]]
        else:
            #allcards = [c.__deepcopy__() for c in AllThreeKingPokerCards.values()]
            allcards = [c for c in AllThreeKingPokerCards.values()]
            random.shuffle(allcards)
        self.__params__["allcards"] = allcards

        if "record_history" in params:
            self.__params__["record_history"] = params["record_history"]
        else:
            self.__params__["record_history"] = False

        self.player = {'LiuBei':(4,1,['RenDe','JiJiang']),'MaChao':(4,1,['MaShu','TieQi']),'ZhaoYun':(4,1,['LongDan','YaJiao']),'SiMaYi':(4,1,['FanKui','GuiCai']),'ZhangLiao':(4,1,['TuXi']),'XuChu':(4,1,['LuoYi']),'XiaHouDun':(4,1,['GangLie','QingJian']),'SunSHangXiaNG':(4,1,['JieYin','XiaoJi'])}

        
        self.public_state = ThreeKingPublicState()
        self.private_state = ThreeKingPrivateState()
        self.person_states = [ThreeKingPersonState() for i in range(self.__params__["num_players"])]

        self.public_state_history = []
        self.private_state_history = []
        self.person_states_history = []

        ##private_state
        self.private_state.__keep_cards__ = allcards ## it means?##check more!!!
        
        for i in range(self.__params__["num_players"]):
            tmp = []
            for j in range(4):
            # in this part, some an hero can get more cards
            # implement your code!
                c = self.private_state.__keep_cards__.pop() ## check more !!!
                tmp.append(c)
            self.person_states[i].__add_cards__(tmp)
                

        ##init public_state
        self.public_state.__terminal__              = False

        self.public_state.__previous_id__           = -1 #-1
        self.public_state.__previous_action__       = None
        self.public_state.__lord_id__               = [i  for i in range(self.__params__['num_players'])  if self.__params__['players_info'][i][1] == 'lord'][0]
        self.public_state.__num_players__           = self.__params__["num_players"]
        self.public_state.__num_discard_cards__     = 0
        self.public_state.__num_deposit_cards__     = 0
        self.public_state.__num_equipment_cards__   = 0
        self.public_state.__num_fate_zone_cards__   = 0
        self.public_state.__num_hand_cards__        = [len(p.hand_cards) for p in self.person_states]
        self.public_state.__num_keep_cards__        = len(self.private_state.keep_cards)

        # init self.public_state.__turn__        
        self.public_state.__turn__                  = self.public_state.__lord_id__

        # init self.public_state.__state__
        for info in self.__params__["players_info"]:
            name            = info[0]
            alive           = 1
            peroid          = 0 if info[1] == 'lord' else -1
            hp              = self.player[name][0] + 1 if info[1] == 'lord' else self.player[name][0]
            max_hp          = hp
            sex             = self.player[name][1]
            attack          = 1
            defend          = 1
            skill           = self.player[name][2]
            
            tmp             = {'name':name,'alive':alive,'hp':hp,'sex':sex,'attack':attack,'defend':defend,'skill':skill}

            self.public_state.__state__.append(tmp)
            
        # init self.person_state.__role__
        for i in range(self.__params__["num_players"]):
            self.person_states[i].__role__    = self.__params__["players_info"][i][1]

            if i == self.public_state.turn:
                self.person_states[i].__available_actions__ =  ThreeKingEnv.available_actions(self.public_state, self.person_states[i]) 
            
        #self.__gen_history__()
        infos = self.__gen_infos__()

        return infos, self.public_state, self.person_states, self.private_state

    def forward(self, action):
        '''
        The ThreeKing game environment steps with the action taken by the current player
        :param action:
        :return:
        '''
        pu = self.public_state
        pr = self.private_state
        pes = self.person_states
        turn = pu.turn

        if self.is_action_valid(action, pu, pes[turn]) == False: #implement code here!
            raise ValueError("The (%s) is an invalid action " % (action.key))
       
         
        #self.change_state()#implement you code here!
        self.take_action(pu,pr,pes,action)# action is an object
    
        infos = self.__gen_infos__()    
        return infos, self.public_state, self.person_states, self.private_state


    @classmethod
    def compete(cls, env, players):
        '''
        use the game environment to hold a complete for the players
        
        :param env: The game environment 
        :param players: The players
        :return: scores for the players
        '''
        num_players = len(players)
        infos, public_state, person_states, private_state = env.init()#implement your code here

        for i in range(env.__params__["num_players"]):
            players[i].receive_info(infos[i])

        while public_state.terminal == False:
            turn    = public_state.turn
            action  = players[turn].take_action()
            #For Unit Test
            person_states[turn].__add_card__(ThreeKingPokerCard.lookup('SHA_7_spade_0'))
            public_state.__num_hand_cards__        = [len(p.hand_cards) for p in person_states]
            public_state.__num_keep_cards__        = len(private_state.keep_cards)

            # For Unit Test 
            print "BEFORE FORWARD"
            ThreeKingEnv.print_info(env.__params__,public_state, person_states, private_state)
    
            infos, public_state, person_states, private_state = env.forward(action)
            
            print " "
            print "AFTER FORWARD"
            c = private_state.__keep_cards__.pop() ## For Unit Test
            public_state.__num_hand_cards__        = [len(p.hand_cards) for p in person_states]
            public_state.__num_keep_cards__        = len(private_state.keep_cards)
            ThreeKingEnv.print_info(env.__params__,public_state, person_states, private_state)

            for i in range(env.__params__["num_players"]):
                players[i].receive_info(infos[i])
            #For Unit Test
            return 0

        #return implement code here!


    def take_action(self,pu,pr,pes,action):
    
        skill_name      = action.__skill__
        card            = action.__card__
        targets         = action.__targets__
        other_targets   = action.__other_targets__
        target_zones    = action.__target_zones__
        target_cards    = action.__target_cards__
        
        if skill_name in ["Pass"]:
            #globals().get_str(skill_name)(pu,pr,pes)
            globals()[skill_name](pu,pr,pes)

        elif skill_name in ["Get","Equip","Fate","NanManRuQin","WuZhongShengYou","WanJianQiFa","TaoYuanJieYi"]:
            #globals().get_str(skill_name)(pu,pr,pes,card)
            globals()[skill_name](pu,pr,pes,card)
         
        elif skill_name in ["Sha","FengTianHuaJi","JueDou","WuXieKeJi","LeBuSiShu"]:
            #globals().get_str(skill_name)(pu,pr,pes,card,targets)
            globals()[skill_name](pu,pr,pes,card,targets)
         
        elif skill_name in ["ShunShouQianYang","GuoHeChaiQiao"]:
            #globals().get_str(skill_name)(pu,pr,pes,card,targets,other_targets)
            globals()[skill_name](pu,pr,pes,card,targets,other_targets)
        
        elif skill_name in ["JieDaoShaRen"]:
            #globals().get_str(skill_name)(pu,pr,pes,card,targets,targets_zones,target_cards)
            globals()[skill_name](pu,pr,pes,card,targets,targets_zones,target_cards)


    @classmethod
    def is_action_valid(self, action, public_state, person_state):
        #return action.key in person_state.available_actions
        return True


    @classmethod
    def available_actions(cls, public_state, person_state):

        available_actions   = dict()

        '''
        
        '''
        return available_actions

    @classmethod
    def print_info(self,params,pu,pe,pr):
    
        print "players info in env params: ", params["players_info"]
        print "lord id in public_state: ", pu.__lord_id__
        print "cards in person_states[0]: ", pe[0].__hand_cards_key__
        print "num of cards in discard zone: ", pu.__num_discard_cards__
        print "num of hand cards in public_state: ",pu.__num_hand_cards__
        print "num of cards in private_state: ",pu.__num_keep_cards__
        
