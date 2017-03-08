#!/bin/python
import sys
sys.path.append("..")
from DouDiZhuPokerUtils import *

actions_file            = open("actions.txt","w")
handcards2actions_file  = open("handcards2actions.txt","w")
AllActionsDict          = dict()

def extractStraight(hand_cards, numStraightK, count, exclude):
    cards = []
    count = 0

    for i in xrange(ActionSpace.r-1,-1,-1):

        if i not in exclude:
            count  = 0 
        elif hand_cards[i] >= count:
            count += 1
        else:
            count  = 0        

        if count >= count:
            cards.append(hand_cards[i:i+numStraightK])


        return cards          

    
def extractDiscrete(hand_cards, numDiscreteK, count, exclude):
    cards   = []
    
    for i in xrange(numDiscrete):
        
        old_cards = copy.deepcopy(cards)
        for c in xrange(len(hand_cards)):
            if (hand_cards[c] >= count) and (c not in cards) and (c not in exclude):
                for origin in old_cards:
                    if len(origin) == numDiscreteK:  continue
                    copy1 = copy.deepcopy(origin)
                    copy1.append(c)
                    cards.append(copy1)        
                cards.append([c])

    return cards


def gen_actions(hand_cards):

    if "i_" in pattern[0]:
         return []    

    actions = [];
    if pattern[0] == "x_rocket":
         if  hand_cards[ActionSpace.r] == 1 and \
             hand_cards[ActionSpace.R] == 1:
         action = Action([ActionSpace.r, ActionSpace.R],[])
         actions.append(action)
         return actions       

    numMaster   = pattern[1]
    numMasterV  = pattern[2]
    isStraight  = pattern[3]
    numSlave    = pattern[4]
    numSlaveV   = pattern[5]
    
    numMasterCount  = numMaster/numMasterV
    numSlaveCount   = numSlave /numSlaveV

    if isStraight == 1:
        ## master Card set set
        mCardss = extractStraight(hand_cards, numMasterV, numMasterCount, [])
    else:
        mCards = extractDiscrete(hand_cards, numMasterV, numMasterCount, [])

    for mCards in mCardss:
        m = []
        for mc in mCards:
            m.extend([mc for i in xrange(numMasterCount)])
        m.sort()

        sCardss = extractDiscrete(hand_cards, numSlaveV, numSlaveCount, mCards)
        if len(sCardss) > 0:
            for sCards in sCardss:
                s = []
                for sc in sCards:
                    s.extend([sc for i in xrange(numSlaveCount)])
                actions.append(Action(copy.deepcopy(m), s.sort()))
                            
    
    return actions


def gen_handcards_dfs(hand_cards, currentP, currentNum, numList):

    hand_cards_str = ""
    for i in hand_cards:
        hand_cards_str += "%d,"%(i)

    if currentNum > numList:
        pass

    elif currentNum == numList or currentP == 15:
        actions = gen_actions(hand_cards)
        for act in actions:
            act.masterCards.sort()
            act.slaveCards.sort()
            if act not in AllActionsDict:   
                idx = len(AllActionsDict)
                AllActionsDict[act] = idx
                
                mStr = ""
                for c in act.masterCards:
                    mStr += "%d,"%c
                sStr = ""
                for c in act.slaveCards:
                    sStr += "%d,"%c

                actions_file.write("%s\t%s"%(mStr,sStr))
                handcards2actions_file.write("%s\t%d"%(hand_cards_str,idx))

            else:
                idx = AllActionsDict[act]
                handcards2actions_file.write("%s\t%s"%(hand_cards_str,idx))
                

    else:
        range1 = 5
        if currentP == 13 or currentP == 14:
            range1 = 2
        for i in xrange(range1):
            hand_cards[currentP] = i
            gen_handcards_dfs(hand_cards, currentP+1, currentNum + i, numList)
            hand_cards[currentP] = 0


gen_handcards_dfs([0 for i in xrange(15)], 0, 0, 20)
actions_file.close()
handcards2actions_file.close()
