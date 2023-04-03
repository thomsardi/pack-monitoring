import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from resources.window_ui.mainwindowtest import Ui_MainWindowTest

class MainWindowTest(qtw.QMainWindow) :
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.homeWindow = Ui_MainWindowTest()
        self.homeWindow.setupUi(self)     

if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    widget = MainWindowTest()
    widget.show()
    app.exec_()