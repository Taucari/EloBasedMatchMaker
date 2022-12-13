import sys
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

from ui.ComputeControls import *

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Matchmaking App by Taucari')
        self.setFixedSize(qtc.QSize(400, 300))



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
