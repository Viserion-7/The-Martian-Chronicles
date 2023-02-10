import sys
import requests
import random
import json
from PyQt5 import QtCore, QtWidgets, QtGui

apitoken="cGgrQ050dAIbAd2T19ysIRWzvLumwMvcmoCt2w82"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Martian Chronicles")
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("10.jpg")
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.setCentralWidget(label)

        container_widget = QtWidgets.QWidget(self)
        container_widget.setGeometry(QtCore.QRect(800, 900, 300, 80))
        container_widget.setStyleSheet("background-color: black;")

        self.Rover_cam = QtWidgets.QLineEdit(self)
        self.Rover_cam.setGeometry(QtCore.QRect(1000, 800, 100, 40))

        self.Earth_Date = QtWidgets.QLineEdit(self)
        self.Earth_Date.setGeometry(QtCore.QRect(1000, 800, 100, 40))

        fetchButton=QtWidgets.QPushButton('Fetch',self)
        fetchButton.setGeometry(QtCore.QRect(925,900,80,40))
        fetchButton.clicked.connect(self.fetchData)
        
    def fetchData(self):
        rover = self.Rover_cam.text()

        urldata=requests.get("https://api.nasa.gov/planetary/apod?api_key=cGgrQ050dAIbAd2T19ysIRWzvLumwMvcmoCt2w82")
        fields=urldata.json()

        # self.
        print("User input:",rover)

        print("Fetching Data")
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
