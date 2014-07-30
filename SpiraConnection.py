__author__ = 'nicolasanastassacos'

import time

from suds.client import Client

import logging
from suds.xsd.doctor import Import, ImportDoctor

import operator
import Requirements

logging.basicConfig(level=logging.INFO)


class SpiraConnector(object):

    projectDict = {}
    sortedProjects = {}

    requirementDict = {}
    sortedRequirements = {}
    MyReqs = Requirements.Requirements()

    connect = ''
    #url = 'http://lmsnus-s-spira/SpiraTeam/Services/v4_0/ImportExport.svc?wsdl'
    url = 'https://demo2.spiraservice.net/nicolasleica1/Services/v4_0/ImportExport.svc?wsdl'

    schema_url = 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
    schema_import = Import(schema_url)
    schema_doctor = ImportDoctor(schema_import)
    client = Client(url, doctor=schema_doctor)

    def connectToServer(self, username, password):

        #username and password determined by what the customer enters.
        #username = Ui_MainWindow.lineEdit_Username.text()
        #password = Ui_MainWindow.lineEdit_Password.text()

        print 'Attempting to connect to server...'
        connect = self.client.service.Connection_Authenticate(username, password)
        #connect = self.client.service.Connection_Authenticate('administrator', 'testpassword1234')
        if connect:
            print 'Connected!'
        else:
            print 'Connection failed.'


    def getAllProjects(self):

        #t0 = time.time()

        #Retrieves projects from the server.
        projectList = self.client.service.Project_Retrieve()
        projects = projectList.RemoteProject
        for project in projects:
            #compile projects in a dictionary, accessible by project name.
            self.projectDict[project.Name] = project.ProjectId

        self.sortedProjects = sorted(self.projectDict.iteritems(), key=operator.itemgetter(1))

        #returns list of tuples. ListView works only on single entry lists.

        #t1 = time.time()

        #total = t1 - t0
        #print total
        #time taken 0.86085

    def connectToProject(self, projectName):

        projectID = self.projectDict[projectName]
        connect = self.client.service.Connection_ConnectToProject(projectID)
        if connect:
            print 'Connection established to project: ' + projectName + '.'
        else:
            print 'Unable to establish connection to project.'

        '''
        connect = self.client.service.Connection_ConnectToProject(1)
        if connect:
                print 'Connection to project established.'
        '''

    def getRequirements(self):

        t0 = time.time()
        #Retrieve all requirements.
        #Filter can be left empty. SUDS error.
        remoteFilter = []
        #count the amount of requiremements to determine necessary numberOfRows
        count = self.client.service.Requirement_Count()
        startingRow = 1
        numberOfRows = count

        reqList = self.client.service.Requirement_Retrieve(remoteFilter, startingRow, numberOfRows)


        if (not reqList):
            print 'No requirements available.'
        else:
            for requirement in reqList.RemoteRequirement:
                #store all requirements as a dictionary by name.
                self.requirementDict[requirement.Name] = [requirement.RequirementId, requirement.StatusName]

            self.sortedRequirements = sorted(self.requirementDict.keys())
            #print sortedRequirements

            #time taken ~3.3 seconds to store and sort items into dictionary.

        #t1 = time.time()
        #total = t1 - t0
        #print total

        #time taken ~3.8 seconds

        '''
        #Error: returns an instance of MyReqs (type dict). Cannot print/display on listWidget.

        for currentReq in reqList.RemoteRequirement:
            #create MyReq, a Requirements instance (dictionary)
            MyReq = Requirements.Requirement()

            #Store attributes as a Requirement instance
            MyReq.ReqID = currentReq.RequirementId
            MyReq.ReqName = currentReq.Name
            MyReq.Status = currentReq.StatusName

            #Add it to the dictionary
            self.MyReqs.add(MyReq)

        t1 = time.time()
        total = t1 - t0
        print total

        #time taken 3.5

        list = self.listWidget_Reqs
        listOfReqs = self.MyReqs
        #print [MyReq.label for MyReq in self.MyReqs]
        #MyReqStr = ', '.join(map(str, listOfReqs))
        for Req in listOfReqs.ReqDict:
            item = QtGui.QListWidgetItem(Req[2])
            list.addItem(item)
        '''

    '''
    def lookUpRequirement(self):
        dialog = Dialog()

        cur = self.listWidget_Reqs.currentItem()
        if not (cur):
            print 'Please select a requirement to look up.'

        reqName =  cur.text()

        reqValues = self.requirementDict[reqName]

        reqValuesStr = ', '.join(map(str, reqValues))

        list = dialog.listWidget_Requirements
        item = QtGui.QListWidgetItem(reqValuesStr)

        list.addItem(item)

        dialog.exec_()
    '''

