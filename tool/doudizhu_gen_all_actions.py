#!/bin/python

import roomai.doudizhu

print ("doudizhu_action_data=[")

actions = roomai.doudizhu.DouDiZhuPokerEnv.__available_actions_generate_all__()
for action_key in actions:
    print ("'"+action_key+"\t"+ \
          ",".join([str(s) for s in actions[action_key].masterCards])+"\t"+\
          ",".join([str(s) for s in actions[action_key].slaveCards])+"\t" +\
          actions[action_key].pattern[0]+"',")
action = roomai.doudizhu.DouDiZhuPokerAction([roomai.doudizhu.DouDiZhuActionElement.str_to_rank["x"]],[])
print ("'"+action.key + "\t" + \
      ",".join([str(s) for s in action.masterCards]) + "\t" + \
      ",".join([str(s) for s in action.slaveCards]) + "\t" + \
      action.pattern[0]+"',")

action = roomai.doudizhu.DouDiZhuPokerAction([roomai.doudizhu.DouDiZhuActionElement.str_to_rank["b"]],[])
print ("'"+action.key + "\t" + \
      ",".join([str(s) for s in action.masterCards]) + "\t" + \
      ",".join([str(s) for s in action.slaveCards]) + "\t" + \
      action.pattern[0]+"']")


