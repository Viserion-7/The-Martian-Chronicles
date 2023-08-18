import sys
import requests
import shutil
from PyQt5 import QtCore, QtWidgets, QtGui
import ezgmail
import os
import cred

os.makedirs('img',exist_ok=True)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Martian Chronicles")
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("1.jpg")
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.setCentralWidget(label)
        self.setMinimumSize(1,1)
        
        font = QtGui.QFont()
        font.setPointSize(20)

        text_1 = QtWidgets.QLabel(" Rover ", self)
        text_1.setGeometry(QtCore.QRect(1380, 340, 150, 40))
        text_1.setFont(font)
        text_1.setStyleSheet("color: White;")

        self.Rover = QtWidgets.QComboBox(self)
        self.Rover.setGeometry(QtCore.QRect(1540, 340, 200, 40))
        self.Rover.addItems(["Curiosity", "Opportunity", "Spirit"])

        text_2 = QtWidgets.QLabel(" Solar Year", self)
        text_2.setGeometry(QtCore.QRect(1380, 400, 150, 40))
        text_2.setFont(font)
        text_2.setStyleSheet("color: White;")

        self.Sol = QtWidgets.QLineEdit(self)
        self.Sol.setGeometry(QtCore.QRect(1540, 400, 200, 40))

        text_3 = QtWidgets.QLabel(" Camera ", self)
        text_3.setGeometry(QtCore.QRect(1380, 460, 150, 40))
        text_3.setFont(font)
        text_3.setStyleSheet("color: White;")
        
        self.Rover_cam = QtWidgets.QComboBox(self)
        self.Rover_cam.setGeometry(QtCore.QRect(1540, 460, 200, 40))
        self.Rover_cam.addItems(["FHAZ","RHAZ","MAST","CHEMCAM","MAHLI","MARDI","NAVCAM","PANCAM","MINITES"])

        text_4 = QtWidgets.QLabel(" Earth Date", self)
        text_4.setGeometry(QtCore.QRect(1380, 520, 150, 40))
        text_4.setFont(font)
        text_4.setStyleSheet("color: White;")

        self.Earth_Date = QtWidgets.QLineEdit(self)
        self.Earth_Date.setGeometry(QtCore.QRect(1540, 520, 200, 40))
        self.Earth_Date.setText("yyyy-m-d")
        
        fetchButton=QtWidgets.QPushButton('Fetch',self)
        fetchButton.setGeometry(QtCore.QRect(1500,570,120,40))
        
        fetchButton.setStyleSheet("""
        background-color: rgba(255,255,255,0);
        color: white;
        font-size: 25px;
        border-radius: 5px;
        border: 2px solid #EC2D01;
        """)
        fetchButton.clicked.connect(self.fetchData)

    def fetchData(self):
        print("\nFetching Data")
        rover = self.Rover.currentText()
        sol = self.Sol.text()
        camera = self.Rover_cam.currentText()
        date = self.Earth_Date.text()

        if not rover:
            rover="curiosity"
        if not sol:
            sol="1000"
        if not camera:
            camera="fhaz"
        if date == 'yyyy-m-d':
            date="2015-6-3"

        urldata=requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover.lower()}/photos?sol={sol}&camera={camera.lower()}&earth_date={date}&api_key={cred.apitoken}")
        data=urldata.json()
        photo=data['photos']
        images=[]
        print("\nUser input:", rover,sol,camera,date)
        print("\nNumber of photos = ",len(photo))
        print()
        c=1
        for i in range(len(photo)):
            image_url=photo[i]['img_src']
            with open(f"img/image{i}.jpg","wb") as f:
                resp=requests.get(image_url,stream=True)
                shutil.copyfileobj(resp.raw,f)
                images.append(f"img/image{i}.jpg")
                print("URL of image :\n ",image_url)
                print("Downloaded Image successfully")
                print()
            if c==20:
                break
            c+=1

        self.image_window = ImageWindow(images)
        self.image_window.setGeometry(QtCore.QRect(300, 100, 600, 400))
        self.image_window.show()

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
        num.setGeometry(QtCore.QRect(160, 350, 150, 40))
        num.setStyleSheet("font-size: 15px;background-color: white;")
        num.setAlignment(QtCore.Qt.AlignCenter)

        share_button = QtWidgets.QPushButton('Share', self)
        share_button.setGeometry(QtCore.QRect(350, 350, 100, 40))
        share_button.clicked.connect(self.share_image)

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

    def share_image(self):
        email_dialog = EmailInputDialog(self.images)
        email_dialog.exec_()

class EmailInputDialog(QtWidgets.QDialog,):
    def __init__(self, images):
        super().__init__()
        print("Sending Mail")
        self.images = images
        self.setWindowTitle("Send Email")

        self.email_label = QtWidgets.QLabel("Email:", self)
        self.email_label.setGeometry(QtCore.QRect(18, 20, 50, 20))

        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setGeometry(QtCore.QRect(80, 20, 200, 20))
        
        self.subject_label = QtWidgets.QLabel("Subject:", self)
        self.subject_label.setGeometry(QtCore.QRect(18, 60, 50, 20))

        self.subject_input = QtWidgets.QLineEdit(self)
        self.subject_input.setGeometry(QtCore.QRect(80, 60, 200, 20))
        self.subject_input.setText("Nasa Martian Rover Images")

        self.message_label = QtWidgets.QLabel("Message:", self)
        self.message_label.setGeometry(QtCore.QRect(18, 100, 50, 20))

        self.message_input = QtWidgets.QTextEdit(self)
        self.message_input.setGeometry(QtCore.QRect(80, 100, 200, 120))
        self.message_input.setText("Hello Mars!!")

        self.send_button = QtWidgets.QPushButton("Send", self)
        self.send_button.setGeometry(QtCore.QRect(80, 240, 70, 30))
        self.send_button.clicked.connect(self.send_email)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.setGeometry(QtCore.QRect(160, 240, 70, 30))
        self.cancel_button.clicked.connect(self.close)

    def send_email(self):
        tom = self.email_input.text().split(',')
        subject = self.subject_input.text()
        message = self.message_input.toPlainText()
        for to in tom:
            ezgmail.send(to, subject, message, attachments=self.images)

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Email sent successfully!")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        shutil.rmtree('img')
        print("Email sent successfully!")

        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
