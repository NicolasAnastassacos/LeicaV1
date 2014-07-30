
#Have not yet been able to succesfully incorporate this into the SpiraConnection class.


class Requirement:

    def __init__(self, ReqID = '', ReqName = '', ReqStatus = ''):
        None

    def getReqs(self, ReqID, ReqName, ReqStatus):
        return ReqID, ReqName, ReqStatus

class Requirements:

    def __init__(self):
        self.ReqDict = dict()
 
    def add(self, Requirement):
        self.ReqDict[Requirement.ReqID] = Requirement

