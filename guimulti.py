# -*- coding: utf-8 -*-
import sqlite3
import sys
import os.path
import platform
import serialportcontext
from PyQt5.QtCore import Qt, QTimer,QThread,pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap 
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, QVBoxLayout, QAction, QFileDialog, QApplication, QLabel,QGroupBox , QInputDialog,QTableWidget,QTableWidgetItem , QMessageBox
import cv2
import glob
from PyQt5 import QtCore, QtGui, QtWidgets


from PyQt5.QtWidgets import QGridLayout, QComboBox
from PyQt5.QtCore import QSize, QRect  
import time
##########################################################################
data = [0]
data1 =[0]
data2 = [0]
data3 = [0]
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import numpy as np



##########################################################################

import imageio
import os

import seaborn as sns
#import matplotlib.pyplot as plt
import scipy.misc

########################################################################
 #thread.changeMap.connect(label.setPixmap,label1.setPixmap,label2.setPixmap,label3.setPixmap)
 
class Thread(QThread):
    changeMap = pyqtSignal(QPixmap)
    changeMap1 = pyqtSignal(QPixmap)
    changeMap2 = pyqtSignal(QPixmap)
    changeMap3 = pyqtSignal(QPixmap)
    
    getData = pyqtSignal(str)
    getData1 = pyqtSignal(str)
    getData2 = pyqtSignal(str)
    getData3 = pyqtSignal(str)
    signalCollect = pyqtSignal(int,int,int,int,name='signalCollect')
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)

    def run(self):

        videoCapture = cv2.VideoCapture(r'/media/pankaj/New Volume/crowdcount/videos/104207/overlay.mp4')
        videoCapture1 = cv2.VideoCapture(r'/media/pankaj/New Volume/crowdcount/videos/200608/overlay.mp4')
        videoCapture2 = cv2.VideoCapture(r'/media/pankaj/New Volume/crowdcount/videos/200702/overlay.mp4')
        videoCapture3 = cv2.VideoCapture(r'/media/pankaj/New Volume/crowdcount/videos/500717/overlay.mp4')

        crowdDensity = np.load('data1.npy',mmap_mode='r')
        crowdDensity1 = np.load('data2.npy',mmap_mode='r')
        crowdDensity2 = np.load('data3.npy',mmap_mode='r')
        crowdDensity3 = np.load('data4.npy',mmap_mode='r')

        
        count1=0
        while True:
            ret, frame = videoCapture.read()
            ret, frame1 = videoCapture1.read()
            ret, frame2 = videoCapture2.read()
            ret, frame3 = videoCapture3.read()
            
            time.sleep(3)

            if ret is False:
                break
            if count1 == 2999:
                break
            count1 = count1 +1
            
            densityCount= int(crowdDensity[count1]-20)
            densityCount1= int(crowdDensity1[count1])
            densityCount2= int(crowdDensity2[count1])
            densityCount3= int(crowdDensity3[count1])
            
            denser = str(densityCount)
            denser1 = str(densityCount1)
            denser2 = str(densityCount2)
            denser3 = str(densityCount3)
            
           # print('count =',count1)
            
            self.getData.emit(denser)
            self.getData1.emit(denser1)
            self.getData2.emit(denser2)
            self.getData3.emit(denser3)
            
            self.signalCollect.emit(densityCount,densityCount1,densityCount2,densityCount3)

            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            convertQtFormat = QPixmap.fromImage(convertQtFormat)
            p = convertQtFormat.scaled(210, 210)
            
            rgbImage1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            convertQtFormat1 = QImage(rgbImage1.data, rgbImage1.shape[1], rgbImage1.shape[0], QImage.Format_RGB888)
            convertQtFormat1 = QPixmap.fromImage(convertQtFormat1)
            q = convertQtFormat1.scaled(210, 210)            
            
            rgbImage2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            convertQtFormat2 = QImage(rgbImage2.data, rgbImage2.shape[1], rgbImage2.shape[0], QImage.Format_RGB888)
            convertQtFormat2 = QPixmap.fromImage(convertQtFormat2)
            r = convertQtFormat2.scaled(210, 210)            
            
            rgbImage3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
            convertQtFormat3 = QImage(rgbImage3.data, rgbImage3.shape[1], rgbImage3.shape[0], QImage.Format_RGB888)
            convertQtFormat3 = QPixmap.fromImage(convertQtFormat3)
            s = convertQtFormat3.scaled(210, 210)            
            
            
            self.changeMap.emit(p)
            self.changeMap1.emit(q)
            self.changeMap2.emit(r)
            self.changeMap3.emit(s)
            
        count1=0

        videoCapture.release()
        videoCapture1.release()
        videoCapture2.release()
        videoCapture3.release()
        
        cv2.destroyAllWindows()



class App(QWidget):
    receiveSignal = QtCore.pyqtSignal(str)
    sendSignal = QtCore.pyqtSignal()

    global alist,dataUpdate
    alist = ['']
    dataUpdate = ['']
    def __init__(self):
        super().__init__()
        self.title = 'Crowd Monitoring' 
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        
        
        #image = cv2.imread(r'C:\Users\Pankaj\Downloads\pank do not throw\WorldExpo\test_video')
        # Combo BOX
        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(1150, 20, 200, 180))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
######################################## PORT #######################
        self.BoxPort = QtWidgets.QComboBox(self.groupBox)
        self.BoxPort.setGeometry(QtCore.QRect(100, 25, 75, 21))
        self.BoxPort.setObjectName("BoxPort")
#####################################COM = COM ##################################################################
        self.COM = QtWidgets.QLabel(self.groupBox)
        self.COM.setGeometry(QtCore.QRect(2, 25, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.COM.setFont(font)
        self.COM.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.COM.setObjectName("COM")
######################################label = Baud rate ##################################################################
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(2, 50, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
####################################################################
        self.BoxBaud = QtWidgets.QComboBox(self.groupBox)
        self.BoxBaud.setGeometry(QtCore.QRect(100, 50, 75, 21))
        self.BoxBaud.setObjectName("BoxBaud")
#################################### ParityBits = Parity Bits ######################################################
        self.ParityBits = QtWidgets.QLabel(self.groupBox)
        self.ParityBits.setGeometry(QtCore.QRect(2, 75, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ParityBits.setFont(font)
        self.ParityBits.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ParityBits.setObjectName("ParityBits")
#########################################################################
        self.BoxCheckSum = QtWidgets.QComboBox(self.groupBox)
        self.BoxCheckSum.setGeometry(QtCore.QRect(100, 75, 75, 21))
        self.BoxCheckSum.setObjectName("BoxCheckSum")
##################################### DataBits = Data Bits ##########################################################        
        self.DataBits = QtWidgets.QLabel(self.groupBox)
        self.DataBits.setGeometry(QtCore.QRect(2, 100, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.DataBits.setFont(font)
        self.DataBits.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DataBits.setObjectName("DataBits")
######################################################################
        self.BoxBits = QtWidgets.QComboBox(self.groupBox)
        self.BoxBits.setGeometry(QtCore.QRect(100, 100, 75, 21))
        self.BoxBits.setObjectName("BoxBits")
###################################### stopBits = Stop Bits ###########################################################
        self.stopBits = QtWidgets.QLabel(self.groupBox)  
        self.stopBits.setGeometry(QtCore.QRect(2, 125, 80, 21))        
        font = QtGui.QFont()
        font.setPointSize(8)
        self.stopBits.setFont(font)
        self.stopBits.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.stopBits.setObjectName("stopBits")
##########################################################################
        self.BoxStopBits = QtWidgets.QComboBox(self.groupBox)
        self.BoxStopBits.setGeometry(QtCore.QRect(100, 125, 75, 21))
        self.BoxStopBits.setObjectName("BoxStopBits")
######################################### Open Button ############################################################
        self.OpenButton = QtWidgets.QPushButton(self.groupBox)
        self.OpenButton.setGeometry(QtCore.QRect(50, 150, 125, 21))
        self.OpenButton.setObjectName("OpenButton")
########################################  Send Button  for sending ####################################################
        self.SendDataButton = QtWidgets.QPushButton(self)
        self.SendDataButton.setGeometry(QtCore.QRect(1300, 450, 50, 75))
        self.SendDataButton.setAutoDefault(True)
        self.SendDataButton.setObjectName("SendDataButton")
########################################  clear Button  for sending ####################################################
        self.clearSendDataButton = QtWidgets.QPushButton(self)
        self.clearSendDataButton.setGeometry(QtCore.QRect(1300, 375, 50, 75))
        self.clearSendDataButton.setObjectName("clearSendDataButton")
        self.clearSendDataButton.clicked.connect(self.clearsenddata)    
####################################### text  box for receiving  ############################################################
        self.ReceivedText = QtWidgets.QTextEdit(self)
        self.ReceivedText.setGeometry(QtCore.QRect(1100, 210, 250, 150))
###################################################################################################################
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ReceivedText.sizePolicy().hasHeightForWidth())
        self.ReceivedText.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ReceivedText.setFont(font)
        self.ReceivedText.setReadOnly(True)
        self.ReceivedText.setObjectName("ReceivedText")
        ################################### Sending text box ###################################
        self.SentText = QtWidgets.QTextEdit(self)
        self.SentText.setGeometry(QtCore.QRect(1100, 375, 200, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SentText.setFont(font)
        self.SentText.setObjectName("SentText")

#########################################################################################################################       
        self.groupBox.setTitle("COM Setting")
        self.COM.setText("COM")
        self.label.setText("Baud rate")
        self.ParityBits.setText("Parity Bit")
        self.DataBits.setText("Data Bit")
        self.stopBits.setText("Stop Bit")
        self.OpenButton.setText("Open")
        self.SendDataButton.setText("Send")
        self.clearSendDataButton.setText("Clear")

        self.SentText.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'PMingLiU\';\"><br /></p></body></html>")
        #groupBox = QGroupBox("Best Food")
 ######################################### controlling post creating group box ########################################################
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(QtCore.QRect(1150,535, 190, 80))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox1.setFont(font)
        self.groupBox1.setObjectName("groupBox1")
        self.groupBox1.setTitle("Manual Post control")

####################################### post 1 ############################################################
        self.post1 = QtWidgets.QPushButton(self.groupBox1)
        self.post1.setGeometry(QtCore.QRect(10, 20, 80, 21))
        self.post1.setObjectName("post1")
        self.post1.setText("Post 1")
        self.post1.setCheckable(True)
        
        #self.post1.toggle()
        self.post1.clicked.connect(lambda:self.whichbtn(self.post1))
        self.post1.clicked.connect(self.btnstate1)

        
        
#################################### post 2 ###########################        
        self.post2 = QtWidgets.QPushButton(self.groupBox1)
        self.post2.setGeometry(QtCore.QRect(100, 20, 80, 21))
        self.post2.setObjectName("post2")
        self.post2.setText("Post 2")
        
        self.post2.setCheckable(True)
        #self.post2.toggle()
        self.post2.clicked.connect(lambda:self.whichbtn(self.post2))
        self.post2.clicked.connect(self.btnstate2)
        
        

#################################### post 3 ###########################        
        self.post3 = QtWidgets.QPushButton(self.groupBox1)
        self.post3.setGeometry(QtCore.QRect(10, 45, 80, 21))
        self.post3.setObjectName("post3")
        self.post3.setText("Post 3")
        
        self.post3.setCheckable(True)
        #self.post3.toggle()
        self.post3.clicked.connect(lambda:self.whichbtn(self.post3))
        self.post3.clicked.connect(self.btnstate3)

#################################### post 4 ###########################        
        self.post4 = QtWidgets.QPushButton(self.groupBox1)
        self.post4.setGeometry(QtCore.QRect(100, 45, 80, 21))
        self.post4.setObjectName("post4")
        self.post4.setText("Post 4")
        
        self.post4.setCheckable(True)
        #self.post4.toggle()
        self.post4.clicked.connect(lambda:self.whichbtn(self.post4))
        self.post4.clicked.connect(self.btnstate4)

######################################### group box for database of RFID ########################################################
        self.groupBoxRFID = QGroupBox(self)
        self.groupBoxRFID.setGeometry(QtCore.QRect(1150,615,190, 80))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBoxRFID.setFont(font)
        self.groupBoxRFID.setObjectName("groupBox1")
        self.groupBoxRFID.setTitle("RFID Database") 
#################################### RFID database ##########################        
        self.RFID = QtWidgets.QPushButton(self.groupBoxRFID)
        self.RFID.setGeometry(QtCore.QRect(10, 20,170, 21))
        self.RFID.setObjectName("rfidtable")
        self.RFID.setText("Open Database")
        self.RFID.clicked.connect(self.showDialog1)     
############################# Rfid Register#########################        
        self.RFIDdata = QtWidgets.QPushButton(self.groupBoxRFID)
        self.RFIDdata.setGeometry(QtCore.QRect(10, 45,170, 21))
        self.RFIDdata.setObjectName("rfidtable")
        self.RFIDdata.setText("Register")
        self.RFIDdata.clicked.connect(self.showDialog2)    


      
        
############################### Group Box and update of serial com and baud rate setting ###############
        print(platform.system())
        
        if platform.system() == "Windows":
            ports = list()
            for i in range(8):
                ports.append("COM%d" %((i+1)))    
            self.BoxPort.addItems(ports)
            print(ports)
            
        if platform.system() == "Linux":
            ports = glob.glob('/dev/tty[A-Za-z]*')
            print(ports)
            self.BoxPort.addItems(ports)

        
        bauds = ["50","75","134","110","150","200","300","600","1200","2400","4800","9600","14400","19200","38400","56000","57600",
            "115200"]
        self.BoxBaud.addItems(bauds)
        self.BoxBaud.setCurrentIndex(len(bauds) - 1)
        
        checks = ["None","Odd","Even","Zero","One"]
        self.BoxCheckSum.addItems(checks)
        self.BoxCheckSum.setCurrentIndex(len(checks) - 1)
        
        bits = ["4 Bits", "5 Bits","6 Bits", "7 Bits", "8 Bits"]
        self.BoxBits.addItems(bits)
        self.BoxBits.setCurrentIndex(len(bits) - 1)
        
        stopbits = ["1 Bit","1.5 Bits","2 Bits"];
        self.BoxStopBits.addItems(stopbits)
        self.BoxStopBits.setCurrentIndex(0)
        
        
        #self.sendSignal.connect(self.__auto_send_update__)
        
        port = self.BoxPort.currentText()
        baud = int("%s" % self.BoxBaud.currentText(), 10)
        self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)

#        self.lineEditReceivedCounts.setText("0")
#        self.lineEditSentCounts.setText("0")
        self.OpenButton.clicked.connect(self.__open_serial_port__)
       # self.pushButtonClearRecvArea.clicked.connect(self.__clear_recv_area__)
        self.SendDataButton.clicked.connect(self.__send_data__)
        self.receiveSignal.connect(self.__display_recv_data__)
       # self.pushButtonOpenRecvFile.clicked.connect(self.__save_recv_file__)
        
        
############################# Setting Label for image  #######################################       
        imglabel = QLabel(self)
        imglabel.setGeometry(QtCore.QRect(0, 0, 1100, 700))

        pixmape = QPixmap('crossroads.jpg')
        scaleimage = pixmape.scaledToWidth(1090)
        imglabel.setPixmap(scaleimage)
#
#        
        label = QLabel(self)
        label.move(450, 0)
        label.resize(210, 210)
        label.setStyleSheet("background-color:blue;")
        
        label1 = QLabel(self)        
        label1.move(830, 260)
        label1.resize(210, 210)
        label1.setStyleSheet("background-color:red;")


        label2 = QLabel(self)        
        label2.move(85, 260)
        label2.resize(210, 210)
        label2.setStyleSheet("background-color:white;")

        label3 = QLabel(self)        
        label3.move(450, 500)
        label3.resize(210, 210)
        label3.setStyleSheet("background-color:yellow;")

        self.label21 = QLabel(self)
        self.label21.move(400, 220)
        self.label21.resize(300, 25)
        self.label21.setStyleSheet("background-color:blue;")#525,245
        
        self.label22 = QLabel(self)        
        self.label22.move(700, 220)
        self.label22.resize(25, 300)
        self.label22.setStyleSheet("background-color:red;")

        self.label23 = QLabel(self)        
        self.label23.move(400, 495)
        self.label23.resize(300, 25)
        self.label23.setStyleSheet("background-color:white;")

        self.label24 = QLabel(self)        
        self.label24.move(375, 220)
        self.label24.resize(25, 300)
        self.label24.setStyleSheet("background-color:yellow;")
        
        
        
        labelt = QLabel(self)
        labelt.move(525, 245)
        labelt.resize(50,50)
        labelt.setStyleSheet("background-color:blue;""font: bold 20pt 'Arial'")#525,245
        labelt.setAlignment(QtCore.Qt.AlignCenter)  
        
        labelt21 = QLabel(self)        
        labelt21.move(650, 350)
        labelt21.resize(50,50)
        labelt21.setStyleSheet("background-color:red;""font: bold 20pt 'Arial'")
        labelt21.setAlignment(QtCore.Qt.AlignCenter)  

        labelt22 = QLabel(self)        
        labelt22.move(400, 350)
        labelt22.resize(50,50)
        labelt22.setStyleSheet("background-color:white;""font: bold 20pt 'Arial'")        
        labelt22.setAlignment(QtCore.Qt.AlignCenter)  
        
        
        labelt23 = QLabel(self)        
        labelt23.move(525, 445)
        labelt23.resize(50, 50)
        labelt23.setStyleSheet("background-color:yellow;""font: bold 20pt 'Arial'")#525,445
        labelt23.setAlignment(QtCore.Qt.AlignCenter)  

#############################################################################################3
        self.groupBoxGraph = QGroupBox(self)
        self.groupBoxGraph.setGeometry(QtCore.QRect(0,700, 1090, 325))

        font = QtGui.QFont()
        font.setPointSize(8)

        self.groupBoxGraph.setFont(font)
        self.groupBoxGraph.setObjectName("groupBoxGraph")
        
        #self.groupBoxGraph.setStyleSheet("background-color:green;")
 
    
        self.horizontalLayout =  QtGui.QHBoxLayout(self.groupBoxGraph)
        self.horizontalLayout.setGeometry(QtCore.QRect(0, 0, 1090, 325))
        

        
        self.win = pg.GraphicsWindow()
        #self.win.resize(200,200)
        self.horizontalLayout.addWidget(self.win)
#        pg.setConfigOption('background', 'w')
#        pg.setConfigOption('foreground', 'k')
        
        self.p6 = self.win.addPlot(title="Density Plot")
        self.curve = self.p6.plot(pen='b')
        self.curve1 = self.p6.plot(pen='r')
        self.curve2 = self.p6.plot(pen='w')
        self.curve3 = self.p6.plot(pen='y')


   
        
                


#################################################################################################### 
        thread = Thread(self)
        thread.changeMap.connect(label.setPixmap)
        thread.changeMap1.connect(label1.setPixmap)
        thread.changeMap2.connect(label2.setPixmap)
        thread.changeMap3.connect(label3.setPixmap)
                
        thread.getData.connect(labelt.setText)
        thread.getData1.connect(labelt21.setText)
        thread.getData2.connect(labelt22.setText)
        thread.getData3.connect(labelt23.setText)
        
        thread.signalCollect.connect(self.collecteddensity)
        #thread.signalCollect.connect(self.plotgraph)
        
        thread.start()
        
         
################################### Crowd count maths ########################################  

    def getmax(self,densitylist):
       # print('crowdDensity list =',densitylist)
        maximumdensity= max(densitylist)
       # print('maximum crowdDensity list =', maximumdensity)
        maxposition = np.argmax(densitylist)
       # print('position of maximum',maxposition)
        
        if maxposition == 0:
           # print('inside 0')
        
            self.post1.setChecked(True)
            self.btnstate1()
            time.sleep(1)
            
            self.post2.setChecked(False)
            self.btnstate2()
            time.sleep(1)
            
            self.post3.setChecked(False)
            self.btnstate3()
        
    
            
        if maxposition == 1:
           # print('inside 1')

        
            self.post1.setChecked(False)
            self.btnstate1()
            time.sleep(1)
            self.post2.setChecked(True)
            self.btnstate2()
            time.sleep(1)
            self.post3.setChecked(False)
            self.btnstate3()
        
    
            
        if maxposition == 2:
           # print('inside 2')
        
            self.post1.setChecked(False)
            self.btnstate1()
            time.sleep(1)

            self.post2.setChecked(False)
            self.btnstate2()
            time.sleep(1)

            self.post3.setChecked(True)
            self.btnstate3()
            

            
    def allowed(self):
       # print('############### open all gates ##############')
        
        self.post1.setChecked(False)
        self.btnstate1()
        time.sleep(1)

        self.post2.setChecked(False)
        self.btnstate2()
        time.sleep(1)

        self.post3.setChecked(False)
        self.btnstate3()
        
        #self.post1.toggle()
#        self.post1.setCheckable(True)
        
#        self.post1.clicked.connect(lambda:self.whichbtn(self.post1))
#        self.post1.clicked.connect(self.btnstate1)
        
        
        
        
    def control(self,densitylist):
        self.getmax(densitylist)
        

    def collecteddensity(self,d0,d1,d2,d3):
       # print('d0 =', d0,'d1 =',d1,'d2 =',d2,'d3 =',d3)
        ################################################
        #d0= d0-22
        global curve,data,data1,data2,data3
        
        data.append(int(d0))
        data1.append(int(d1))
        data2.append(int(d2))
        data3.append(int(d3))
        
        self.curve.setData(data)
        self.curve1.setData(data1)
        self.curve2.setData(data2)
        self.curve3.setData(data3)
        
        x0=1              
        x1=1        
        x2=1
        
        referdensity = 60
        
        densityAverage = (d0*x0)+(d1*x1)+(d3*x2)
        #print('##################### densityAverage  #####################',densityAverage)
        #print('###############d2= ',d2)
        realTimeDensity = (referdensity - d2)
        #print('current space available =',realTimeDensity)
        densitylist= [d0,d1,d3]
        
        if realTimeDensity >= 0:
           if realTimeDensity == 0:
               #print("Zero")
               self.allowed()
               
           else:
               #print("Positive number")
               self.allowed()
        else:
           #print("Negative number")
           
           self.control(densitylist)
           
        
################################### Dialog Box for whole project #########################        

    def showDialog1(self):
        Dialog = QtWidgets.QDialog()
        Dialog.setObjectName("Dialog")
        Dialog.resize(427, 418)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(50, 20, 331, 321))
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.pushButton7 = QtWidgets.QPushButton(Dialog)
        self.pushButton7.setGeometry(QtCore.QRect(170, 370, 75, 23))
        self.pushButton7.setObjectName("pushButton")
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setWindowTitle("Load Rfid Database")
        self.pushButton7.setText("Load")
        self.pushButton7.clicked.connect(self.loadData)
        Dialog.exec_()
        
        
        
    def showDialog2(self):
        Dialog1 = QtWidgets.QDialog()
        Dialog1.setObjectName("Dialog1")
        Dialog1.resize(500, 250)
        self.label10 = QtWidgets.QLabel(Dialog1)
        self.label10.setGeometry(QtCore.QRect(40, 40, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label10.setFont(font)
        self.label10.setObjectName("label10")
        self.label11 = QtWidgets.QLabel(Dialog1)
        self.label11.setGeometry(QtCore.QRect(40, 100, 131, 13))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label11.setFont(font)
        self.label11.setObjectName("label11")
        self.label12 = QtWidgets.QLabel(Dialog1)
        self.label12.setGeometry(QtCore.QRect(40, 150, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label12.setFont(font)
        self.label12.setObjectName("label12")
        self.registerbutton = QtWidgets.QPushButton(Dialog1)
        self.registerbutton.setGeometry(QtCore.QRect(200, 210, 100, 25))
        self.registerbutton.setObjectName("registerbutton")
        self.lineEdit10 = QtWidgets.QLineEdit(Dialog1)
        self.lineEdit10.setGeometry(QtCore.QRect(180, 30, 250, 30))
        self.lineEdit10.setObjectName("lineEdit10")
        self.lineEdit11 = QtWidgets.QLineEdit(Dialog1)
        self.lineEdit11.setGeometry(QtCore.QRect(180, 90, 250, 30))
        self.lineEdit11.setObjectName("lineEdit11")
        self.lineEdit12 = QtWidgets.QLineEdit(Dialog1)
        self.lineEdit12.setGeometry(QtCore.QRect(180, 150, 250, 30))
        self.lineEdit12.setObjectName("lineEdit12")
        QtCore.QMetaObject.connectSlotsByName(Dialog1)
        Dialog1.setWindowTitle("Registration Form")
        self.label10.setText("Name")
        self.label11.setText("Mobile number")
        self.label12.setText("RFID Tag number")
        self.registerbutton.setText("Register")
        self.registerbutton.clicked.connect(self.insertData)
        Dialog1.exec_()



    def clearsenddata(self):
        self.SentText.clear()
        
####################################  Mysql Database function for RFID #####################################        
    def loadData(self):
        connection = sqlite3.connect('RFID.db')
        query = "SELECT * FROM USERS"
        result = connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number , row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
        connection.close()


    def insertData(self):
        name = self.lineEdit10.text()
        mobilenumber = self.lineEdit11.text()
        rfidnumber = self.lineEdit12.text()

        connection  = sqlite3.connect("RFID.db")
        connection.execute("INSERT INTO USERS VALUES(?,?,?)",(name,mobilenumber,rfidnumber))
        connection.commit()
        connection.close()
        QMessageBox.about(self, "Registration", "Registration Successful")
        self.lineEdit10.clear()
        self.lineEdit11.clear()
        self.lineEdit12.clear()

######################## RFID Authentication and access to post ################################

    def parsingctrl(self):
       
        totaldata = ''.join(alist)
        print('totaldata =',totaldata)
        commandnumber = totaldata
        self.post1.setCheckable(True)
        if commandnumber.startswith("*a*"):
            print("Rfid from Post A")
            adata = commandnumber.strip("*a*#")
            print('Rfid number =',adata)
          
            checkaccess = self.checkdatabase(adata)
            print('access result =',checkaccess)
            if checkaccess == True:
                print('self.post1.isChecked =',self.post1.isChecked())
                self.post1.toggle()
                self.btnstate1()
                
                



        elif commandnumber.startswith("*b*"):
            print("Rfid from Post B")
            adata = commandnumber.strip("*b*#")
            print('Rfid number =',adata)
            
            checkaccess = self.checkdatabase(adata)
            print('access result =',checkaccess)
            if checkaccess == True:
                print('self.post2.isChecked =',self.post2.isChecked())
                self.post2.toggle()
                self.btnstate2()
                
                    


        elif commandnumber.startswith("*c*"):
            print("Rfid from Post C")
            adata = commandnumber.strip("*c*#")
            print('Rfid number =',adata)
            
            
            checkaccess = self.checkdatabase(adata)
            print('access result =',checkaccess)
            if checkaccess == True:
                print('self.post3.isChecked =',self.post3.isChecked())
                self.post3.toggle()
                self.btnstate3()
                
                    

                                

        elif commandnumber.startswith("*d*"):
            print("Rfid from Post D")
            adata = commandnumber.strip("*d*#")
            print('Rfid number =',adata)
            
            checkaccess = self.checkdatabase(adata)
            print('access result =',checkaccess)
            if checkaccess == True:
                print('self.post4.isChecked =',self.post4.isChecked())
                self.post4.toggle()
                self.btnstate4()
                
                    

            

    def checkdatabase(self,rfidnumber):
        print("Inside check database RFID =",rfidnumber)
        connection = sqlite3.connect("RFID.db")
        result = connection.execute("SELECT * FROM USERS WHERE rfidnumber = ?",[str(rfidnumber)])
        if(len(result.fetchall()) > 0):
            print("User Found allowing to access the post! ")
            #QMessageBox.about(self, "Warning", "User Found allowing to access the post!")
            access = True
        else:
            print("User Not Found !")
            #QMessageBox.about(self, "Warning", "Invalid Rfid number")
            access = False
        connection.close()
        return access
        
        
#################################### Serial communication function #########################   
        
    def __display_recv_data__(self,data):
        #for l in range(len(data)):
        #   hexstr = "%02X " % ord(str(data[l]))
        #  self.ReceivedText.insertPlainText(hexstr)
        self.ReceivedText.insertPlainText(data)
        #print("gogog",len(data))

        
        global alist
        for character in data:
            if character != " " :
                if character != '\n':
                    if character !=  '\r':
                        alist.append(data)
                        
            if character == '\n' :
                print('alist =', alist)
                dataUpdate = alist
                self.parsingctrl()
                print('dataUpdate =',dataUpdate)
                alist.clear()
                print('alist =', alist)
  
                break
        

                

        for l in range(len(data)):
            #self.ReceivedText.insertPlainText(data[l])  
            sb = self.ReceivedText.verticalScrollBar()
            sb.setValue(sb.maximum())
           # print("test recive", data[l])






            
    def __data_received__(self,data):
        print('recv:%s' % data)
        self.receiveSignal.emit(data)

        
        
    def __open_serial_port__(self):
        print("I am here")
        if  self._serial_context_.isRunning():
            print("lets see")
            self._serial_context_.close()
            self.OpenButton.setText(u'open')
            print("open")
        else:
            try:
                
                #currentIndex() will get the number
                portss = self.BoxPort.currentText()
                port = self.BoxPort.currentText()
                print("the", portss)
                baud = int("%s" % self.BoxBaud.currentText(),10)
                self._serial_context_ = serialportcontext.SerialPortContext(port = port,baud = baud)
                #print(self._serial_context_ )
                self._serial_context_ .recall()
                self._serial_context_.registerReceivedCallback(self.__data_received__)
                
                print("4")
                self._serial_context_.open()
                print("5")
                self.OpenButton.setText(u'close')
            except Exception as e:
                print("error")
    
    def __send_data__(self):
        data = str(self.SentText.toPlainText()+'\n')
        #print("i m data", data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)
                print(data)
                
################################### Button state ###########################################               
    def whichbtn(self,b):
      print ("clicked button is "+b.text())

    def btnstate1(self):
      if self.post1.isChecked():
         #print ("button pressed post 1")
         self.post1.setStyleSheet('background-color: red') 
         self.label21.setStyleSheet('background-color: red')
         self.label21.setAlignment(QtCore.Qt.AlignCenter)
         font = QtGui.QFont()
         font.setPointSize(18)
         self.label21.setText("Stop") 
         self.sendpost1()
      else:
          self.post1.setStyleSheet('background-color: green')
          self.label21.setStyleSheet('background-color: green')
          self.label21.setAlignment(QtCore.Qt.AlignCenter)
          font = QtGui.QFont()
          font.setPointSize(18)
          self.label21.setText("Go")
#          self.groupBox21.setStyleSheet('background-color: green')       
          self.sendpost10()
          #print ("button release - post 1")
          
          
    def btnstate2(self):
        if self.post2.isChecked():
            #print("button pressed post2")
            self.post2.setStyleSheet('background-color: red')     
            self.label22.setStyleSheet('background-color: red')
            self.label22.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(18)
            self.label22.setText("Stop")
            self.sendpost2()
            
        else:
            self.post2.setStyleSheet('background-color: green')
            self.label22.setStyleSheet('background-color: green')
            self.label22.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(18)
            self.label22.setText("Go") 
            self.sendpost20()
            #print ("button release - post 2")
            
            
    def btnstate3(self):
        if self.post3.isChecked():
            #print("button pressed post3")
            self.post3.setStyleSheet('background-color: red')   
            self.label23.setStyleSheet('background-color: red')
            self.label23.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(18)
            self.label23.setText("Stop")
            self.sendpost3()
        else:
            self.post3.setStyleSheet('background-color: green')
            self.label23.setStyleSheet('background-color: green')
            self.label23.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(18)
            self.label23.setText("Go") 
            self.sendpost30()
            #print ("button release - post 3")


    def btnstate4(self):
        if self.post4.isChecked():
            #print("button pressed post4")
            self.post4.setStyleSheet('background-color: red') 
            self.label24.setStyleSheet('background-color: red')
            self.label24.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(18)
            self.label24.setText("Stop")
            self.sendpost4()
        else:
            self.post4.setStyleSheet('background-color: green')
            self.label24.setStyleSheet('background-color: green')
            self.label24.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(18)
            self.label24.setText("Go") 
            self.sendpost40()
            #print ("button release - post 4")
        
        
        

############################ Post control ###########################################                
    def sendpost1(self):
        data = str('*2*closep1#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)


    def sendpost10(self):
        data = str('*1*openp1#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)

    
    def sendpost2(self):
        data = str('*4*closep2#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)    
                

    def sendpost20(self):
        data = str('*3*openp2#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)  
        
    def sendpost3(self):
        data = str('*6*closep3#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0)     
                
                
        
    def sendpost30(self):
        data = str('*5*openp3#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0) 
                

    def sendpost4(self):
        data = str('*8*closep4#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0) 
                
    def sendpost40(self):
        data = str('*7*openp4#'+'\n')
        self.SentText.insertPlainText(data)
        print (data)
        if self._serial_context_.isRunning():
            if len(data) > 0:
                self._serial_context_.send(data, 0) 
    


 
                
                
                
                
                
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = App()
    player.show()

   
    sys.exit(app.exec_())


    
    






