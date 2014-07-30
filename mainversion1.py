__author__ = 'nicolasanastassacos'

from PySide import QtCore, QtGui

import time

import sys, random

from wholegui2 import Ui_MainWindow
from suds.client import Client

from suds.cache import DocumentCache
from suds.sax.element import Element
from suds import WebFault

import logging
from suds.xsd.doctor import Import, ImportDoctor

import operator
import Requirements

from requirementsdialog import Ui_Dialog

logging.basicConfig(level=logging.INFO)



class Dialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_getSelect.clicked.connect(self.pushButton_getSelect_Clicked)

    def pushButton_getSelect_Clicked(self):
        self.getSelected()

    def getSelected(self):
        cur = self.listWidget_Requirements.currentItem()
        print cur.text()


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    projectDict = {}
    requirementDict = {}
    MyReqs = Requirements.Requirements()

    connect = ''
    #url = 'http://lmsnus-s-spira/SpiraTeam/Services/v4_0/ImportExport.svc?wsdl'
    url = 'https://demo2.spiraservice.net/nicolasleica1/Services/v4_0/ImportExport.svc?wsdl'

    schema_url = 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
    schema_import = Import(schema_url)
    schema_doctor = ImportDoctor(schema_import)
    client = Client(url, doctor=schema_doctor)


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #All button functions are displayed here
        self.pushButton_ServerConnect.clicked.connect(self.pushButton_ServerConnect_Clicked)
        self.pushButton_GetProjects.clicked.connect(self.pushButton_GetProjects_Clicked)
        self.pushButton_ProjectConnect.clicked.connect(self.pushButton_ProjectConnect_Clicked)
        self.pushButton_ReqSearch.clicked.connect(self.pushButton_ReqSearch_Clicked)
        self.pushButton_lookUpReq.clicked.connect(self.pushButton_lookUpReq_Clicked)

    def pushButton_ServerConnect_Clicked(self):
        self.connectToServer()

    def pushButton_GetProjects_Clicked(self):
        #When the button is pushed, old data in the widget is cleared before entering new data.
        self.listWidget_Projects.clear()
        self.getAllProjects()

    def pushButton_ProjectConnect_Clicked(self):
        self.listWidget_Reqs.clear()
        self.connectToProject()

    def pushButton_ReqSearch_Clicked(self):
        self.listWidget_Reqs.clear()
        self.getRequirements()


    def pushButton_lookUpReq_Clicked(self):
        self.lookUpRequirement()


    def connectToServer(self):

        #username and password determined by what the customer enters.
        username = self.lineEdit_Username.text()
        password = self.lineEdit_Password.text()

        print 'Attempting to connect to server...'
        connect = self.client.service.Connection_Authenticate(username, password)
        #connect = self.client.service.Connection_Authenticate('administrator', 'testpassword1234')
        if connect:
            print 'Connected!'
        else:
            print 'Connection failed.'


    def getAllProjects(self):

        t0 = time.time()

        #Retrieves projects from the server.
        projectList = self.client.service.Project_Retrieve()
        projects = projectList.RemoteProject
        for project in projects:
            #compile projects in a dictionary, accessible by project name.
            self.projectDict[project.Name] = project.ProjectId

        '''
        musics = [
            'Rock',
            'Pop',
            'Rap',
            'Indie',
            'Jazz'
            ]

        for music in musics:
        # Create an item with a caption
            item = QtGui.QStandardItem(music)

        # Add a checkbox to it
            #item.setCheckable(True)

        # Add the item to the model
            model.appendRow(item)

        '''

        '''

        list = self.listView_Projects
        model = QtGui.QStandardItemModel(list)

        sortedProjects = sorted(self.projectDict.iteritems(), key=operator.itemgetter(1))
        #returns list of tuples. ListView works only on single entry lists.

        stringProjects = []
        for project in sortedProjects:
            stringProject = ', '.join(str(i) for i in project)
            stringProjects.append(stringProject)

        #print stringProjects

        for project in stringProjects:
            #Each item is equal to the name of the project.
            #PROBLEM: How to recall the project ID from here.
            #Should also sort by project ID
            item = QtGui.QStandardItem(project)
            model.appendRow(item)
        '''

        '''

        for project in sortedProjects:
            #Each item is equal to the name of the project.
            #PROBLEM: How to recall the project ID from here.
            #Should also sort by project ID

            item = QtGui.QStandardItem(project[0])
            #item.setCheckable(True)
            model.appendRow(item)


        list.setModel(model)
        list.show()

        '''
        sortedProjects = sorted(self.projectDict.iteritems(), key=operator.itemgetter(1))
        #returns list of tuples. ListView works only on single entry lists.

        list = self.listWidget_Projects
        for project in sortedProjects:

            item = QtGui.QListWidgetItem(project[0])
            list.addItem(item)

        #print item

        t1 = time.time()

        total = t1 - t0
        #print total
        #time taken 0.86085

    def connectToProject(self):

        '''
        list = self.listView_Projects

        model = QtGui.QStandardItemModel(list)
        Is item checked?
        if item.checkState():
            print item

        #Need to be able to access the projectDict in order to look up by selected. (Selected is a name)
        #Need to be able to see selected Item.

        projectID = self.projectDict['selectedItem']
        connect = self.client.service.Connection_ConnectToProject(projectID)
        '''

        cur = self.listWidget_Projects.currentItem()
        if not (cur):
            print 'Please select a project first.'

        projectName =  cur.text()

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


            sortedRequirements = sorted(self.requirementDict.keys())
            #print sortedRequirements

            #t1 = time.time()
            #total = t1 - t0
            #print total

            #time taken ~3.3 seconds

            list = self.listWidget_Reqs
            for requirement in sortedRequirements:
                item = QtGui.QListWidgetItem(requirement)
                list.addItem(item)

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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()



