import sys
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QApplication,QMainWindow
from Ui4 import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)


        self.uic.Button_Submit.clicked.connect(self.Submit_Arg)
        self.uic.Button_Line.clicked.connect(self.Create_Line)
        self.uic.Button_Signal.clicked.connect(self.Detect_Signal)
        self.uic.Button_FirstFrame.clicked.connect(self.First_Frame)
        self.uic.Button_Finish.clicked.connect(self.Finish_Setting)
        self.uic.Button_StartVideo.clicked.connect(self.Start_Video)
        self.uic.Button_StopVideo.clicked.connect(self.Stop_Video)

        self.thread = {}
    def Submit_Arg(self):
        pass


    def Create_Line(self):
        pass

    def Detect_Signal(self):
        pass

    def First_Frame(self):
        pass

    def Finish_Setting(self):
        pass



    def closeEvent(self, event):
        self.Stop_Video()

    def Stop_Video(self):
        self.thread[1].stop()

    def Start_Video(self):
        self.thread[1] = capture_video(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.Video_2.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(capture_video, self).__init__()

    def run(self):
        cap = cv2.VideoCapture('C:/Users/anhlo/Downloads/video-1648283099.mp4')  # 'D:/8.Record video/My Video.mp4'
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.signal.emit(cv_img)
    def stop(self):
        print("stop threading", self.index)
        self.terminate()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())