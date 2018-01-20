import roomai.common

class ThreeKingPokerCard(roomai.common.PokerCard):
    '''
    '''

    def __init__(self, point, suit, name, genre):

        self.__name__       = name 
        self.__point__      = point
        self.__suit__       = suit
        self.__genre__      = genre
        self.__key__        = "%s_%s_%s_%s"%(self.__point__,self.__suit__,self.__name__,self.__genre)

    @classmethod
    def lookup(cls, key):
        return AllThreeKingPokerCards[key]



cards  =   [['SHA','7','spade','PuTong', 1],['SHA','8','spade','PuTong', 2],['SHA','9','spade','PuTong', 2],['SHA','10','spade','PuTong', 2],
           ['SHA','10','heart','PuTong', 2],['SHA','11','heart','PuTong', 1],['SHA','2','club','PuTong', 1],['SHA','3','club','PuTong', 1],
           ['SHA','4','club','PuTong', 1],['SHA','5','club','PuTong', 1],['SHA','6','club','PuTong', 1],['SHA','7','club','PuTong', 1],
           ['SHA','8','club','PuTong', 2],['SHA','9','club','PuTong', 2],['SHA','10','club','PuTong', 2],['SHA','11','club','PuTong', 2],
           ['SHA','6','diamond','PuTong', 1],['SHA','7','diamond','PuTong', 1],['SHA','8','diamond','PuTong', 1],['SHA','9','diamond','PuTong', 1],
           ['SHA','10','diamond','PuTong', 1],['SHA','13','diamond','PuTong', 1],['SHAN','2','heart','PuTong', 2],['SHAN','13','heart','PuTong', 1],
           ['SHAN','2','diamond','PuTong', 2],['SHAN','3','diamond','PuTong', 1],['SHAN','4','diamond','PuTong', 1],['SHAN','5','diamond','PuTong', 1],
           ['SHAN','6','diamond','PuTong', 1],['SHAN','7','diamond','PuTong', 1],['SHAN','8','diamond','PuTong', 1],['SHAN','9','diamond','PuTong', 1],
           ['SHAN','10','diamond','PuTong', 1],['SHAN','11','diamond','PuTong', 2],['Tao','3','heart','PuTong', 1],['Tao','4','heart','PuTong', 1],
           ['Tao','6','heart','PuTong', 1],['Tao','7','heart','PuTong', 1],['Tao','8','heart','PuTong', 1],['Tao','9','heart','PuTong', 1],
           ['Tao','12','heart','PuTong', 1],['Tao','12','diamond','PuTong', 1],['NanMan','7','spade','JinNang', 1],['NanMan','13','spade','JinNang', 1],
           ['NanMan','7','club','JinNang', 1],['WanJian','1','heart','JinNang', 1],['TaoYuan','1','heart','JinNang', 1],['WuGu','3','heart','JinNang', 1],
           ['WuGu','4','heart','JinNang', 1],['ShanDian','1','spade','JinNang', 1],['LeBu','6','spade','JinNang', 1],['LeBu','6','heart','JinNang', 1],
           ['LeBu','6','club','JinNang', 1],['WuXie','11','spade','JinNang', 1],['WuXie','12','club','JinNang', 1],['WuXie','13','club','JinNang', 1],
           ['ShunShou','3','spade','JinNang', 1],['ShunShou','4','spade','JinNang', 1],['ShunShou','11','spade','JinNang', 1],['ShunShou','3','diamond','JinNang', 1],
           ['ShunShou','4','diamond','JinNang', 1],['ShunShou','4','spade','JinNang', 1],['ShunShou','11','spade','JinNang', 1],['ShunShou','3','diamond','JinNang', 1],



