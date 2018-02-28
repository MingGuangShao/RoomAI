#!/bin/python
import roomai.common

def take_action(pu,pr,pes,action):

    skill_name      = action.skill.skill_name
    card            = action.card
    targets         = action.targets
    other_targets   = action.other_targets
    target_zones    = action.targert_zones
    target_cards    = action.target_cards 
    
    if skill_name in ["Pass"]:
        globals().get_str(skill_name)(pu,pr,pes)

    elif skill_name in ["Get","Equip","Fate","NanManRuQin","WuZhongShengYou","WanJianQiFa","TaoYuanJieYi"]:
        globals().get_str(skill_name)(pu,pr,pes,card)

    elif skill_name in ["Sha","FengTianHuaJi","JueDou","WuXieKeJi","LeBuSiShu"]:
        globals().get_str(skill_name)(pu,pr,pes,card,targets)

    elif skill_name in ["ShunShouQianYang","GuoHeChaiQiao"]:
        globals().get_str(skill_name)(pu,pr,pes,card,targets,other_targets)
    
    elif skill_name in ["JieDaoShaRen"]:
        globals().get_str(skill_name)(pu,pr,pes,card,targets,targets_zones,target_cards)


def Sha(pu, pr, pes, card, targets):
    '''
    '''
    pes[pu.turn].__del_cards__(card)
    pu.__num_hand_cards__[turn] = len(pes[pu.turn].hand_cards)

    pu.__add_discard_cards__(card)
    pu.__num_discard_cards__    = len(pu.num_discard_cards) 

    
def NanManRuQin(pu,pr,pes):
    '''
    '''
    pes[turn].__del__cards__(card)
    pu.__num_hand_cards__[turn] = len(pes[turn].hand_cards)

    pu.__add__discard_cards__(card)
    pu.__num_discard_cards__ = len(pu.num_discard_cards)

    pu.__action_history__.append((pu.turn,action))

    return pu,pr,pes

def WuZhongShengYou(pu,pr,pes):
    '''
    '''

def ShunShouQianYang(pu,pr,pes):
    '''
    '''
    



