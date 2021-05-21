import cv2 as cv
import numpy as np
import argparse
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap
from numpy.core.numeric import normalize_axis_tuple
from PIL import Image
import os

capture = cv.VideoCapture(0)    #Initialize camera capture

class Window(QWidget):          #Application window

    def __init__(self):

        QWidget.__init__(self)
        self.capture = cv.VideoCapture(0)

        #Initialize RGB color boundry values
        self.rl = 0
        self.ru = 1
        self.gl = 0
        self.gu = 1
        self.bl = 0
        self.bu = 1

        #Initialize color vs normal screenshot flag
        self.flag = 0
        
        #Build slider objects for RGB color boundries
        #First letter denotes color (r, g, b)
        #Second letter denotes upper or lower boundry (u, l)
        self.rl_slider = QSlider(Qt.Orientation(1))
        self.rl_slider.setRange(0, 255)
        self.rl_slider.setTickPosition(QSlider.TickPosition(2))
        self.rl_slider.valueChanged[int].connect(self.changeValue_rl)
        self.ru_slider = QSlider(Qt.Orientation(1))
        self.ru_slider.setRange(0, 255)
        self.ru_slider.setTickPosition(QSlider.TickPosition(2))
        self.ru_slider.valueChanged[int].connect(self.changeValue_ru)
        self.gl_slider = QSlider(Qt.Orientation(1))
        self.gl_slider.setRange(0, 255)
        self.gl_slider.setTickPosition(QSlider.TickPosition(2))
        self.gl_slider.valueChanged[int].connect(self.changeValue_gl)
        self.gu_slider = QSlider(Qt.Orientation(1))
        self.gu_slider.setRange(0, 255)
        self.gu_slider.setTickPosition(QSlider.TickPosition(2))
        self.gu_slider.valueChanged[int].connect(self.changeValue_gu)
        self.bl_slider = QSlider(Qt.Orientation(1))
        self.bl_slider.setRange(0, 255)
        self.bl_slider.setTickPosition(QSlider.TickPosition(2))
        self.bl_slider.valueChanged[int].connect(self.changeValue_bl)
        self.bu_slider = QSlider(Qt.Orientation(1))
        self.bu_slider.setRange(0, 255)
        self.bu_slider.setTickPosition(QSlider.TickPosition(2))
        self.bu_slider.valueChanged[int].connect(self.changeValue_bu)

        #Construct buttons
        startcambutton = QPushButton()                                                              #Starts camera feed in new window
        startcambutton.setText("Start Camera")
        startcambutton.clicked.connect(lambda: self.startcam())
        norm_sc_button = QPushButton()                                                              #Takes a normal screenshot of camera feed
        norm_sc_button.setText("Take a Normal Screenshot")
        norm_sc_button.clicked.connect(lambda: self.screenshot())
        color_sc_button = QPushButton()                                                             #Takes a color-parsed screenshot of camera feed
        color_sc_button.setText("Take a Color-Parsed Screenshot")
        color_sc_button.clicked.connect(lambda: self.getcolor())
        disp_norm_sc_button = QPushButton()                                                         #Displays the last normal screenshot taken inside main window
        disp_norm_sc_button.setText("Display Normal Screenshot")
        disp_norm_sc_button.clicked.connect(lambda: self.dispscreenshot("norm_screenshot.png"))
        disp_color_sc_button = QPushButton()                                                        #Displays the last color-parsed screenshot taken inside main window
        disp_color_sc_button.setText("Display Color-Parsed Screenshot")
        disp_color_sc_button.clicked.connect(lambda: self.dispscreenshot("color_screenshot.png"))
        save_sc_button = QPushButton()                                                              #Saves the screenshot currently displayed in main window
        save_sc_button.setText("Save Current Screenshot")
        save_sc_button.clicked.connect(lambda: self.savescreenshot())
        
        #Initialize and build QFormLayout object to organize main window
        self.flo = QFormLayout()
        self.flo.addRow("", startcambutton)
        self.flo.addRow("", norm_sc_button)
        self.flo.addRow("Red Lower Limit", self.rl_slider)
        self.flo.addRow("Red Upper Limit", self.ru_slider)
        self.flo.addRow("Green Lower Limit", self.gl_slider)
        self.flo.addRow("Green Upper Limit", self.gu_slider)
        self.flo.addRow("Blue Lower Limit", self.bl_slider)
        self.flo.addRow("Blue Upper Limit", self.bu_slider)
        self.flo.addRow("", color_sc_button)
        self.flo.addRow("", disp_norm_sc_button)
        self.flo.addRow("", disp_color_sc_button)
        self.flo.addRow("", save_sc_button)
        self.flo.setVerticalSpacing(10)

        #Finalize main window
        self.setLayout(self.flo)
        self.setGeometry(50,50,700,500)
        self.setWindowTitle("Camera Interface")
        

    def changeValue_rl(self, value):
        #Called on Red Lower Limit slider change
        pre = self.rl
        self.rl = value
        if self.rl >= self.ru:                  #Ensures that lower limit slider is always < or = to upper limit slider
            self.ru += abs(self.rl - pre)
            self.ru_slider.setValue(self.ru)

    def changeValue_ru(self, value):
        #Called on Red Upper Limit slider change
        pre = self.ru
        self.ru = value
        if self.rl >= self.ru:                  #Ensures that lower limit slider is always < or = to upper limit slider
            self.rl -= abs(self.ru - pre)
            self.rl_slider.setValue(self.rl)

    def changeValue_gl(self, value):
       #Called on Green Lower Limit slider change
        pre = self.gl
        self.gl = value
        if self.gl >= self.gu:                  #Ensures that lower limit slider is always < or = to upper limit slider
            self.gu += abs(self.gl - pre)
            self.gu_slider.setValue(self.gu)

    def changeValue_gu(self, value):
        #Called on Green Upper Limit slider change
        pre = self.gu
        self.gu = value
        if self.gl >= self.gu:                  #Ensures that lower limit slider is always < or = to upper limit slider
            self.gl -= abs(self.gu - pre)
            self.gl_slider.setValue(self.gl)

    def changeValue_bl(self, value):
        #Called on Blue Lower Limit slider change
        pre = self.bl
        self.bl = value
        if self.bl >= self.bu:                  #Ensures that lower limit slider is always < or = to upper limit slider
            self.bu += abs(self.bl - pre)
            self.bu_slider.setValue(self.bu)

    def changeValue_bu(self, value):
        #Called on Blue Upper Limit slider change
        pre = self.bu
        self.bu = value
        if self.bl >= self.bu:                  #Ensures that lower limit slider is always < or = to upper limit slider
            self.bl -= abs(self.bu - pre)
            self.bl_slider.setValue(self.bl)

    def dispscreenshot(self, text):
        #Called on either display screenshot button click
        #Sends screenshot to main window
        self.flag = 0 if text == "norm_screenshot.png" else 1
        self.im = QPixmap(text)
        pic = QLabel()
        pic.setPixmap(self.im)
        self.flo.removeRow(12)
        self.flo.addRow("", pic)
        return

    def startcam(self):
        #Called on start camera buton click
        #Displays the camera feed of a camera module connected to user computer inside of another window
        #Has not been tested on computers with multiple camera modules connected
        self.capture = cv.VideoCapture(0)
        ret, frame = self.capture.read()

        x, y, w, h = 300, 200, 100, 50 
        track_window = (x, y, w, h)

        roi = frame[y:y+h, x:x+w]
        hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)
        term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 100, 100 )

        count = 0
        fnt = 0

        while True:
            count = count + 1
            ret, frame = self.capture.read()
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            ret, track_window = cv.CamShift(dst, track_window, term_crit)
            pts = cv.boxPoints(ret)
            pts = np.int0(pts)
            img2 = cv.polylines(frame,[pts],True, 255,2)
            cv.imshow('Video Feed', img2)

            if cv.waitKey(1) == 27:     #Exit on "esc"
                break

        self.capture.release()

        cv.destroyAllWindows()

    def screenshot(self):
        #Called on norm screenshot button click
        #Takes a screenshot of the current camera feed
        t = cv.imwrite('norm_screenshot.png',self.capture.read()[1])

    def getcolor(self):
        #Called on color screenshot button click
        #Takes a screenshot of the current camera feed and constructs a new image from RGB boundries given by user
        t = cv.imwrite('color_screenshot.png',self.capture.read()[1])
        image = cv.imread("Z:\Engineering\\02-Users\\nmyers\Reports and Proposals\Hydraulic Press\Python\\color_screenshot.png")
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        lower_range = np.array([self.rl,self.gl,self.bl])
        upper_range = np.array([self.ru,self.gu,self.bu])
        mask = cv.inRange(hsv, lower_range, upper_range)
        t = cv.imwrite('color_screenshot.png',mask)

    def savescreenshot(self):
        #Called on save screenshot button click
        #Saves most recent screenshot displayed on main window to user's home directory
        homeDir = os.path.expanduser("~")
        if self.flag == 0:
            pic = Image.open("Z:\Engineering\\02-Users\\nmyers\Reports and Proposals\Hydraulic Press\Python\\norm_screenshot.png")
            pic = pic.save(homeDir + "\\test.png")
        else:
            pic = Image.open("Z:\Engineering\\02-Users\\nmyers\Reports and Proposals\Hydraulic Press\Python\\color_screenshot.png")
            pic = pic.save(homeDir + "\\test2.png")

#Begin program
app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec())