from getpass import getpass
from itertools import count
from venv import create
from mysql.connector import connect, Error
import sys
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QApplication
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap
import yaml
import cv2
import numpy as np
import os
####################################################################### MYSQL login

config_data = yaml.load(open("C:/Users/sahil/Documents/repos/mysqltest/config.yml"), Loader=yaml.FullLoader)
try:
    conn = connect(host=config_data["host"],
        user=config_data["user"],
        passwd=config_data["passwd"],
        database=config_data["db"]
    )
    if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
######################################################################


#REAL SHIT lol
###################################################################### Face recognition
class face_recog(QThread):
    
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
    
    def run(self): 

        if len(sys.argv) < 2:
            video_mode= 0
        else:
            video_mode = sys.argv[1] 

        cascasdepath = r'C:/Users/sahil/Documents/repos/mysqltest/haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascasdepath)
        video_capture = cv2.VideoCapture(video_mode)
        path = r'C:/Users/sahil/Documents/repos/mysqltest/'
        while self._run_flag:
            ret, image = video_capture.read()
            if ret:
                faces = face_cascade.detectMultiScale( #actual face recog here
                image,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (30,30)
                )
                count = 0
                
                for (x,y,w,h) in faces:
                    face = image[y:y+h, x:x+w] #slice the face from the image
                    cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)
                    if count <2:
                            cv2.imwrite(os.path.join(path, str(count)+'.jpg'), face)
                    
                
                self.change_pixmap_signal.emit(image)
        

        video_capture.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
######################################################################        

###################################################################### Main login 
class Login(QtWidgets.QWidget): #Generic account login
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(400, 200)) #lol

        self.Username = QLabel(self) #setup label
        self.Username.setText("Username: ")
        self.UserEntry = QtWidgets.QLineEdit(self)
        self.Username.move(80, 20) 
        self.Username.resize(200, 32)
        self.UserEntry.move(150, 20)

        self.Pass = QLabel(self)
        self.Pass.setText("Password: ")
        self.PassEntry = QtWidgets.QLineEdit(self)
        self.PassEntry.setEchoMode(QLineEdit.EchoMode.Password)
        self.Pass.move(80, 20)
        self.Pass.resize(200, 60)
        self.PassEntry.move(150, 40)

        login = QPushButton('Login', self)
        login.clicked.connect(self.Login)
        login.resize(210,70)
        login.move(75, 60)

        createAcc = QPushButton('Create Account', self)
        self.w = None
        createAcc.clicked.connect(self.show_new_window)
        createAcc.resize(210,70)
        createAcc.move(75, 120)

    def show_new_window(self):
        self.hide()
        if self.w is None:
            self.w = accountCreation()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.
  
    #login function     
    def Login(self):
        print("Swag2")
######################################################################
        
###################################################################### New window to create an account
class accountCreation(QWidget): #to create account, probably going to use a lot of cv2
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(400, 200)) #lol

        face_account = QPushButton("Face Recognition", self)
        self.w = None
        face_account.clicked.connect(self.show_face_recog)
        face_account.resize(210,70)
        face_account.move(75, 0)

        Exit = QPushButton('Exit', self)
        Exit.clicked.connect(self.show_new_window)
        self.Login = Login()
        Exit.resize(210,70)
        Exit.move(75, 60)

    def show_face_recog(self):
        self.hide()
        if self.w is None:
            self.w = face_recog_holder()
            self.w.show()
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def show_new_window(self):
        self.hide()
        self.Login.show()
######################################################################

###################################################################### PyQt6 window to hold cv2 face recog
class face_recog_holder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("face_recog")
        self.display_width=640
        self.display_height=480

        self.image_label=QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)

        self.allGood = QLabel(self)
        self.allGood.setText("Face found, you can exit")
        self.allGood.move(70, 0)


        Exit = QPushButton("Exit", self)
        self.w = None
        Exit.clicked.connect(self.show_accountCreation)
        Exit.resize(210,70)
        Exit.move(75, 0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(Exit)
        self.setLayout(vbox)

        self.thread = face_recog()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        

    def show_accountCreation(self):
        self.hide()
        if self.w is None:
            self.w = accountCreation()
            self.w.show()
            self.thread.stop() #so i dont get fucked wih errors
            cursor._batch_insert
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference

    def closeEvent(self, event): #so face recog actually closes on program end 
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray) #references change_pixmap_signal
    def update_image(self, image):
        qt_img = self.convert_cv_qt(image)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, image): #all of the processing happens here
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape #all of this is to convert for pyqt6 usage
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
######################################################################

#so nothing goes wrong
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Login()
    mainWin.show()
    
    sys.exit( app.exec() )
    
 