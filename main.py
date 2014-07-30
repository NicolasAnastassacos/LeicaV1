__author__ = 'nicolasanastassacos'

from PySide import QtCore, QtGui
import SpiraConnection


import sys

from wholegui2 import Ui_MainWindow

from requirementsdialog import Ui_Dialog


myConnection = SpiraConnection.SpiraConnector()

class Dialog(QtGui.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        self.setupUi(self)
        self.pushButton_getSelect.clicked.connect(self.pushButton_getSelect_Clicked)

    def pushButton_getSelect_Clicked(self):
        cur = self.listWidget_Requirements.currentItem()
        print cur.text()





class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

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

        username = self.lineEdit_Username.text()
        password = self.lineEdit_Password.text()

        myConnection.connectToServer(username, password)

    def pushButton_GetProjects_Clicked(self):
        #When the button is pushed, old data in the widget is cleared before entering new data.
        self.listWidget_Projects.clear()

        myConnection.getAllProjects()

        listSortedProjects = myConnection.sortedProjects

        list = self.listWidget_Projects
        for project in listSortedProjects:
            item = QtGui.QListWidgetItem(project[0])
            list.addItem(item)

    def pushButton_ProjectConnect_Clicked(self):
        self.listWidget_Reqs.clear()
        cur = self.listWidget_Projects.currentItem()
        if not (cur):
            print 'Please select a project first.'
        projectName =  cur.text()
        myConnection.connectToProject(projectName)

    def pushButton_ReqSearch_Clicked(self):
        self.listWidget_Reqs.clear()

        listSortedRequirements = myConnection.sortedRequirements
        list = self.listWidget_Reqs
        for requirement in listSortedRequirements:
                item = QtGui.QListWidgetItem(requirement)
                list.addItem(item)

        myConnection.getRequirements()


    def pushButton_lookUpReq_Clicked(self):
        myConnection.lookUpRequirement()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()



