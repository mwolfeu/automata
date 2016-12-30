# World in which actors reside
# yep.  just a simple 10x10 matrix

class world():

  def __init__(self):
    self.spaceX=10 # size of matrix
    self.spaceY=10
    self.locations = {} # location dict of all objects
    self.screenCleared = False
    
  def registerActor (self, actorInstance):
    self.locations[actorInstance] = {"name":actorInstance.name, "icon":actorInstance.icon, "x":0, "y":0}
    
  def deregisterActor (self, actorInstance):
    del(self.locations[actorInstance])
  
  def cls (self):
    for y in range(self.spaceY + 5):  # allow some extra for whatever context prints after
      print ('\033[%d;%dH%s' % (y, 0, " " * self.spaceX * 4))
    
  def requestLocationChange (self, obj, x, y):
    if x >= self.spaceX or y >= self.spaceY:
      return (False)
    if x < 0 or y < 0:
      return (False)

    #print ('\033[%d;%dH%s' % (self.locations[obj]["x"], self.locations[obj]["y"]*2, " ")) # unset icon
      
    self.locations[obj]["x"] = x
    self.locations[obj]["y"] = y
	        
    #print ('\033[%d;%dH%s' % (self.locations[obj]["x"], self.locations[obj]["y"]*2, self.locations[obj]["icon"])) # set icon
    #print ('\033[%d;%dH%s' % (self.spaceY, 0, " "))
    
    return (True)
	
  def printContext (self):
    if not self.screenCleared:
      print ('\033[2J') # clear screen
      print ('\033[H')
      self.screenCleared = True
      
    self.cls()
      
    for l in self.locations.keys():
      print ('\033[%d;%dH%s' % (self.locations[l]["x"], self.locations[l]["y"]*2, self.locations[l]["icon"]))
      
    print ('\033[%d;%dH%s' % (self.spaceY, 0, " "))

    

