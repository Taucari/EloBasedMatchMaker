from ui.ComputePlayerTable import Ui_Form
from editTableDialog import editTableDialog

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

import json

class ComputePlayerTableWidget(qtw.QWidget):

    submitted = qtc.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tabledata = [['', 0]]
        self._rowCount = len(self._tabledata)

        self.CPT_ui = Ui_Form()
        self.CPT_ui.setupUi(self)

        self.CPT_ui.playerDisplay_tableWidget.setRowCount(self._rowCount)
        
        self.CPT_ui.save_pushButton.clicked.connect(self.file_save)
        self.CPT_ui.load_pushButton.clicked.connect(self.file_open)

        self.CPT_ui.editPlayers_pushButton.clicked.connect(self.editPlayerTable)

        self.populateTable(self._tabledata)
        self.on_submit()
    
    @property
    def tableData(self):
        return self._tabledata
    
    @tableData.setter
    def tableData(self, tableData):
        if not isinstance(tableData, list):
            raise TypeError(f'Must be a list of lists. Instead, the 1 dimension is a {type(tableData)}')
        for row in tableData:
            if not isinstance(row, list):
                raise TypeError(f'Each row must be a list.Instead, the 1 dimension is a {type(row)}')
            if len(row) != 2:
                raise TypeError(f'TypeError: This table has two columns and therefore each row can only have two items, this row is {len(row)} items long.')
            if not isinstance(row[0], str):
                raise TypeError(f'Item in the Name Column must be a string. Instead it is {row[0]}, which is a {type(row[0])}')
            if not isinstance(row[1], int):
                raise TypeError(f'Item in the Elo Column must be an int. Instead it is {row[1]}, which is a {type(row[1])}')
        self._tabledata = tableData
        self._rowCount = len(tableData)
        self.CPT_ui.playerDisplay_tableWidget.setRowCount(self._rowCount)
        self.populateTable(self._tabledata)
    
    def populateTable(self, data):
        if data == [[]]:
            self.CPT_ui.playerDisplay_tableWidget.clearContents()
            while (self.CPT_ui.playerDisplay_tableWidget.rowCount() > 0):
                self.CPT_ui.playerDisplay_tableWidget.removeRow(0)
            self.CPT_ui.playerDisplay_tableWidget.setRowCount(0)
        else:
            self.CPT_ui.playerDisplay_tableWidget.setRowCount(len(data))
            for rowIndex in range(len(data)):
                self.CPT_ui.playerDisplay_tableWidget.setItem(rowIndex, 0, qtw.QTableWidgetItem(str(data[rowIndex][0])))
                self.CPT_ui.playerDisplay_tableWidget.setItem(rowIndex, 1, qtw.QTableWidgetItem(str(data[rowIndex][1])))
            
    
    def file_save(self):
        dialog = qtw.QFileDialog
        name, _ = dialog.getSaveFileName(self, 'Save File', filter="JSON Files (*.json)")
        if name:
            text = {'type': 'input', 'table_data': {item[0]: item[1] for item in self._tabledata}}
            with open(name, "w") as outfile:
                json.dump(text, outfile)
    
    def file_open(self):
        dialog = qtw.QFileDialog
        name, _ = dialog.getOpenFileName(self, 'Open File', filter="JSON Files (*.json)")
        if name.endswith('.json'):
            with open(name, 'r') as file:
                data = json.load(file)
                if data['type'] == 'input':
                    self._tabledata = [[player, elo] for player, elo in data['table_data'].items()]
                    self.populateTable(self._tabledata)
                    self.on_submit()
        
    def editPlayerTable(self):
        self.dialog = editTableDialog(table_data=self._tabledata)
        if self.dialog.exec():
            self._tabledata = self.dialog._tableData
            self.populateTable(self._tabledata)
            self.on_submit()
        self.dialog.close()
    
    def on_submit(self):
        self.submitted.emit(self._tabledata)
        

if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = ComputePlayerTableWidget()
    widget.show()

    app.exec_()