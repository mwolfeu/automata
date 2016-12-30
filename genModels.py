from dataTypes import xCoord, yCoord, actBool, actorTime
from dataTypes import pAtomicData, aAtomicData, derivedData
from testArgPolicy import argPolicy
import numpy as np
from copy import deepcopy
import _pickle as pickle # was cPickle in python2

# models applicable to many types of actors

# saved/loaded DD needs to be serialized.  Methods can't be.
# This saves all symbols (methods) to a lookup table and generates a key
# the key can replace symbol instances in DD thus making them serializable
class symbol ():
  # vars can be gotten from timespace slots actions / tests / datatype classes must be registered
  
  #def __init__(self): 
  #  self.store = {}
    
  #def registerSymbol (self, s):
  #  self.store[s.__name__] = s  # for a method
  
  #  store(self, s):
  # with	open('/tmp/my_output.txt',	'w')	as	handle:
  # 			handle.write('This	is	some	data!')
  
  def deserialize (s): # read into observations
    return (pickle.loads(s))
    
  def serialize (self, data): # and store
    global ttt
    age=data.age
    
    # d = deepcopy(data)
    d = data.copy()
    d.makeSerializable(age)
    return (pickle.dumps(d)) # when writing to store make a "completelyWritten" bool for sanity in case a process gets killed mid write. (could totally fuck the whole store)
    
import time
# idea: start small w reps.  increase till one slope > -2.  commit all -1.29 and beyond.
# compiles/saves/loads serialized objects
# runs curves when stores are large enough
# marks data as learned
class learn ():  # stores data for all actors in one big lump... BAD... add another layer of indirection later

  def __init__(self): 
    self.store = {}
    self.interestingStore = []
    self.magicNumRepetitions = 400 # just a W.A.G.
    self.symbols = symbol()

  def getSuggestions(self, testFcn):
    ''' Match elements of interestingStore to current timeState data and 
    do housekeeping on worth of elements.  Take an arbitrary function from
    the memory model to evaluate data.  
    testFcn returns associated action if any and a match equaling:
     1 =  found all arguments, associated tests passed,
     0 =  couldn't find some arguments. 
    -1 =  found all arguments, some associated tests failed. 
    To which we return a sorted (by y val) list of actions whose associated args passed all tests.'''
    #suggestions = []
    sugDict = {}
    for i in self.interestingStore:  # compare the interesting data alg
      action, match = testFcn(symbol.deserialize(i["intData"]))
      i["aTime"] = time.time() # update access time
      if match == 1:
        i["score"] += 1    # score could relate to forgetting?
        i["aTime"] = time.time()
        if action in sugDict:
          sugDict[action].append(i["z"][0] * -1)
        else:
          sugDict[action] = [i["z"][0] * -1]
        #suggestions.append((action, i["z"][0])) # compile all that matched w associated z->y value
      if match == -1:
        i["score"] -= 1
        i["aTime"] = time.time()
        
    totScore = 0
    for key, val in list(sugDict.items()):  # average them all
      sugDict[key] = sum(val) / len(val)
      if sugDict[key] < 0:
        del sugDict[key] # get rid of the ones having negative associations
      else:
        totScore += sugDict[key]
        
    for key in sugDict.keys():  # change to percentage confidence
      sugDict[key] = (100/totScore) * sugDict[key]
      
    return(sorted([(k, sugDict[k]) for k in sugDict.keys()], key=lambda i: i[1])) # return sorted list
    
  def setInterestingStore(self, interestingData):  # add priortized desires as dict key containing this interesting data
    '''Add entry to interesting store w metrics'''
    # don't re-store dup Os, connect w want
    for i in interestingData: # each is formed like: z, o, coords
      oldID = [d for d in self.interestingStore if d["intData"] == i[1]]  # get dupes
      if len(oldID) > 1:
        print ("ID Insert Error.  Should never be more than one already in there.")
        
      if len(oldID) == 1:
        oldID[0]["z"] =  (oldID[0]["z"] + i[0])/ 2  # Average them.  Change anything else?
      else:  
        self.interestingStore.append({"intData":i[1], "z":i[0], "score":0, "cTime":time.time(), "aTime":time.time()}) # create time and the interesting dd

  # for given DD, assembles x(distance to goal), y(% slots where i noticed DD) per run
  # gets line equation:  steeper = more difference between short and long runs = better (ASSUMPTION)  
  # from all lEq values it splits em into -/+ and finds the highest inflection points 
  # beyond inflection point is the best observations (ASSUMPTION) 
  # store best observations in "interesting" store
  def getLineEquations (self, runs):
    x=[r["metric"] for r in runs] # x axis values
    
    allObservables = []
    for run in runs:  # build master list of everything observed across all runs
      allObservables += [k for k in run["ddQty"].keys() if b"AND" in k ] # HACK: to cut down data. take out later    b"AND" is to turn it into bytestring
      
    allObservables = set(allObservables) # make each element uniq

    lEq = [] # list of line eqs
    for o in allObservables:
      coords=[]
      for run in runs:
        if o in run["ddQty"]:
          coords.append((run["metric"], run["ddQty"][o]*(100/len(run["ops"]))))  # change from count to %
        else:
          coords.append((run["metric"], 0))
          
      coords = sorted(coords, key = lambda c: c[0])  # sort by x value
      z = np.polyfit([x[0] for x in coords], [y[1] for y in coords], 1) # z = (y slope, x starting point)
      lEq.append((z, o, coords)) # lEq value, observable, coordinates
      
    lEq = sorted(lEq, key = lambda s: s[0][0])  # sort by y slope value
    lEqNeg = [e for e in lEq if e[0][0] < 0] # these are "I should do that" relations
    lEqPos = [e for e in lEq if e[0][0] > 0] # these are "I shouldn't do that" relations
    lEqPos.reverse() # to print best matches first
    diffsNeg = np.diff([e[0][0] for e in lEqNeg]) # max of these shows highest inflection point in curve
    diffsPos = np.diff([e[0][0] for e in lEqPos])
    #if len([i for i,e in enumerate(diffsNeg) if e == max(diffsNeg)]) == 0:
    #  import code						# drop to interpreter
    #  code.interact(local=locals())
    # BUG!!!  len [i for i,e in enumerate(diffsNeg) if e == max(diffsNeg)] can be 0 as curve flattens out.  Dereferencing it below will crash
    idxNeg = [i for i,e in enumerate(diffsNeg) if e == max(diffsNeg)][0] # index of the largest diff in curve
    idxPos = [i for i,e in enumerate(diffsPos) if e == max(diffsPos)][0] 
    
    interestingNeg = lEqNeg[:idxNeg + 1] # get info starting above / below inflection point
    interestingPos = lEqPos[:idxNeg + 1]
        
    # for i in interestingNeg:
    #   print ("slope:", i[0][0], "\nobservable:\n", i[1]) # print most interesting : not useful yet but.... almost...
    
    self.setInterestingStore(interestingNeg) # + interestingPos
    
  def getMinRun (self, key):
    return (self.store[key]["minRun"])
    
  # Register a run that fulfilled a desire  potentially run metrics
  def registerRun(self, key, run, metricFcn): # metricFcn = grades how well you did
    if not key in self.store: # create new if not existing
      self.store[key] = {"minRun":len(run), "minMetric":None, "avrMetric":None, "metricFcn":metricFcn, "runs":[]}

    if self.getMinRun(key) == None or len(run) < self.getMinRun(key): # truncate all: this should not be hardcoded but part of a housekeeping fcn passed in
      self.store[key]["minRun"] = len(run)
      for r in (R["ops"] for R in self.store[key]["runs"]): #INEFFICENT as runs will never get larger.  should stop when truncLen = timeSlotLen
        r[:] = (t[:self.getMinRun(key)] for t in r)    # Truncate all tests to shortest # steps
    
    # should sort/insert runs by metric for speedup
    self.store[key]["runs"].append({"metric":-1, "ddQty":{}, "ops":run[:self.getMinRun(key)]})
    lastRun = self.store[key]["runs"][-1]
    lastRun["metric"] = self.store[key]["metricFcn"] (lastRun["ops"]) # rate this run
    
    if self.store[key]["minMetric"] == None or lastRun["metric"] < self.store[key]["minMetric"] : # update minMetric
      self.store[key]["minMetric"] = lastRun["metric"] 
      
    for step in lastRun["ops"]:
      for d in step:
        if type(d) is derivedData:
          serializedD = self.symbols.serialize(d) # generalized DD key
          if serializedD not in lastRun["ddQty"]: # store the quantity of each dd per run
            lastRun["ddQty"][serializedD] = 1
          else:
            lastRun["ddQty"][serializedD] += 1
    
    numRuns = len(self.store[key]["runs"])
    if numRuns > self.magicNumRepetitions:  # keep list at x length
      idxs = [i for i, r  in enumerate(self.store[key]["runs"]) if r["metric"] > lastRun["metric"]] # get indices of elements whose distance is larger
      for i in idxs[:int(numRuns/10)]:           # delete (max) fraction off list if over minimum
        del (self.store[key]["runs"][i])  
        
      if len(idxs) == 0:                         # else delete the last one so we won't calc the lEq on it
        del (self.store[key]["runs"][:-1]) 
      else:
        pass # if you have nothing to delete and no suggestion fatigue, mark as learned
      
    if len(self.store[key]["runs"]) == self.magicNumRepetitions: # do learning at watermark & periodically thereafter
      #metrics = [r["metric"] for r in self.store[key]["runs"]]
      #self.store[key]["avrMetric"] = sum(metrics) / self.store[key]["minRun"] # this is wrong
      self.getLineEquations (self.store[key]["runs"]) # get list of like eqs    


# an abstracted model of experienced states/time, sorting and utility methods
class memory (): # store, order, & evaluate memory properties

  def __init__(self):
    self.time = 0 # only meant to differentiate states of same name  i.e. 'time' not 'Time'
    self.timeState = [[]]      # array of AD / DD states indexed by time
    self.taSymbols={}    # dict of __name__ to function ptr for actions and tests
    
    # waves order how actions are run
    # each wave's test results will be committed to timeState as data for the next wave
    self.testWaves = {}
    for test in self.xGT, self.xLT, self.xEq, self.yGT, self.yLT, self.yEq:
      self.registerSymbol("padTests", test)
    self.registerSymbol("relationTests", self.AND)
    self.registerSymbol("manually_run", self.timeEq) # used for desire... never run automatically
    
  def findValue (self, name, tsDataSlot):  # for timeState slot, return first value found
    for a in tsDataSlot:
      if a.key == name:
        return (a.value)
      #baseClassStr = a.__class__.__weakref__.__qualname__[:10] # 10 = len atomicData # not needed as we are only ever getting aad
      #if baseClassStr == 'atomicData' and a.key == name:
      #  return (a.value)
    return (None)
      
  def testAgainstCurrent(self, ddata): # return ([],True|False) where [] = list of actions and T/F if all the tests pass
    # actions=[] # this might come later where there are more actions per time tick
    action = None
    args = []
    match = 1
    
    if type(ddata.args[0]) == aAtomicData:
      return (self.taSymbols[ddata.args[0].key], 1)  #FIXME we are assuming only one arg and Falses aren't stored
      
    for a in ddata.args:
      if type(a) == pAtomicData:
        if a.age + self.time < 0: # if age = earlier than ts store can handle
          args.append(None)
        else:
          args.append(self.findValue(a.key, self.timeState[-1 + a.age])) # will only work with generalized DD # truncated?
      
      if type(a) == derivedData:  # AND will hit here
        act, mat = self.testAgainstCurrent(a)
        if act != None:
          action = act    # assuming one action per tick
        if mat == 1:
          args.append(True)
        if mat == 0:
          args.append(None)
        if mat == -1:
          args.append(False)
          
          
        #if match != 0:  # if anywhere along the line we get a 0 preserve it
        #  if mat != 1:  # after this, if we get neg, the whole thing is neg
        #    match = mat # change to 0 or -1
            
        #import code						# drop to interpreter
        #code.interact(local=locals())
    
    
    #FIXME should test if action (ddata.key) exists anymore
    if None in args:    # if one of the values is None  I.E. AD was not in tsStore for given timeslot   
      return (action, 0)  # couldn't match args.  no harm no foul.
      
    #FIXME best action when key not in taSymbols dict?
    if self.taSymbols[ddata.key] (*args):   #INEFFICIENT this will run through everything even if it hits False midway (useful?)
      return (action, 1)  # matched args.  test was true.
    else:
      return (action, -1)  # matched args.  test was false.
      
  def tsAdd (self, data):          # data derived at each insert?
    '''Add AD/DD to timeState store and derive data'''
    self.timeState[-1].append(data)
  
  def deriver(self, key):   # create all derived data you can by running tests on data at a unique time idx
    for test in self.testWaves[key]: # do tests in waves
      argPolicy.getArgCombos (test, self.timeState) # get argCombos for test, do tests, store Trues.
    
  def advanceTime(self):
    self.time += 1
    self.timeState.append([]) # start off a new array of AD/DD for new time interval

  def getTime(self):
    return (self.time)
  
  #def addAction(self, key, act): # add action to symbol resolver dict
  #  self.taSymbols[act.__name__] = act
  
  # add a test (and its action) to a wave & add test to symbol resolver dict
  def registerSymbol (self, key, test, act=False): 
    if act:
      self.taSymbols[act.__name__] = act
    self.taSymbols[test.__name__] = test # for deserialization
    
    if key not in self.testWaves:
      self.testWaves[key] = []
    self.testWaves[key].append(test)
    
  # Too much noise for now
  #  def isZero(self, x: int):
  #  def isPositive(self, x: int):
  #  def isNegative(self, x: int):

  def xGT(self, x0: xCoord, x1: xCoord):
    return x0 > x1
    
  def xLT(self, x0: xCoord, x1: xCoord):
    return x0 < x1

  def xEq(self, x0: xCoord, x1: xCoord):
    return x0 == x1

  def yGT(self, y0: yCoord, y1: yCoord):
    return y0 > y1
    
  def yLT(self, y0: yCoord, y1: yCoord):
    return y0 < y1

  def yEq(self, y0: yCoord, y1: yCoord):
    return y0 == y1
    
  def timeEq(self, t0: actorTime, t1: actorTime):
    return t0 == t1

  def AND(self, x: bool, y: actBool): # actBool here severely limits the comparisons.  # or, xor?
    return x and y

# basic model of desire tree 
# will include dependencies later
class desires():
	
  def __init__(self): 
    self.store = {} # can be sorted / triaged at each step in the future
	
  # need deregister at some point
  def registerWant(self, key, value): # Register a want T/F test.  True == desire fulfilled.
    self.store[key] = value
	
  def testWants(self, testFcn):  # see if any desires are fulfilled
    fulfilledWants = []
    for key,value in self.store.items():
      action, match = testFcn(value)
      if match == 1:
        fulfilledWants.append(key)
        
    for key in fulfilledWants:
      self.store.pop(key, None) # desire fulfilled, take off list
      
    return (fulfilledWants)
  
  def count (self):
    return(len(self.store))
