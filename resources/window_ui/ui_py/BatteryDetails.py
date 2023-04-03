import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from resources.window_ui.batterydetails import Ui_BatteryDetails

class BatteryDetailsUi(qtw.QMainWindow) :
    dataReady = qtc.pyqtSignal(str)
    isDatabaseConnected = qtc.pyqtSignal(bool)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.ui = Ui_BatteryDetails()
        self.ui.setupUi(self)

    def updateLcd(self) :
        pass

if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    widget = BatteryDetailsUi()
    widget.show()
    app.exec_()