# RoomAI

[![Build Status](https://travis-ci.org/roomai/RoomAI.svg?branch=master)](https://travis-ci.org/roomai/RoomAI.svg?branch=master)
[![Documentation Status](https://readthedocs.org/projects/roomai/badge/?version=latest)](http://roomai.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/roomai.svg)](https://pypi.python.org/pypi/roomai)
[![Join the chat at https://gitter.im/roomai](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/roomai?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


RoomAI is a toolkit for developing and comparing AI-bots of imperfect information games.



# Installation and Your First Try

You can install roomai with pip

<pre>
pip install roomai
</pre>

Try your first RoomAI program


<pre>
#!/bin/python
from roomai.kuhn import *;
import random

class KuhnPokerExamplePlayer(roomai.common.AbstractPlayer):
    #@override
    def receive_info(self, info):
        if info.person_state.available_actions is not None:
            self.available_actions = info.person_state.available_actions
            
    #@override
    def take_action(self):
        return list(self.available_actions.values())[int(random.random() * len(self.available_actions))]
        
    #@overide
    def reset(self):
        pass

if __name__ == "__main__":
        players = [KuhnPokerExamplePlayer() for i in range(2)]
        env = KuhnPokerEnv()
        scores = KuhnPokerEnv.compete(env, players)
        print scores
</pre>




# For More Information

 - [RoomAI Tutorials](https://github.com/roomai/RoomAI/blob/master/roomai/README.md)
 
 - [RoomAI API Docs](http://roomai.readthedocs.io/en/latest/?badge=latest)
 
 - [RoomAI Model Zoo](https://github.com/roomai/RoomAI/blob/master/models/README.md)


# Contributors

If you would like to contribute to the project, please send me (lili1987mail at gmail.com) an email. We are always happy for more help.
