#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################
#                                                                    #    
# @version: 0.1.1                                                      #
# @author: heath behrens                                             #
###################################################################### 

import os, os.path
import urllib2
from urllib import urlretrieve
import thread
import threading
import Queue
from PyQt4.QtCore import *
import gtk, pygtk, pynotify

#######################################################################
# Image downloader class simple contains the functions to extract
# urls from web pages and download images.
# Also handles browsing of skins.be forum pages
#######################################################################
class ImageDownloader(QObject):

    def __init__(self, main):
        QObject.__init__(self)
        self.url_list = []
        self.queue = Queue.Queue()
        self.done = True
        self.home = os.getenv("HOME");
        self.ui = main

    """------------------------------------------------------------------
    Download an image in another thread uses a queue
    ------------------------------------------------------------------"""
    def download_image(self, url):
        self.queue.put_nowait(url)
        while(not self.queue.empty()):
            if (self.done):
                #starts a new thread calling fetch image
                thread = threading.Thread(target=self.fetch_image, args=(self.queue.get_nowait(),)) 
                thread.start()
                self.done = False

    """------------------------------------------------------------------
    download an image (This does not run in a thread unless created prior.) refer
    to download_image() function
    ------------------------------------------------------------------"""
    def fetch_image(self, url):
        self.emit(SIGNAL("update_status(QString)"), url)
        img_name = url[url.rfind("/") + 1 : len(url)]
        urlretrieve(url, self.home+"/Downloads/"+img_name)
        self.done = True
        self.emit(SIGNAL("update_progressbar_value()"))
        
        
    """------------------------------------------------------------------
    finds an image url on a given web page and returns the image url
    works with skins image host so far
    ------------------------------------------------------------------"""
    def extract_image_url( self, url, original_url ):
        
        self.emit(SIGNAL("update_status(QString)"), url)
        #check if the image is hosted on sharenxs and if so append &pjk=l onto it
        if("http://sharenxs" in url or "http://www.sharenxs" in url or "sharenxs.com" in url):
            url = url + "&pjk=l"
        
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        if("image.skins.be" in url or "imagevenue.com" in url):
            for line in response:
                if("<img id=" in line):
                    line = line.strip()
                    split = line.split(" ")
                    for s in split:
                        if(s.startswith("src=")):
                            line = s
                            split = line.split('"')
                            line = split[1]
                            self.emit(SIGNAL("update_extract_url(QString)"), line)
                            return line
                            continue
                        elif(s.startswith("SRC=")):
                            line = s
                            split = line.split('"')
                            line = original_url[0 : original_url.rfind("/")+1] + split[1]
                            self.emit(SIGNAL("update_extract_url(QString)"), line)
                            return line
                            continue
        
        elif("http://sharenxs" in url or "http://www.sharenxs" in url or "sharenxs.com" in url):
            for line in response:
                if("src=" + '"' + "http://sharenxs.com/images/" in line 
                   or "src=" + '"' + "http://www.sharenxs.com/images/" in line
                   or "src=" + '"' + "http://cache.sharenxs" in line):
                    line = line.strip()
                    split = line.split(" ")
                    for s in split:
                        if(s.startswith("src=")):
                            line = s
                            split = line.split('"')
                            line = split[1]
                            self.emit(SIGNAL("update_extract_url(QString)"), line)
                            return line
                            continue
                        elif(s.startswith("SRC=")):
                            line = s
                            split = line.split('"')
                            line = original_url[0 : original_url.rfind("/")+1]
                            self.emit(SIGNAL("update_extract_url(QString)"), line)
                            return line
                            continue
                        
    """-------------------------------------------------------------
    Read a file given a path to a particular file.
    ------------------------------------------------------------------"""
    def read_file(self, url ):
        f = open(url, 'r')
        for line in f:
            s = self.extract_image_url(line, line)
            self.write_image_url_to_file(self.home + "/Downloads/url.txt", s)
        f.close()
        
    def write_image_url_to_file(self, path_to_file, url):
        f = open(path_to_file, 'r+')
        f.write(url)
        f.close()
        
    def fetch_page( self, url ):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        for line in response:
            print line
            
    def browse_forum_page(self, url):
        thread = threading.Thread(target=self.read_forum_page, args=(url,)) 
        thread.start()
                
    """------------------------------------------------------------------
    Read a forum page for skins forums
    ------------------------------------------------------------------"""        
    def read_forum_page( self, url):
        self.emit(SIGNAL("update_status(QString)"), url)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        isRightLine = False
        urlstring = ""
        urlList = []
        for line in response:
            isNext = False
            if("class="+'"content"' in line.strip()):
                isRightLine = True
            elif("class="+'"content hasad"' in line.strip()):
                isRightLine = True
            elif("class="+'"after_content"' in line.strip()):
                isRightLine = False
            elif("class=" + '"prev_next"' + "><a rel=" + '"next"' in line.strip()):
                if(isNext == False):
                    isNext = True
            
            if(isNext):
                substring = line[line.find("href="): line.find("title=")-2]
                split = substring.split('"')
            if(isRightLine):
                urlstring += line.strip() + '\n'
        sp = urlstring.split("<a")
        tmp = ""
        for s in sp:
            if("href=" in s and "target=" in s):
                if("image.skins.be" in s): #handle skins image host
                    if("src=" in s and "border=" in s):
                        tmp = s[s.find("src="): s.find("border=")]
                        tmp = tmp[tmp.find('"') + 1 : tmp.rfind('"')]
                        tmp = tmp.replace("thumb","img")
                        urlList.append(tmp)
                        self.emit(SIGNAL("update(QString)"), tmp)
                else: #handle other imagehosts
                    tmp = s[s.find("href="): s.find("target=")]
                    tmp = tmp[tmp.find('"') + 1 : tmp.rfind('"')]
                    urlList.append(tmp)
                    self.emit(SIGNAL("update(QString)"), tmp)
        self.emit(SIGNAL("update_status(QString)"), "Complete!")
        return urlList            
    
