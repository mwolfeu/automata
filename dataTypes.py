# timeState objects and prettyPrinting utils

# wanted a type difference in atomic data so comparisons  x>y would never happen
# it is reasonable to assume it could _learn_ this comparison but my computer is slow
class xCoord(int):
  pass

class yCoord(int):
  pass

class actBool(int):  # can't use bool as a base type
  pass
  
class actorTime(int):
  pass
  
class learnedData ():  # header for storing & testing genericized AD/DD from previous runs
  promote = 0
  
  def __init__(self, data, promote=True):
    self.data = data
	  #self.dataHash =
	  #self.createDate =
	  #self.lastAccessDate =
    if promote: 
      self.grade += 1
    else:
      self.grade -= 1

# get DD, genericize, search for hash -> return [actions]
# forgetting data

class atomicData ():
	
  def __init__(self, age, var, value):
    self.age = age
    self.key = var
    self.value = value
    
  def pp (self, node=None, spaces=0): # pretty print
    if node == None: node=self
    for i in range(spaces):
      print (" ", end='')
    print ('\033[94m', "AD:", '\033[0m', node.age, node.key, " ", end='') # ANSI BLUE
    if hasattr(node, "value"):  # serialized has no "value"
      if hasattr(node.value, "method"):
        print(node.value.method.__name__, end='') # print method name instead of object value
      else:
        print(node.value, end='')
    print('\n', end='')
    
#  @staticmethod
#  def prettyPrintRelative (node, time0, mutStr, spaces=0): # time0 is your base time to compare to, mutStr is a [""]
#    for i in range(spaces):
#      mutStr[0] += " "
#    mutStr[0] += str(node.age - time0) + " " +  node.key + " "
#    if hasattr(node.value, "method"):
#      mutStr[0] += node.value.method.__name__ # print method name
#    # don't print actual value
#   mutStr[0] += "\n"
    
  def makeSerializable (self, baseAge): # and store 
    self.age -= baseAge
    if hasattr(self, 'value'):
      del(self.value) 
      
  def copy (self):
    return(type(self)(self.age, self.key, self.value))
    
#  @staticmethod
#  def getAtomicValue (timeSlot, name): # get the first atomic value for a given timeslot
#    AD = [a.value for a in timeSlot if type(a) is atomicData and a.key == name]
#    return [AD[0]]

class pAtomicData(atomicData): # "passive" atomic data regarding existence (Ex: this is my x, y)
  pass
  
class aAtomicData(atomicData): # "active" atomic data regarding actions
  pass
    
class derivedData ():
	
  def __init__(self, age, youngestArgAge, testFcn, args, rv):
    self.age = age
    self.youngest = youngestArgAge
    self.key = testFcn
    self.args = args
    self.value = rv
    
  def pp (self, node=None, spaces=0): # pretty print
    if node == None: node=self
    for i in range(spaces):
      print (" ", end='')
    print ('\033[95m', "DD:", '\033[0m', node.age, end='') # ANSI PURPLE
    if hasattr(node, "youngest"): # check if serialized
      print (node.youngest, " ", end='')
    print (node.key, node.value)
    for a in node.args:
      a.pp(a, spaces+1)
      
#  @staticmethod
#  def ppRelative (node, time0, mutStr, spaces=0): # time0 is your base time to compare to, mutStr is a [""]
#    for i in range(spaces):
#      mutStr[0] += " "
#    mutStr[0] += str(node.age - time0) + " " + node.key + " " + str(node.value) + "\n" # don't print youngest
#    for a in node.args:
#      a.ppRelative(a, time0, mutStr, spaces+1)
      
  def makeSerializable (self, baseAge): # and store 
    self.age -= baseAge
    del(self.youngest)
    #mw  self.key = self.key.__name__
    for a in self.args:
      a.makeSerializable (baseAge)

  def copy (self):
    """The "wow deepcopy is shit slow" method """
    d = type(self)(self.age, self.youngest, self.key, [], self.value)
    for a in self.args:
      d.args.append(a.copy())
    return(d)
    
    
