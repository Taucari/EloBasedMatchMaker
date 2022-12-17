from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from ComputeControlsWidget import ComputeControlsWidget
from ComputeOutputWidget import ComputeOutputWidget
from ComputePlayerTableWidget import ComputePlayerTableWidget

class MainWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.input_table = ComputePlayerTableWidget()
        self.control = ComputeControlsWidget()
        self.output = ComputeOutputWidget()
        
        layout = qtw.QHBoxLayout()
        layout.addWidget(self.input_table)
        layout.addWidget(self.control)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.input_table.submitted.connect(self.table_changed)
        self.control.submitted_text.connect(self.compute_finished)

        
    @qtc.pyqtSlot(list)
    def table_changed(self, new_table):
        # Passes table changes to control
        self.control.data = new_table
        self.output.inputPlayerData = new_table
    
    @qtc.pyqtSlot(int, int, list)
    def compute_finished(self, computeMode, randomSize, data):
        self.output.computeMode = computeMode
        self.output.randomSize = randomSize
        self.output.outputData = data







if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = MainWidget()
    widget.show()

    app.exec_()