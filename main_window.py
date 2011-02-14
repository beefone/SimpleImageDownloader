# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Wed Feb  2 17:36:38 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import gtk, pygtk, pynotify, os, os.path

###############################################################
# 2011 - Heath Behrens
# A button class to create a button and handle dropEvents.
#
###############################################################
class Button(QtGui.QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)
        self.parent = parent
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
      
        if e.mimeData().urls():
            if e.mimeData().hasUrls(): #make sure there is something to use
                e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        url = e.mimeData().urls()[0].toString() #handle the PyQt4.QtCore.QUrl object
        if("img.skins.be" in url): #is an image url
                self.parent.displayArea.append(url)
        else: #is a webpage url and needs to be read
            self.parent.displayArea.append(url)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("SimpleImageDownloader")
        MainWindow.resize(784, 589)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtGui.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.download_pushButton = QtGui.QPushButton(self.widget)
        self.download_pushButton.setObjectName("download_pushButton")
        self.gridLayout.addWidget(self.download_pushButton, 0, 0, 1, 1)
        self.browse_pushButton = QtGui.QPushButton(self.widget)
        self.browse_pushButton.setObjectName("browse_pushButton")
        self.gridLayout.addWidget(self.browse_pushButton, 1, 0, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.clear_pushButton = QtGui.QPushButton(self.widget)
        self.clear_pushButton.setObjectName("clear_pushButton")
        self.gridLayout.addWidget(self.clear_pushButton, 3, 0, 1, 1)
        self.recusion_checkBox = QtGui.QCheckBox(self.widget)
        self.recusion_checkBox.setObjectName("recusion_checkBox")
        self.gridLayout.addWidget(self.recusion_checkBox, 4, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 1, 2, 1)
        self.scrollArea = QtGui.QScrollArea(self.widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 614, 446))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.displayArea = QtGui.QTextEdit(self.scrollAreaWidgetContents)
        self.displayArea.setObjectName("displayArea")
        self.gridLayout_2.addWidget(self.displayArea, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.forumPageInput = QtGui.QLineEdit(self.widget)
        self.forumPageInput.setObjectName("forumPageInput")
        self.horizontalLayout.addWidget(self.forumPageInput)
        self.progressBar = QtGui.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.drop_pushButton = Button("Drop Here!", self)
        self.drop_pushButton.setObjectName("drop_pushButton")
        self.gridLayout_3.addWidget(self.drop_pushButton, 2, 1, 1, 1)
        self.gridLayout_4.addWidget(self.widget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 784, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.clear_pushButton, QtCore.SIGNAL("clicked()"), self.displayArea.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("SimpleImageDownloader", "SimpleImageDownloader", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SimpleImageDownloader", "Status..", None, QtGui.QApplication.UnicodeUTF8))
        self.download_pushButton.setText(QtGui.QApplication.translate("SimpleImageDownloader", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_pushButton.setText(QtGui.QApplication.translate("SimpleImageDownloader", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("SimpleImageDownloader", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_pushButton.setText(QtGui.QApplication.translate("SimpleImageDownloader", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.recusion_checkBox.setText(QtGui.QApplication.translate("SimpleImageDownloader", "Use Recursion", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setToolTip(QtGui.QApplication.translate("SimpleImageDownloader", "Progress....", None, QtGui.QApplication.UnicodeUTF8))
        self.drop_pushButton.setText(QtGui.QApplication.translate("SimpleImageDownloader", "Drop Here!", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("SimpleImageDownloader", "File", None, QtGui.QApplication.UnicodeUTF8))
