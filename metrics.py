# graph printing / evaluating

import math
import numpy as np

# for a given run count eval the data
class evaluate ():
  
  def __init__ (self):
    self.testMetrics = [] # array of (goalDist,algDict(converted to %))
    self.algDict = {} # dict of alg str: times called
    self.allAlgs = []  # list of all algs
    self.runLen = "NaN"
    
  def addAlg (self, alg): # add test algorithm str to dict
    if alg not in self.algDict:
      self.algDict[alg] = 1
    else:
      self.algDict[alg] += 1
      
    if alg not in self.allAlgs:
      self.allAlgs.append(alg)
	  
  def flushDict (self, runLen, goalDist): # when run is complete add to array of testMetrics
    self.runLen = runLen
    self.testMetrics.append((goalDist, {key: value*(100/runLen) for (key, value) in self.algDict.items()})) # convert to percentage of run
    self.algDict = {}
  
  def sortTM (self):
    self.testMetrics = sorted(self.testMetrics, key=lambda x: x[0]) # sort by each run's goalDist
    print("Num Algorithms stored: ", len(self.allAlgs))
  
  def graph (self):
    import os
    import sys 
    import datetime
    import matplotlib.pyplot as plt
	  
    datePathStr = sys.path[0] + "/graphs/" + str(datetime.datetime.now()) + "/"
    os.makedirs(datePathStr)
    #keyFile = open(datePathStr + "key.txt", "a")

    x=[m[0] for m in self.testMetrics] # dist from goal
    
    for idx, alg in enumerate(self.allAlgs): #get first alg
      print("Graphing Algorithm: ", idx, "\r", end='')
	
      y=[]
      for d in [dic[1] for dic in self.testMetrics]:
        if alg not in d:
          y.append(0)
        else:
          y.append(d[alg])
		  
      fig, ax = plt.subplots()
      
      # Remove the plot frame lines
      ax.spines["top"].set_visible(False)  
      ax.spines["bottom"].set_visible(False)  
      ax.spines["right"].set_visible(False)  
      ax.spines["left"].set_visible(False)  

      #ax.plot(x, y, 'ro')
      #ax.plot(x, y, 'k--')
      ax.plot(x, y, 'b.-')
      
      # print mean
      # y_mean = [np.mean(y) for i in x]
      # ax.plot(x, y_mean, linestyle='--')
      
      # calc the trendline
      z = np.polyfit(x, y, 1)
      p = np.poly1d(z)
      ax.plot(x,p(x),"c--")
      # the line equation:
      ax.set_title("runLen=" + str(self.runLen) + "\ny=%.6f x+(%.6f)" % (z[0],z[1])) #, horizontalalignment='left'
      
      # axis ticks only on the bottom and left  
      ax.get_xaxis().tick_bottom()  
      ax.get_yaxis().tick_left()  
      
      # Provide tick lines across the plot  
      for y in range(10, 101, 10):  
        plt.plot(range(0, 10), [y] * len(range(0, 10)), "--", lw=0.5, color="black", alpha=0.3) # TODO x here needs to be dynamic
      
      plt.yticks(range(0, 101, 10), [str(x) + "%" for x in range(0, 101, 10)], fontsize=14)  
      plt.xticks(fontsize=14)
      
      ax.set_ylim((0, 101))
      plt.text(0.25, 0.5, alg, fontsize=17, va="center", alpha=0.7, transform = ax.transAxes) #, ha="center"
      
      plt.xlabel('Goal Distance')
      plt.ylabel('Alg Appearance in Run')
      plt.savefig(datePathStr + "y%.6f" % (z[0]) + " " + str(idx) + ".png") # auto sort by change in y + idx for uniqueness 
      plt.close('all')
      
      #plt.show()
      #keyFile.write("\n" + str(idx) + "\n----------\n" + pp(key))

    #keyFile.close()
    print ("") # newline
  
  def getDist (self, x1, y1, x2, y2):
    return ( math.sqrt((x2 - x1)**2 + (y2 - y1)**2) )
