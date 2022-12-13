from ui.ComputeOutput import Ui_Form

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import json

class ComputeOutputWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._outputData = []
        self._outputText = ""

        self.CO_ui = Ui_Form()
        self.CO_ui.setupUi(self)

        self.CO_ui.computeOutput_plainTextEdit.setPlainText(self._outputText)

        self.CO_ui.saveOutput_pushButton.clicked.connect(self.file_save)
    
    @property
    def outputText(self):
        return self._outputText
    
    @outputText.setter
    def outputText(self, textStr):
        if isinstance(textStr, str):
            self._outputText = textStr
            self.CO_ui.computeOutput_plainTextEdit.setPlainText(self._outputText)
        else:
            raise TypeError(f"Only strings are allowed when setting _outputText. You set {textStr} which is {type(textStr)}.")
    
    @property
    def outputData(self):
        return self._outputData
    
    @outputData.setter
    def outputText(self, data):
        if isinstance(data, list):
            self._outputData = data

        else:
            raise TypeError(f"Only lists are allowed when setting _outputText. You set {data} which is {type(data)}.")
    

    # def turnDataIntoText(self):
    #     message = []
    #     for team in team_list:
    #         message.append("\n")
    #         message.append("Team " + str(team_list.index(team) + 1) + ":")
    #         team_elo = []
    #         for player in team:
    #             message.append("↳ " + str(player_names[player]))
    #             team_elo.append(data[player_names[player]])
    #         current_team_elo = sum(team_elo) / len(team_elo)
    #         message.append("= Average Team Elo: " + str(current_team_elo))
    #         global_elo.append(current_team_elo)
    #     message.append("\n")
    #     message.append("=> Group Elo: " + str(sum(global_elo) / len(global_elo)))
    #     message.append("=> Group StDev: " + str(stats.stdev(global_elo)))
    #     return '\n'.join(message)
    
    def file_save(self):
        dialog = qtw.QFileDialog
        name = dialog.getSaveFileName(self, 'Save File', filter="JSON Files (*.json)")
        if name[0]:
            text = {'type': 'output', 'data': self._outputData, 'text': self._outputText}
            with open(name[0], "w") as outfile:
                json.dump(text, outfile)

if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = ComputeOutputWidget()
    widget.show()

    app.exec_()