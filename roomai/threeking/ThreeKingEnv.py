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

        self.public_state.__previous_id__           = -1#previous id and action used in skill
        self.public_state.__previous_action__       = None#previous id and action used in skill
        self.public_state.__lord_id__               = [i  for i in range(self.__params__['num_players'])  if self.__params__['players_info'][i][1] == 'lord'][0]
        self.public_state.__num_players__           = self.__params__["num_players"]
        self.public_state.__num_discard_cards__     = 0
        self.public_state.__num_deposit_cards__     = 0
        self.public_state.__num_equipment_cards__   = 0 * self.__params__["num_players"]
        self.public_state.__num_fate_zone_cards__   = 0 * self.__params__["num_players"]
        self.public_state.__num_hand_cards__        = [len(p.hand_cards) for p in self.person_states]
        self.public_state.__num_keep_cards__        = len(self.private_state.keep_cards)

        # init self.public_state.__turn__        
        self.public_state.__turn__                  = self.public_state.__lord_id__
        self.public_state.__previous_turn__         = self.public_state.__lord_id__#previous turn record the turn before breaked

        # init self.public_state.__state__
        for info in self.__params__["players_info"]:
            name            = info[0]
            period          = 0 if info[1] == 'lord' else -1 # This item record the six peroid of each player,-1 means wait
            hp              = self.player[name][0] + 1 if info[1] == 'lord' else self.player[name][0]
            max_hp          = hp
            sex             = self.player[name][1]
            attack          = 1 #attack_distance
            defend          = 1 #defend_distance
            skill           = self.player[name][2]
            
            tmp             = {'name':name,'period':period,'hp':hp,'max_hp','sex':sex,'attack':attack,'defend':defend,'skill':skill}

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
       
        self.take_action(pu,pr,pes,action)# action is an object
        self.change_state(pu,action)#implement you code here!
    
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
        infos, public_state, person_states, private_state = env.init()

        for i in range(env.__params__["num_players"]):#question why player need receive info? for choose strategy?maybe
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
            public_state.__num_discard_cards__        = len(public_state.discard_cards)
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
    def cal_period_turn(self, pu, action):
        # change period and  turn in public_state

        period_list = [p['period'] for p in pu.__state__]   #The period before change state, -2 means dead, -1 means wait
        name_list = [p['name'] for p in pu.__state__]       #All hero names in public state
        targets = [i for i in range(len(pu.__state__)) if period_list[i] != -2]#Index the hero aliving
        period_turn = period_list.index([i for i in peroid_list if i > 0][0])#index of hero has the period
        pre_turn =  pu.__turn__

        skill_name = action.__skill__
        #First change the hero's period
        #check
        assert len(targets) > 2 and len([i for i in period_list if i > 0]) == 1 
    
        period  = pu.__state__[period_turn]['period']   #Thre period of hero before change state
        hero_skill   = pu.__state__[period_turn]['skill']    #Assume hero only have one skill
        action_skill   = action.__skill__    #Assume hero only have one skill

        # if the period_turn the same as the turn before change state
        #same_turn = True if period_turn == pre_turn  else False


        if period == 0:
            #start period
            active_list = ['GuanXing','LuoShen']
            if action_skill in active_list:
                #This two skill can be taken by one step
                period = 1
            elif action_skill == "Pass":
                #action_skill == pass
                period = 1 
            else:
                #In period 0, action can only be skill or Pass
                print ("error! in period 0, action can onlu be skill or pass!")
                exit()
            #In period 0, there is no case to change turn 
            turn = period_turn  
        
        elif period == 1:
            #fate period
            active_list = ["ShenShu","QiaoBian","GuiCai"]
            if action_skill in active_list:
                #This two skill can be taken by one step
                period = 2 
            elif action_skill == "Pass":
                #action_skill == pass
                period = 2
            elif action_skill == "PanDing":
                period = 2
            else:
                #In period 1, action can only be skill, Pass or PanDing
                print ("error! in period 0, action can onlu be skill ,pass or PanDing!")
                exit()

            #In period 1, there is no case to change turn 
            turn = period_turn  

        elif period == 2:
            #get card period
            active_list = ["TuXi","LuoYi"]
            if action_skill in active_list:
                #This two skill can be taken by one step
                period = 3 
            elif action_skill == "Pass":
                #action_skill == pass
                period = 3
            else:
                #In period 2, action can only be skill or  Pass
                print ("error! in period 0, action can onlu be skill or pass!")
                exit()

            #In period 2, there is no case to change turn 
            turn = period_turn 
 
        elif period == 3:
            #put card period
            #In period 3, assume there is not skill about other !!! check
            active_list = ["ShenShu","XianTu"]

            if action_skill == "Pass":
                #action_skill == pass
                period = 4
                turn = period_turn
 
            if action_skill in active_list:
                #Assume this two skill can be taken by one step
                #In this period, only pass can change period
                period = 3 
                turn = period_turn


            if action_skill in ["WuZhongShengYou"]:
                turn = period_turn
                period = 3 

            else:
        
                #find the action target player,first group skill
                if skillname in ["NanManRuQin","WanJianQiFa","TaoYuanJieYi","WuGuFengDeng"]:
                    targets_turn = []
                    if skillname in ["NanManRuQin","WanJianQiFa"]:
                        targets_turn = targets[period_turn + 1:] + targets[:period_turn]
                    else:
                        targets_turn = targets[period_turn:] + targets[:period_turn]

                    #boundary condition
                    if pu.__pre_turn__ = targets_turn[-1]:
                        turn = period_turn
                        period = 3 
                    else:
                        turn = targets_turn[targets_turn.index(pu.__pre_turn__) + 1]
                        period = 3 

                else:
        
                    if len(targets) != 1:
                        print "error! len of targets != 1"
                        exit()
                    turn = name_list.index([name for name in name_list if name == targets][0])
                    period = 3

        elif period == 4:
            #discard period
            active_list = ["YingZi","XuanFeng"]
            if action_skill in active_list:
                #This two skill can be taken by one step
                period = 2 
            elif action_skill == "Pass":
                #action_skill == pass
                period = 2
            elif action_skill == "QiPai":
                period = 2
            else:
                #In period 4, action can only be skill, Pass or DiPai
                print ("error! in period 0, action can onlu be skill ,pass or PanDing!")
                exit()

            #In period 1, there is no case to change turn 
            turn = period_turn 
 
        elif period == 5:
            #discard period
            active_list = ["ZhiYan","QieTing"]
            if action_skill in active_list:
                #This two skill can be taken by one step
                period = 0 
            elif action_skill == "Pass":
                #action_skill == pass
                period = 0
            else:
                #In period 5, action can only be skill or  Pass
                print ("error! in period 0, action can onlu be skill ,pass or PanDing!")
                exit()

            #In period 5, there is no case to change turn
            turn = targets_turn[targets_turn.index(pu.__pre_turn__) + 1] 

        return period,turn
        
    
    @classmethod
    def change_state(self, action, pu):
        #note

        #The below list of element should be changed in skill function

        #self.private_state.__keep_cards__##change it through .add
        #self.person_state.__hand_cards__ ##change it through .add
        #self.public_state.__num_discard_cards__##change it through .add .del
        #self.public_state.__num_discard_cards__##change it through .add .del
        #self.public_state.__num_deposit_cards__##change it through .add .del
        #self.public_state.__num_deposit_cards__##change it through .add .del
        #self.public_state.__num_equipment_cards__##change it through .add .del
        #self.public_state.__num_equipment_cards__##change it through .add .del 
        #self.public_state.__num_fate_zone_cards__##change it through .add .del
        #self.public_state.__num_fate_zone_cards__##change it through .add .del
        #state : hp attack defend 

        #The below list of element should be changed in change_state function

        #self.public_state.__num_hand_cards__
        #self.public_state.__num_keep_cards__
        #self.public_state.__terminal__         
        #self.public_state.__previous_id__   
        #self.public_state.__previous_action__
        #self.public_state.__lord_id__             
        #self.public_state.__num_players__        
        #self.public_state.__num_discard_cards__   
        #self.public_state.__num_deposit_cards__   
        #self.public_state.__num_equipment_cards__ 
        #self.public_state.__num_fate_zone_cards__ 
        #self.public_state.__num_hand_cards__      
        #self.public_state.__num_keep_cards__    
        #self.public_state.__turn__             
        #self.public_state.__previous_turn__ 
        #self.public_state.__state__   period
        
        period,turn = cal_period_turn(action,pu)
        #change state
        for index in range(len(self.public_state.__state__)):
            
            if self.public_state.__state__[index]['hp'] <= 0:
                self.public_state.__state__[index]['period'] = -2:
            
            if turn == index:
                self.public_state.__state__[turn]['period'] == period
            elif self.public_state.__state__[index]['period'] >= 0:
                self.public_state.__state__[index]['period'] = -1:
                
        #change period and turn
        self.public_state.__turn__  = turn
        
                     
        self.public_state.__num_hand_cards__         = [len(self.person_states[i].__hand_cards__) for i in range(self.public_state.__num_players)]
        self.public_state.__num_keep_cards__         = len(self.private_state.__keep_cards__)    
        #self.public_state.__terminal__              = 
        #self.public_state.__previous_id__   
        #self.public_state.__previous_action__
        self.public_state.__num_discard_cards__      = len(self.public_state.__discard_cards__)   
        self.public_state.__num_deposit_cards__      = len(self.public_state.__deposit_cards__)     
        self.public_state.__num_equipment_cards__    = [len(self.public_states[i].__equipment_cards__) for i in range(self.public_state.__num_players)] 
        self.public_state.__num_fate_zone_cards__    = [len(self.public_states[i].__fate_zone_cards__) for i in range(self.public_state.__num_players)]
        #self.public_state.__previous_turn__ 
        
        

    @classmethod
    def is_ask_wuxie(self, action, pu, pe):
        # calculate the condition of asking WuXieKeJi
        # return the list of id who has WuXieKeJi or None
        card = action.__card__
        ask_WuXie = None
        is_JinNang = False
        has_WuXie = False
        
        tmp = list()

        person_cards = list()
        for i in range(len(pu.__state__)):
                
            if pu.__state__[i]['period'] == -2:
                person_cards.append([])

            else:
                tmp = pe[i].__hand_cards_key__.split(',')
                name_list = [c.split('_')[0] for c in tmp]
                person_cards.append(name_list)

                if "WuXie" in name_list:
                    has_WuXie = True
                    tmp.append(i)
        
        if card is not None and card.__genre__ == "JinNang":
            is_JinNang = True

        if is_JinNang  and has_WuXie:
           
            ask_WuXie = list()
            ask_WuXie = tmp

        return ask_WuXie
             

 
    @classmethod
    def available_actions(cls, pu, pe, action):
        #generate avaliable action
        available_actions   = dict()
        #some element that affect the avaliable action
        name_list       = [p['name'] for p in pu.__state__]
        period_list     = [p['period'] for p in pu.__state__]  
        turn            = pu.__turn__
        hero_name       = name_list[turn]
        hero_period     = pu.__state__[turn]['period'] 
        hero_hp         = pu.__state__[turn]['hp']
        hero_sex        = pu.__state__[turn]['sex']
        skill_name      = action.__skill__

        cards           = pe[turn].__hand_cards__ 

        if hero_period == 0 and hero_name == "ZhuGeLiang":
            avaliable_actions.append(ThreeKingAction.lookup('Pass'))
            avaliable_actions.append(ThreeKingAction.lookup('GuanXing'))
 

        return available_actions

    @classmethod
    def print_info(self,params,pu,pe,pr):
    
        print "players info in env params: ", params["players_info"]
        print "lord id in public_state: ", pu.__lord_id__
        print "cards in person_states[0]: ", pe[0].__hand_cards_key__
        print "num of cards in discard zone: ", pu.__num_discard_cards__
        print "num of hand cards in public_state: ",pu.__num_hand_cards__
        print "num of cards in private_state: ",pu.__num_keep_cards__
        
