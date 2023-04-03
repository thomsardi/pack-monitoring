import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from resources.window_ui.homewindow import Ui_HomeWindow
from resources.window_ui.ui_py.MainInfoWindow import MainInfoWindowUi

class HomeWindowUi(qtw.QMainWindow) :
    dataReady = qtc.pyqtSignal(str)
    isDatabaseConnected = qtc.pyqtSignal(bool)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.homeWindow = Ui_HomeWindow()
        self.mainInfo = MainInfoWindowUi()
        self.homeWindow.setupUi(self)
        # self.homeWindow.tabWidget.addTab(self.mainInfo, "tab 2")

if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    widget = HomeWindowUi()
    widget.show()
    app.exec_()