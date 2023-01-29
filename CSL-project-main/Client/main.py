from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QLineEdit,QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QObject,QThread
import sys
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QThreadPool
import numpy as np
import zmq
import base64
import numpy as np
import threading
import socket

# send socket shit
# sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sendsocket.bind(('', 12367))
#
# sendsocket.listen(5)
# c, addr = sendsocket.accept()


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.bind('tcp://*:5555')
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode_(''))
        #cap = cv2.VideoCapture(0)
        while self._run_flag:
            #ret, cv_img = cap.read()
            frame = footage_socket.recv_string()
            img = base64.b64decode(frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            cv_img = cv2.imdecode(npimg, 1)
            if cv_img is not None:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        #cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 1280
        self.display_height = 720
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')
        self.line = QLineEdit(self)
        self.line.move(720,760)
        self.line.resize(200, 32)

        pybutton = QPushButton('Send',self)
        #pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(64,23)
        pybutton.move(1000,760)
        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        self.threadpool = QThreadPool()
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def clickMethod(self):
        global c
        c.send(self.line.text().encode())

    # def closeEvent(self, event):
    #     self.thread.stop()
    #     sendsocket.close()
    #     event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())
