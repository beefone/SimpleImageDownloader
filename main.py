#!/usr/bin/python
######################################################################
#                                                                    #    
# @version: 0.1.1                                                      #
# @author: heath behrens                                             #
###################################################################### 

from PyQt4 import QtGui, QtCore
import sys
# Import the interface class
import main_window
from image_download import ImageDownloader
import threading
import thread
import Queue 
import time
import gtk, pygtk, pynotify, os, os.path

queue = Queue.Queue()
downloader_created = False
reader_created = False
reader_queue = Queue.Queue()

###############################################################
# 2011 - Heath Behrens
# Represents a trayIcon
#
###############################################################
class trayIcon(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #********Create Actions for the Tray Menu********#
        self.quitAction = QtGui.QAction(self.tr("&Quit"), self)
        QtCore.QObject.connect(self.quitAction,
        QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("quit()"))

        create_tray_icon()

        self.composeAction.setEnabled(visible)
        QtGui.QWidget.setVisible(self, visible)

        self.trayIcon.show()

    def create_tray_icon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.composeAction)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(bad.svg)

#######################################################################
# Reader thread that reads a web page and extracts the main images
# url from the page source
#######################################################################

class Reader(threading.Thread):
    
    def __init__(self, img_dl):
        threading.Thread.__init__(self)
        self.downloader = img_dl
        self.done = False
        
    def run(self):
        while (not self.done):
            global reader_queue
            global reader_created
            if(not reader_queue.empty()):
                url = reader_queue.get_nowait()
                url = self.downloader.extract_image_url(url, url)
            else:
                n = pynotify.Notification ("Complete!",
                                   "Image urls have been extracted successfully. ",
                                   "notification-message-im")
                n.show () #show the notification
                #self.emit(SIGNAL("update_status(QString)"), "Extraction Complete!")
                self.kill_reader()
                reader_created = False

    def kill_reader(self):
        self.done = True
        
######################################################################
#Class downloader simply monitors the queue for images to download.
#Holds a reference to the image_downloader created.
#####################################################################
class Downloader(threading.Thread):
    
    def __init__ (self, img_dl):
        threading.Thread.__init__(self)
        self.downloader = img_dl
        self.done = False
        
        
    def run(self):
        while (not self.done):
            print "running"
            global queue
            global downloader_created
            if(not queue.empty()):
                self.downloader.fetch_image(queue.get_nowait())
            else:
                n = pynotify.Notification ("Complete!",
                                   "Images have been downloaded successfully. ",
                                   "notification-message-im")
                n.show () #show the notification
                #self.emit(SIGNAL("update_status(QString)"), "Downloading Complete!")
                self.kill_downloader()
                downloader_created = False
                #time.sleep(3) #sleep the thread for a given number of seconds
                
    def kill_downloader(self):
        self.done = True
        
#######################################################################
# Main Gui class
# handles signals and slots. Along with Ui input and such
########################################################################
class Main(QtGui.QMainWindow, main_window.Ui_MainWindow):
    """ The second parent must be 'Ui_<obj. name of main widget class>'.
        If confusing, simply open up ImageViewer.py and get the class
        name used. I'd named mine as mainWindow, hence Ui_mainWindow. """
 
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        # This is because Python does not automatically
        # call the parent's constructor.
        self.setupUi(self)
        self.displayArea.setAcceptDrops(True)
        #notify that the program has started.
        n = pynotify.Notification ("SimpleImageDownloader Running!",
                                   "Drag an image from a web page to the drop here button "
                                   "the link will be displayed. Hit the Browse button to extract the image url. "
                                   "Select Download to download the image, Multiple Images can be extracted and downloaded at once.",
                                   "notification-message-im")
        n.show () #show the notification
        # Pass this "self" for building widgets and
        # keeping a reference.
        self.connectActions()
        self.img_dl = ImageDownloader(self)
        self.progressBar.setValue(0)
        #signals to update the ui from other threads
        QtCore.QObject.connect(self.img_dl,QtCore.SIGNAL("update(QString)"),self.update)
        QtCore.QObject.connect(self.img_dl,QtCore.SIGNAL("update_progressbar_value()"),self.update_progressbar_value)
        QtCore.QObject.connect(self.img_dl,QtCore.SIGNAL("update_status(QString)"),self.update_status)
        QtCore.QObject.connect(self.img_dl,QtCore.SIGNAL("update_extract_url(QString)"),self.update_extract_url)
        
    def update_extract_url(self, url):
        self.displayArea.append(str(url))
        
    def update_progressbar_value(self):
        self.progressBar.setValue(self.progressBar.value() + 1)
            
    def update(self, s):
        self.displayArea.append(str(s))
        
    def update_status(self, s):
        self.label.setText(str(s))

    def download(self, url):
        global downloader_created
        #check if there is already a downloader created
        if("img.skins.be" in url): #is an image url
                queue.put_nowait(url)
        else: #is a webpage url and needs to be read
            queue.put_nowait(url)
        if(not downloader_created): 
            self.downloader = Downloader(self.img_dl)
            self.downloader.start()
            downloader_created = True
    
    def extract_url(self, url):
        global reader_created
        
        reader_queue.put_nowait(url)
                
        if(not reader_created):
            self.reader = Reader(self.img_dl)
            self.reader.start()
            reader_created = True
            
    def extract_url_list(self, list):
        global reader_created
        self.displayArea.clear()
        for url in list:
            if(not "img.skins.be" in url):
                reader_queue.put_nowait(url)
            else:
                self.displayArea.append(url)    
        if(not reader_created):
            self.reader = Reader(self.img_dl)
            self.reader.start()
            reader_created = True
                
    #connect signals to buttons
    def connectActions(self):
        self.download_pushButton.clicked.connect(self.download_callback) #note the use of clicked not clicked()
        self.browse_pushButton.clicked.connect(self.browse_callback) #note the use of clicked not clicked() 
    
    def download_callback(self):
        text = str(self.displayArea.toPlainText()).strip().split('\n')
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(text))
        for t in text:
            self.download(t)
        
    def browse_callback(self):
        display_area_text = str(self.displayArea.toPlainText()).strip().split('\n')
        forum_page_text = str(self.forumPageInput.text())
        if(len(forum_page_text) > 1):
            self.img_dl.browse_forum_page(forum_page_text) # run in separate thread
        elif(len(display_area_text) > 0):
            self.extract_url_list(display_area_text)
                
    def main(self):
        self.show()
 
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    g = Main()
    g.main()
    app.exec_()
    # This shows the interface we just created. No logic has been added, yet.
