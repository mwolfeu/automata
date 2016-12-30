# register any actors and their AD

from genModels import learn

# Right now this mediates actors and the world.  Dunno if this is smart long term
# It assumes too much about how a world would be built  *change later*
class context ():
  
  def __init__(self, objs, w=None):
    if w!=None:
      self.registerWorld(w)
      
    self.learn = learn()
    
    self.actors = [] # actors are characterized by having pAd and potentially DD / aAD 
    for o in objs:
      self.registerActor (o)
      

  def deregisterActor(self, instance): # given an instance, take it out of the actors list
    self.world.deregisterActor(instance)
    self.actors.remove(instance)
    return(instance.__class__)
    
  def registerActor(self, obj):
    instance = obj(self, self.learn)
    self.actors.append(instance)
    self.world.registerActor(instance)
    if not self.setWorldLoc(instance, instance.initX, instance.initY):
      print("Err setting init location for: ", instance)
      exit (0)
      
  def registerWorld (self, obj):
    self.world = obj()
      
  def getWorldInfo (self, obj): # pass along something from world dict
    return (self.world.locations[obj])
  
  def getAllActorsLocations(self, callingActor): # assuming everyone sees everyone.  no occlusions
    # callingActor can be used for perspective occlusions later
    data = []
    for actor in self.world.locations:  # do nothing placeholder right now
      data.append(self.world.locations[actor])
    return (data)
    
  def setWorldLoc (self, obj, x, y):
    return(self.world.requestLocationChange(obj, x, y))
    
  def tick(self): # when time changes, call this first
    
    self.world.printContext()
    
    for a in self.actors: #FIXME move all this into Actor...
      if a.tok():
        name = self.deregisterActor(a)
        self.registerActor(name)
         
        
