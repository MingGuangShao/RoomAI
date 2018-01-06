import roomai.common
import roomai.threeking
from roomai.threeking import AllThreeKingPatterns

class ThreeKingAction(roomai.common.AbstractAction):
    '''
    The ThreeKing action. The ThreeKing action contains some ...
    '''
    def __init__(self,key):
        if not isinstance(key,str):
            raise TypeError("The key for ThreeKingAction is an str, not %s" %(type(str)))

        super(ThreeKingAction, self).__init__(key)

        self.__skill__          = None
        self.__card__           = None
        self.__targets__        = []
        self.__other_targets__  = []
        self.__target_zones__  =  None
        self.__target_cards__  =  []

        if len(key) > 0:
            action_info = self.key.split(',')
            self.__skill__ = roomai.threeking.ThreeKingSkills.lookup(action_info[0])

            if self.__skill__.name in []:#implement your code here!
                self.__key__ = self.__skill__.name

            elif self.__skill__.name in []:#implement your code here!
                self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1]))
                self.__key__ = self.__skill__.name + ',' + self.__card_.key

            elif self.__skill__.name in []:#implement your code here!
                self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1]))

                for t in action_info[2].split('_'):
                    self.__targets__.append(roomai.threeking.ThreeKingPlayers.lookup(t))
                self.__key__ = self.__skill__.name + ',' + self.__card_.key + ',' + '_'.join([t.name for t in self.__targets__])
            
            elif self.__skill__.name in []:#implement your code here!
                self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1]))

                for t in action_info[2].split('_'):
                    self.__targets__.append(roomai.threeking.ThreeKingPlayers.lookup(t))

                for t in action_info[3].split('_'):
                    self.__other_targets__.append(roomai.threeking.ThreeKingPlayers.lookup(t))
                self.__key__ = self.__skill__.name + ',' + self.__card_.key + ',' + '_'.join([t.name for t in self.__other_targets__])
            
            elif self.__skill__.name in []:#implement your code here!
                self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1]))

                for t in action_info[2].split('_'):
                    self.__targets__.append(roomai.threeking.ThreeKingPlayers.lookup(t))

                for z in action_info[3].split('_'):
                    self.__target_zones__.append(z)

                for c in action_info[4].split('_'):
                    self.__target_cards__.append(roomai.threeking.ThreeKingPokerCard.lookup(c))
                self.__key__ = self.__skill__.name + ',' + self.__card_.key + ',' + '_'.join([z for z in self.__target_zones]) + ','+ '_'.join([c.key for c in self.__target_cards])

            else:
                #implement your code here!
                
        @classmethod
        def __get_skill__(self):
            return self.__skill__
        skill = property(__get_skill__, doc="The skill of this action." ) 

        def __get_card__(self):
            return self.__card__
        card = property(__get_card__, doc="The card of this action." ) 
          
        def __get_targets__(self):
            return tuple(self.__targets__) 
        targets = property(__get_targets__, doc="The targets of this action." ) 

        def __get_other_targets__(self):
            return tuple(self.__other_targets__) 
        other_targets = property(__get_other_targets__, doc="The other targets of this action." ) 

        def __get_target_zones__(self):
            return tuple(self.__target_zones__) 
        target_zones = property(__get_target_zones__, doc="The  target zones of this action." ) 

        def __get_target_cards__(self):
            return tuple(self.__target_cards__) 
        target_cards = property(__get_target_cards__, doc="The  target cards of this action." )

        @classmethod
        def lookup(cls, key) :
        '''
        lookup a ThreeKing action with the specified key
        :param key: THe specified key

        '''
        if key in AllThreeKingActions:
            return AllThreeKingActions[key]
        else:
            AllThreeKingActions[key] = ThreeKingAction(key)
            return AllThreeKingActions[key]

AllThreeKingActions = dict()
