from ui.editTable import Ui_editTable_Dialog

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class editTableDialog(qtw.QDialog):
    def __init__(self, *args, table_data = [[]], **kwargs):
        super().__init__(*args, **kwargs)

        self._tableData = table_data

        self.ETD_ui = Ui_editTable_Dialog()
        self.ETD_ui.setupUi(self)

        if len(table_data) == 1 and table_data[0] == []:
            self._rowCount = 0
        else:
            self._rowCount = len(table_data)
            self.updateTable()

        self.ETD_ui.addRow_pushButton.clicked.connect(self.addRow)
        self.ETD_ui.deleteRow_pushButton_2.clicked.connect(self.deleteRow)
        self.ETD_ui.clearTable_pushButton.clicked.connect(self.clearTable)
        self.ETD_ui.tableWidget.itemChanged.connect(self.updateTableData)

    
    def addRow(self):
        self.ETD_ui.tableWidget.insertRow(self.ETD_ui.tableWidget.currentRow() + 1)
        self._rowCount = self.ETD_ui.tableWidget.rowCount()
        self.updateTableData()

    def deleteRow(self):
        self.ETD_ui.tableWidget.removeRow(self.ETD_ui.tableWidget.currentRow())
        self._rowCount = self.ETD_ui.tableWidget.rowCount()
        self.updateTableData()

    def clearTable(self):
        self._tableData = [[]]
        self._rowCount = 0
        self.ETD_ui.tableWidget.clearContents()
        while (self.ETD_ui.tableWidget.rowCount() > 0):
            self.ETD_ui.tableWidget.removeRow(0)
        self.ETD_ui.tableWidget.setRowCount(self._rowCount)
    
    def updateTable(self):
        self.ETD_ui.tableWidget.setRowCount(self._rowCount)
        self.populateTable(self._tableData)

    def updateTableData(self):
        data = []
        for rowIndex in range(self.ETD_ui.tableWidget.rowCount()):
            if self.ETD_ui.tableWidget.item(rowIndex, 0) is None:
                name = ''
            else:
                name = name = self.ETD_ui.tableWidget.item(rowIndex, 0).text()
            
            if self.ETD_ui.tableWidget.item(rowIndex, 1) is None:
                elo = 0
            else:
                elo = int(self.ETD_ui.tableWidget.item(rowIndex, 1).text())
            
            row_data = [name, elo]
            data.append(row_data)
        self._tableData = data

    def populateTable(self, data):
        self.ETD_ui.tableWidget.setRowCount(len(data))
        for rowIndex in range(len(data)):
            self.ETD_ui.tableWidget.setItem(rowIndex, 0, qtw.QTableWidgetItem(str(data[rowIndex][0])))
            self.ETD_ui.tableWidget.setItem(rowIndex, 1, qtw.QTableWidgetItem(str(data[rowIndex][1])))

if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = editTableDialog(table_data=[['The Crow#9228', 1108], 
            ['Rev Baby <3 #6306', 1220], 
            ['Emili0#6796', 1231], 
            ['cpjh#4088', 1231], 
            ['Homie1kanobi#4490', 1266], 
            ['Awwtistic Saint#2313', 1273], 
            ['Rinzler42#2021', 1285], 
            ['ImJarenWard TTV#4813', 1349], 
            ['starrytittysprinkles#2716', 1358], 
            ['SinisteRock #8632', 1362], 
            ['thursday#8038', 1467], 
            ['Kandoo026#0905', 1519], 
            ['kuroneko#1765', 1543], 
            ['icemount#3566', 1621], 
            ['Ghostloki#2424', 1647], 
            ['Moira#4231', 1851]])
    widget.show()

    app.exec_()