from ui.ComputeOutput import Ui_Form

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import json
import statistics as stats

class ComputeOutputWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._outputData = []
        self._outputText = ""

        self._computeMode = 0
        self._randomSize = 0

        self._inputPlayerData = []

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
    def outputData(self, data):
        if isinstance(data, list):
            self._outputData = data
            self.reflectData()
        else:
            raise TypeError(f"Only lists are allowed when setting _outputText. You set {data} which is {type(data)}.")
    
    @property
    def computeMode(self):
        return self._computeMode
    
    @computeMode.setter
    def computeMode(self, computeMode):
        if isinstance(computeMode, int):
            self._computeMode = computeMode
        else:
            raise TypeError(f"Only ints are allowed when setting _computeMode. You set {computeMode} which is {type(computeMode)}.")
    
    @property
    def randomSize(self):
        return self._randomSize
    
    @randomSize.setter
    def randomSize(self, randomSize):
        if isinstance(randomSize, int):
            self._randomSize = randomSize
        else:
            raise TypeError(f"Only ints are allowed when setting _randomSize. You set {randomSize} which is {type(randomSize)}.")

    @property
    def inputPlayerData(self):
        return self._inputPlayerData
    
    @inputPlayerData.setter
    def inputPlayerData(self, players):
        if isinstance(players, list):
            self._inputPlayerData = players
        else:
            raise TypeError(f"Only lists are allowed when setting _inputPlayerData. You set {players} which is {type(players)}.")
    
    def reflectData(self):
        data = {i[0]: i[1] for i in self._inputPlayerData}

        message = []

        player_names = [*data.keys()]
        global_elo = []
        team_list = self._outputData
        if self._computeMode == 0:
            message.append("Standard Team Assignment")
        elif self._computeMode == 1 and self._randomSize == 0:
            message.append("Random Team Assignment")
        else:
            message.append(f"Best of {pow(10, self._randomSize):,} Random Team Assignments")

        for team in team_list:
            message.append("Team " + str(team_list.index(team) + 1) + ":")
            team_elo = []
            for player in team:
                message.append("↳ " + str(player_names[player]))
                team_elo.append(data[player_names[player]])
            current_team_elo = sum(team_elo) / len(team_elo)
            message.append("= Average Team Elo: " + str(current_team_elo))
            global_elo.append(current_team_elo)
        message.append("\n")
        message.append("=> Group Elo: " + str(sum(global_elo) / len(global_elo)))
        message.append("=> Group StDev: " + str(stats.stdev(global_elo)))
        final = '\n'.join(message)

        self._outputText = final
        self.CO_ui.computeOutput_plainTextEdit.setPlainText(self._outputText)

    
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