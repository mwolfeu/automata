#!/usr/bin/python3

# Bayesian Global Optimization engine for (hyper)parameters which continually plays KOTH for given inputs (Yelp Moe)

# v0.3

from register import context
from actors import automata, goal
from matrix import world

# thought qualities expressed by tests:
# simple AD / (time / space) correlation  to action (positive: go there / negative: don't hit a barrier)
# remembering & new desire creation (w relative importance): I got from a to b only when i passed through c,  c is important
# remembering i tried the left road and it didn't help.  go back to when I made the choice and make a different one
# inheriting a wooden barrier and metal barrier both share qualities of barriers
# constructing hypothetical worlds and running tests / same as watching others?

# potential test runs:
#   no barriers, known goal
#   external barriers only, known goal
#   barriers, known goal, goal occluded at times
#   barriers, goal location must be learned
#   moving barriers
#   moving barriers, goal location must be learned
#   moving barriers, moving unknown goal
#   how would you represent getting near something but not touching it?

# FIXUP:
# location memory / history replay  e.g.'if i'm in maze A i won't head down that path'
# compress memories to ones matched to
# weight useful variables, tests, comparisons
# when looking for action: perfect fit, best fit, consider complexity of DD somehow
# when unpickling pad in dd does it save space when you have two dd pointing to same pad?
# docstrings 

# now:
# find slowdown == pickle.dumps, id() 

# need choice fatigue if world pushes back
# desire priorities: relate top desire to interesting data in set fcn
# rejigger symbol object = not for symbols anymore     unserialize -> de  ACTUALLY SAVE N STORE data & catch CTRLC
# every successive run, replace one that is poorer
# keep doing till curve is flat
# mark as learned  self.desires.count()
# mw want should be actor?  need to specify want too!!!
# @voltage.setter  replaces set/ get methods
# 				def	voltage(self,	voltage):
# get every models fingers out of every other one

# registerRun uses TONNES of string matching... ick
# do graphs for most interesting # combine w serialized  ... maybe ask if debug var is on?
# pay attention to feedback from world when changing location
# unhardcode self.magicNumRepetitions
 # lots of FIXMEs which should wait till I have a better handle on model

########
# MAIN #
########

c = context([automata, goal], w=world)

while True:
  c.tick()


''' 
decomposing a problem means:
achieve desire stochastically
find out which states are true at beginning and the end (%over time)
this is what that goal means!
ex: goal would mean y1 == y0 && x1 == x0
run tests to optimize for each
in this way... one desire gets broken down into constituent desires!
'''    
  # import code						# drop to interpreter
  # code.interact(local=locals())

exit(0)
'''
import signal
import sys
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
signal.pause()
'''
