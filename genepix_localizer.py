
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFileDialog, QPushButton
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt

from GPSPhoto import gpsphoto
import webbrowser
import os
import sys
import time


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.fname = ""
        self.setWindowTitle("GENEPIX Geolocalisation")
        self.setGeometry(300, 300, 800, 600)
        self.main_layout = QVBoxLayout()
        self.lbl_logo = QLabel(self)
        self.lbl_logo.setPixmap(QPixmap(os.path.join("img", "genepix_localizer.png")))
        self.lbl_browsed_img = QLabel(self)
        self.lbl_browsed_img.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setStyleSheet("background-color: #222; color: #fff; font-weight: bold;")
        self.btn_browse = QPushButton("Browse photo...")
        self.btn_browse.setStyleSheet("background-color: #00f2ec; color: #222; padding: 15px; border-radius: 3px;")
        self.btn_browse.clicked.connect(self.browse)
        self.btn_search = QPushButton("Geolocaliser")
        self.btn_search.setStyleSheet("background-color: #ff074b; padding: 15px; border-radius: 3px;")
        self.btn_search.clicked.connect(self.geoloc)
        self.main_layout.addWidget(self.lbl_logo)
        self.main_layout.addWidget(self.lbl_browsed_img)
        self.main_layout.addWidget(self.btn_browse)
        self.main_layout.addWidget(self.btn_search)
        self.setLayout(self.main_layout)

    def geoloc(self):
        print(self.fname)
        if self.fname == "":
            print("Please browse for a photo first")
            return
        data = gpsphoto.getGPSData(self.fname)
        if "Latitude" not in data.keys() or "Longitude" not in data.keys():
            print(f"Couldn't get gps data from exif on this image : {self.fname}")
            return
        print(data['Latitude'], data['Longitude'])
        try:
            webbrowser.open(f"http://maps.google.com/?q={data['Latitude']},{data['Longitude']}")
        except Exception as e:
            print(f"Error while trying to open webbrowser")
            return

    def browse(self):
        file_output = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.gif)")
        if not file_output:
            return
        self.fname = file_output[0]
        browsed_img = QPixmap(self.fname).scaled(300, 300, Qt.KeepAspectRatio)
        self.lbl_browsed_img.setPixmap(browsed_img)


if __name__ == '__main__':
    myApp = QApplication()
    window = Window()
    window.show()
    myApp.exec_()
    sys.exit(0)
