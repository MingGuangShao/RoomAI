import roomai.common

class ThreeKingPokerCard(roomai.common.PokerCard):
    '''
    '''

    def __init__(self, name, point, suit, genre, index):

        self.__name__       = name 
        self.__point__      = point
        self.__suit__       = suit
        self.__genre__      = genre
        self.__index__      = index
        self.__key__        = "%s_%s_%s_%s"%(self.__name__,self.__point__,self.__suit__,self.__index__)

    @classmethod
    def lookup(cls, key):
        return AllThreeKingPokerCards[key]



cards_list  =   [['SHA','7','spade','PuTong', 1],['SHA','8','spade','PuTong', 2],['SHA','9','spade','PuTong', 2],['SHA','10','spade','PuTong', 2],
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
            ['ShunShou','4','diamond','JinNang', 1],['GuoHe','3','spade','JinNang', 1],['GuoHe','4','spade','JinNang', 1],['GuoHe','12','spade','JinNang', 1],
            ['GuoHe','12','heart','JinNang', 1],['GuoHe','3','club','JinNang', 1],['GuoHe','4','club','JinNang', 1],['JueDou','1','spade','JinNang', 1],
            ['JueDou','1','heart','JinNang', 1],['JueDou','3','diamond','JinNang', 1],['WuZhong','7','heart','JinNang', 1],['WuZhong','8','heart','JinNang', 1],
            ['WuZhong','9','heart','JinNang', 1],['WuZhong','11','heart','JinNang', 1],['JieDao','12','club','JinNang', 1],['JieDao','13','club','JinNang', 1],
            ['DaWan','13','spade','ZhuangBei', 1],['ChiTu','5','heart','ZhuangBei', 1],['ZhiXing','13','diamond','ZhuangBei', 1],['JueYing','5','spade','ZhuangBei', 1],
            ['ZhuaHuang','13','heart','ZhuangBei', 1],['DiLu','5','club','ZhuangBei', 1],['BaGua','2','spade','ZhuangBei', 1],['BaGua','2','club','ZhuangBei', 1],
            ['QiLin','5','heart','ZhuangBei', 1],['ZhuGe','1','club','ZhuangBei', 1],['ZhuGe','1','diamond','ZhuangBei', 1],['GuanShi','5','diamond','ZhuangBei', 1],
            ['FangTian','12','diamond','ZhuangBei', 1],['CiXiong','2','spade','ZhuangBei', 1],['QingGang','6','spade','ZhuangBei', 1],['ZhangBa','12','spade','ZhuangBei', 1],
            ['QingLong','5','spade','ZhuangBei', 1]]


AllThreeKingPokerCards = dict()
for card in cards_list:
    num = card[4]
    for i in range(num):
        AllThreeKingPokerCards["%s_%s_%s_%s" % (card[0], card[1], card[2], str(i))] = ThreeKingPokerCard('%s' % card[0],'%s' % card[1],'%s' % card[2],'%s' % card[3],'%s' % str(i))

