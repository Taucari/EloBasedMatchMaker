from ui.ComputeControls import Ui_Form

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from math import factorial
from random import shuffle

import numpy as np

class ComputeControlsWidget(qtw.QWidget):

    submitted_text = qtc.pyqtSignal(int, int, list)

    def __init__(self, *args, data=[['', 0]], **kwargs):
        super().__init__(*args, **kwargs)

        self._data = data
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

        self.CC_ui.compute_pushButton.clicked.connect(self.main_compute)

        #TEST LINE
        #self.CC_ui.compute_progressBar.setValue(self._currentProgressBarValue)
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        if not isinstance(data, list):
            raise TypeError(f'Must be a list of lists. Instead, the 1 dimension is a {type(data)}')
        for row in data:
            if not isinstance(row, list):
                raise TypeError(f'Each row must be a list.Instead, the 1 dimension is a {type(row)}')
            if len(row) != 2:
                raise TypeError(f'TypeError: This table has two columns and therefore each row can only have two items, this row is {len(row)} items long.')
            if not isinstance(row[0], str):
                raise TypeError(f'Item in the Name Column must be a string. Instead it is {row[0]}, which is a {type(row[0])}')
            if not isinstance(row[1], int):
                raise TypeError(f'Item in the Elo Column must be an int. Instead it is {row[1]}, which is a {type(row[1])}')
        self._data = data
        self._numberOfPlayers = len(data)
        self.CC_ui.teamSize_spinBox.setMaximum(self._numberOfPlayers)
    
    # @property
    # def numberOfPlayers(self):
    #     return self._numberOfPlayers
    
    # @numberOfPlayers.setter
    # def numberOfPlayers(self, number):
    #     if isinstance(number, int):
    #         self._numberOfPlayers = number
    #         self.CC_ui.teamSize_spinBox.setMaximum(self._numberOfPlayers)
    #     else:
    #         raise TypeError(f"Only integers are allowed when setting _NumberOfPlayers. You set {number}.")

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
        if self._currentComputeMethodIndex == 0:
            self.CC_ui.randomSize_comboBox.setEnabled(False)
        else:
            self.CC_ui.randomSize_comboBox.setEnabled(True)
    
    def randomSize_index_changed(self, randomSize_index):
        self._currentRandomSizeIndex = randomSize_index

    def change_compute_label_info(self):
        if self._numberOfPlayers % self._currentTeamSize == 0:
            numberOfTeams = int(self._numberOfPlayers/self._currentTeamSize)
            up = factorial(self._numberOfPlayers)
            down = pow(factorial(self._currentTeamSize), numberOfTeams) * factorial(numberOfTeams)
            self.CC_ui.compute_info_label.setText(f"Total number of team variants: {int(up/down)}\n ")
            self.CC_ui.compute_pushButton.setEnabled(True)
        else:
            # self.CC_ui.compute_info_label.setText(f"{self._numberOfPlayers} players do not split equally into teams of {self._currentTeamSize} players.")
            self.CC_ui.compute_info_label.setText(f"{self._numberOfPlayers} players do not split equally into teams \nof {self._currentTeamSize} players.")
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
    
    def main_compute(self):
        data = {i[0]: i[1] for i in self._data}

        if self._currentComputeMethodIndex == 0:
            team_list = self.standard_compute(data, self._currentTeamSize)
        elif self._currentComputeMethodIndex == 1 and self._currentRandomSizeIndex == 0:
            team_list = self.random_compute(data, self._currentTeamSize)
        else:
            team_list = self.n_compute(data, self._currentTeamSize)

        self.submitted_text.emit(self._currentComputeMethodIndex, self._currentRandomSizeIndex, team_list)
    
    def standard_compute(self, data, team_size):
        return [[]]
    
    def random_compute(self, data, team_size):
        index = [*range(len(data))]
        shuffle(index)
        casted = self.cast_teams(index, team_size)
        return casted
    
    def n_compute(self, data, team_size):

        def replace_dict_keys_with_incremental_value(data):
            new = {}
            current = 0
            for values in data.values():
                new[current] = values
                current += 1
            return new


        def np_calculate_iteration_mean_and_stdev(iteration):
            # Needs to Calculate Stdev for each iteration, e.g.:
            # [[1108 1220 1231 1231]
            #  [1266 1273 1285 1349]
            #  [1358 1362 1519 1621]
            #  [1467 1543 1647 1851]]
            return np.std(np.apply_along_axis(np.sum, 1, iteration))

        length = self._numberOfPlayers
        repetition = pow(10, self._currentRandomSizeIndex)

        stuff = np.tile(np.arange(length), (repetition, 1))
        rng = np.random.default_rng()
        temp = rng.permuted(stuff, axis=1, out=stuff)

        output = np.reshape(temp, (repetition, int(length / team_size), team_size))
        np.ascontiguousarray(output, dtype=np.ubyte)
        redone = np.sort(output, kind='heapsort')
        order = redone[:, :, 0].argsort()
        rearranged = np.take_along_axis(redone, order[:, :, None], axis=1)

        unique = np.unique(rearranged, axis=0)

        remapper = replace_dict_keys_with_incremental_value(data)

        remapped = np.vectorize(remapper.__getitem__)(unique)

        stds = np.empty(len(remapped))
        for i in range(len(remapped)):
            iteration = remapped[i]
            stds[i] = np_calculate_iteration_mean_and_stdev(iteration)

        calculated = np.argmin(stds)
        return unique[calculated].tolist()

    def cast_teams(self, index, team_size):
        return [index[i:i + team_size] for i in range(0, len(index), team_size)]



    

if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = ComputeControlsWidget(data = [['Player 1', 0], ['Player 2', 0], ['Player 3', 0], ['Player 4', 0], ['Player 5', 0], ['Player 6', 0]])
    widget.show()

    app.exec_()