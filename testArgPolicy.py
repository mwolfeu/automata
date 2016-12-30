#!/usr/bin/python3

# making/triaging arg combos for, creating, & running tests

import itertools

from dataTypes import pAtomicData, aAtomicData, derivedData

# this should have less access to raw ts data

# gens all combos for given tests, does em, stores results
class argPolicy ():
  #nonSymmetrical	Use args in one order.  Ex: allows 'x=y' but not the redundant 'y=x'
  #noRepeat			  Disallow same arg > once
  #oneCurrent		  One arg must be from last batch of tests (current time-1)
  #maxAgeDomain		How to sublist ts and limit the time domain of args available
  #maxAgeDiff		  Specifies oldest allowed peice of an acceptable arg (prevents bloat)

  # if you need to use goals ad, you can make an action, reflect that does nothing physically

  @staticmethod
  def isSorted(cmpList):
    '''See if a list is sorted by id()'''
    for idx, arg in enumerate(cmpList[1:]):
      if id(cmpList[idx]) > id(arg):
        return(False)
    return(True)
    
  # for a given test, get product of arg combos, test against policy, run / optionally store test results
  # speedup: register each varType so tests would have arg product pre-computed (i.e. only once for each change)
  @staticmethod
  def getArgCombos (testName, tsData, nonSymmetrical=True, noRepeat=True, oneCurrent=True, maxAgeDomain=-2, maxAgeDiff=1):
    tsDataDomain = tsData[maxAgeDomain:]                                 # limit how far back we can compare

    testArgTypes = [x[1] for x in testName.__annotations__.items()]      # get all arg types needed by fcn
    testArgsAvailable = [data for time in tsDataDomain for data in time] # confusing comprehensions ftw!
        
    testArgs = []
    for t in testArgTypes: # all possible args for each required arg by dimension
      testArgs.append([a for a in testArgsAvailable if type(a.value) == t])

    curTime = len(tsData) - 1

    for a in itertools.product(*testArgs):
		
      if nonSymmetrical:  # only test args in one order
        #if argPolicy.isSorted(a) == False:
        #  continue
        symId = [id(x) for x in a]
        if symId != sorted(symId): #are they sorted....
          continue
			
      if oneCurrent and (max([t.age for t in a]) != curTime): 
        continue
        
      if noRepeat and (len([arg.key for arg in a]) != len(set([arg.key for arg in a]))): # only test sets where all args are uniq
        continue
 
      youngest = min([arg.age for arg in a if type(arg) is pAtomicData] + [arg.age for arg in a if type(arg) is aAtomicData] + [arg.youngest for arg in a if type(arg) is derivedData])
      if curTime - youngest > maxAgeDiff:
        continue
			
      # ran the policy gauntlet, do test, append if True
      # might append for false statements one day... so datastructure accomodates
      rv = testName(*[arg.value for arg in a])
      if rv:
        tsData[curTime].append(derivedData (curTime, youngest, testName.__name__, a, rv)) # store it in timestate
    
    
