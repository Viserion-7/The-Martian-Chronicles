import sys
import requests
import shutil
from PyQt5 import QtCore, QtWidgets, QtGui
import random
import os
import json
import pathlib
import time

apitoken="cGgrQ050dAIbAd2T19ysIRWzvLumwMvcmoCt2w82"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Martian Chronicles")
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("background.jpg")
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.setCentralWidget(label)
        
        font = QtGui.QFont()
        font.setPointSize(15)

        self.text_1 = QtWidgets.QLabel(" Rover ", self)
        self.text_1.setGeometry(QtCore.QRect(20, 830, 60, 40))
        self.text_1.setFont(font)
        self.text_1.setStyleSheet("background-color: SlateGray;")


        self.Rover = QtWidgets.QLineEdit(self)
        self.Rover.setGeometry(QtCore.QRect(80, 830, 200, 40))

        self.text_2 = QtWidgets.QLabel(" Solar Year", self)
        self.text_2.setGeometry(QtCore.QRect(340, 830, 100, 40))
        self.text_2.setFont(font)
        self.text_2.setStyleSheet("background-color: SlateGray;")

        self.Sol = QtWidgets.QLineEdit(self)
        self.Sol.setGeometry(QtCore.QRect(440, 830, 200, 40))

        self.text_3 = QtWidgets.QLabel(" Camera ", self)
        self.text_3.setGeometry(QtCore.QRect(670, 830, 80, 40))
        self.text_3.setFont(font)
        self.text_3.setStyleSheet("background-color: SlateGray;")
        
        self.Rover_cam = QtWidgets.QLineEdit(self)
        self.Rover_cam.setGeometry(QtCore.QRect(750, 830, 200, 40))

        self.text_4 = QtWidgets.QLabel(" Earth Date", self)
        self.text_4.setGeometry(QtCore.QRect(1000, 830, 110, 40))
        self.text_4.setFont(font)
        self.text_4.setStyleSheet("background-color: SlateGray;")

        self.Earth_Date = QtWidgets.QLineEdit(self)
        self.Earth_Date.setGeometry(QtCore.QRect(1110, 830, 200, 40))
        
        fetchButton=QtWidgets.QPushButton('Fetch',self)
        fetchButton.setGeometry(QtCore.QRect(925,900,80,40))
        fetchButton.setStyleSheet("font-size: 20px;background-color: SlateGray;")
        fetchButton.clicked.connect(self.fetchData)

    def fetchData(self):

        rover = self.Rover.text()
        sol = self.Sol.text()
        camera = self.Rover_cam.text()
        date = self.Earth_Date.text()

        if not rover:
            rover="curiosity"
        if not sol:
            sol="1000"
        if not camera:
            camera="fhaz"
        if not date:
            date="2015-6-3"

        urldata=requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&camera={camera}&eartg_date={date}&api_key=cGgrQ050dAIbAd2T19ysIRWzvLumwMvcmoCt2w82")
        data=urldata.json()
        photo=data['photos']
        images=[]
        for i in range(len(photo)):
            image_url=photo[i]['img_src']
            with open(f"image{i}.jpg","wb") as f:
                resp=requests.get(image_url,stream=True)
                shutil.copyfileobj(resp.raw,f)
                images.append(f"image{i}.jpg")
        self.image_window = ImageWindow(images)
        self.image_window.show()

        print("Fetching Data")
        print("User input:", rover,sol,camera,date)

class ImageWindow(QtWidgets.QMainWindow):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.current_image = 0

        self.setWindowTitle("Mars Images")
        self.resize(600, 400)

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 600, 400))

        self.update_image()

        next_button = QtWidgets.QPushButton('Next', self)
        next_button.setGeometry(QtCore.QRect(475, 350, 100, 40))
        next_button.clicked.connect(self.next_image)

        num = QtWidgets.QLabel('Total Images = '+str(len(images)), self)
        num.setGeometry(QtCore.QRect(200, 350, 150, 40))
        num.setStyleSheet("font-size: 15px;background-color: white;")
        num.setAlignment(QtCore.Qt.AlignCenter)

        prev_button = QtWidgets.QPushButton('Previous', self)
        prev_button.setGeometry(QtCore.QRect(25, 350, 100, 40))
        prev_button.clicked.connect(self.prev_image)

    def update_image(self):
        pixmap = QtGui.QPixmap(self.images[self.current_image])
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def next_image(self):
        if self.current_image < len(self.images) - 1:
            self.current_image += 1
        else:
            self.current_image = 0
        self.update_image()

    def prev_image(self):
        if self.current_image > 0:
            self.current_image -= 1
        else:
            self.current_image = len(self.images) - 1
        self.update_image()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
