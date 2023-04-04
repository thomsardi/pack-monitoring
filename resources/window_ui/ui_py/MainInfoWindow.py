import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from resources.window_ui.maininfowindow import Ui_MainInfoWindow

class MainInfoWindowUi(qtw.QWidget) :
    dataReady = qtc.pyqtSignal(str)
    isDatabaseConnected = qtc.pyqtSignal(bool)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.homeWindow = Ui_MainInfoWindow()
        self.homeWindow.setupUi(self)   
        self.packList : list[qtw.QPushButton] = [
            self.homeWindow.pack1,
            self.homeWindow.pack2,
            self.homeWindow.pack3,
            self.homeWindow.pack4,
            self.homeWindow.pack5,
            self.homeWindow.pack6,
            self.homeWindow.pack7,
            self.homeWindow.pack8,
        ]     
        self.statusList : list[qtw.QPushButton] = [
            self.homeWindow.packstatus1,
            self.homeWindow.packstatus2,
            self.homeWindow.packstatus3,
            self.homeWindow.packstatus4,
            self.homeWindow.packstatus5,
            self.homeWindow.packstatus6,
            self.homeWindow.packstatus7,
            self.homeWindow.packstatus8,
        ]     

if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    widget = MainInfoWindowUi()
    widget.show()
    app.exec_()