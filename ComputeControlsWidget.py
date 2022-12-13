from ui.ComputeControls import Ui_Form

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from math import factorial

class ComputeControlsWidget(qtw.QWidget):
    def __init__(self, *args, data={'Player 1': 0}, **kwargs):
        super().__init__(*args, **kwargs)

        self._numberOfPlayers = len(data)
        self._currentTeamSize = 1
        self._currentComputeMethodIndex = 0
        self._computeMethods = {'Brute Force': 0, 'Random': 1}
        self._currentRandomSizeIndex = 0
        self._randomSizes = {f'{pow(10, v):,}' : v for v in range(10)}
        self._currentProgressBarValue = 0

        self.CC_ui = Ui_Form()
        self.CC_ui.setupUi(self)

        self.CC_ui.computeMethod_comboBox.addItems([*self._computeMethods.keys()])
        self.CC_ui.computeMethod_comboBox.currentIndexChanged.connect(self.compute_index_changed)

        self.CC_ui.randomSize_comboBox.addItems([*self._randomSizes.keys()])
        self.CC_ui.randomSize_comboBox.currentIndexChanged.connect(self.randomSize_index_changed)
        self.CC_ui.randomSize_comboBox.setEnabled(False)

        self.CC_ui.teamSize_spinBox.setMaximum(self._numberOfPlayers)
        self.CC_ui.teamSize_spinBox.valueChanged.connect(self.team_size_changed)

        self.change_compute_label_info()

        self.CC_ui.compute_pushButton.clicked.connect(self.increaseProgressBarTest)

        #TEST LINE
        self.CC_ui.compute_progressBar.setValue(self._currentProgressBarValue)
    
    @property
    def numberOfPlayers(self):
        return self._numberOfPlayers
    
    @numberOfPlayers.setter
    def numberOfPlayers(self, number):
        if isinstance(number, int):
            self._numberOfPlayers = number
            self.CC_ui.teamSize_spinBox.setMaximum(self._numberOfPlayers)
        else:
            raise TypeError(f"Only integers are allowed when setting _NumberOfPlayers. You set {number}.")

    @property
    def getTeamSize(self):
        return self._currentTeamSize
    
    @property
    def getComputeMethodIndex(self):
        return self._currentComputeMethodIndex

    @property
    def getRandomSizeIndex(self):
        return self._currentRandomSizeIndex
    
    @property
    def currentProgressBarValue(self):
        return self._currentProgressBarValue
    
    @currentProgressBarValue.setter
    def currentProgressBarValue(self, number):
        if not isinstance(number, int):
            raise TypeError(f"Only integers are allowed when setting _currentProgressBarValue. You set {number}.")
        elif number not in range(0, 101, 1):
            raise ValueError(f"Only value between 0 and 100 are allowed when setting _currentProgressBarValue. You set {number}.")
        else:
            self._currentProgressBarValue = number
            self.CC_ui.compute_progressBar.setValue(self._currentProgressBarValue)
    
    def team_size_changed(self, new_teamSize):
        self._currentTeamSize = new_teamSize
        self.change_compute_label_info()
    
    def compute_index_changed(self, compute_index):
        self._currentComputeMethodIndex = compute_index
        print(self._currentComputeMethodIndex)
        if self._currentComputeMethodIndex == 0:
            self.CC_ui.randomSize_comboBox.setEnabled(False)
        else:
            self.CC_ui.randomSize_comboBox.setEnabled(True)
    
    def randomSize_index_changed(self, randomSize_index):
        self._currentRandomSizeIndex = randomSize_index
        print(self._currentRandomSizeIndex)

    def change_compute_label_info(self):
        if self._numberOfPlayers % self._currentTeamSize == 0:
            numberOfTeams = int(self._numberOfPlayers/self._currentTeamSize)
            up = factorial(self._numberOfPlayers)
            down = pow(factorial(self._currentTeamSize), numberOfTeams) * factorial(numberOfTeams)
            self.CC_ui.compute_info_label.setText(f"Total number of team variants: {int(up/down)}\n ")
            self.CC_ui.compute_pushButton.setEnabled(True)
        else:
            # self.CC_ui.compute_info_label.setText(f"{self._numberOfPlayers} players do not split equally into teams of {self._currentTeamSize} players.")
            self.CC_ui.compute_info_label.setText(f"{self._numberOfPlayers} players do not split equally into \nteams of {self._currentTeamSize} players.")
            self.CC_ui.compute_pushButton.setEnabled(False)
    
    def increaseProgressBarTest(self):
        """TEST FUNCTION"""
        current_value = self._currentProgressBarValue
        if current_value >= 100:
            new_value = current_value
        else:
            new_value = current_value + 10
        self._currentProgressBarValue = new_value
        self.CC_ui.compute_progressBar.setValue(self._currentProgressBarValue)


if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = ComputeControlsWidget(data = {'Player 1': 0, 'Player 2': 0, 'Player 3': 0, 'Player 4': 0, 'Player 5': 0, 'Player 6': 0})
    widget.show()

    app.exec_()