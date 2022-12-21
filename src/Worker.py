from PyQt5 import QtCore as qtc

from random import shuffle

import numpy as np

class Worker(qtc.QObject):

    computeResult = qtc.pyqtSignal(int, int, list)

    def __init__(self, data, team_size, computeMode, randomSize):
        self._data = data
        self._teamSize = team_size
        self._computeMode = computeMode
        self._randomSize = randomSize
    
    def main_compute(self):
        data = {i[0]: i[1] for i in self._data}

        if self._computeMode == 0:
            team_list = self.standard_compute(data)
        elif self._computeMode == 1 and self._randomSize == 0:
            team_list = self.random_compute(data)
        else:
            team_list = self.n_compute(data, self._teamSize, self._randomSize)

        self.computeResult.emit(self._computeMode, self._randomSize, team_list)
    
    def standard_compute(self, data):
        ret = [*range(len(data))]
        return self.cast_teams(ret, self._teamSize)
    
    def random_compute(self, data):
        index = [*range(len(data))]
        shuffle(index)
        return self.cast_teams(index, self._teamSize)
    
    def n_compute(self, data, team_size):
        length = len(self._data)
        repetition = pow(10, self._randomSize)

        stuff = np.tile(np.arange(length), (repetition, 1))
        rng = np.random.default_rng()
        temp = rng.permuted(stuff, axis=1, out=stuff)

        output = np.reshape(temp, (repetition, int(length / team_size), team_size))
        np.ascontiguousarray(output, dtype=np.ubyte)
        redone = np.sort(output, kind='heapsort')
        order = redone[:, :, 0].argsort()
        rearranged = np.take_along_axis(redone, order[:, :, None], axis=1)

        unique = np.unique(rearranged, axis=0)

        remapper = self.replace_dict_keys_with_incremental_value(data)

        remapped = np.vectorize(remapper.__getitem__)(unique)

        stds = np.empty(len(remapped))
        for i in range(len(remapped)):
            iteration = remapped[i]
            stds[i] = self.np_calculate_iteration_mean_and_stdev(iteration)

        calculated = np.argmin(stds)
        return unique[calculated].tolist()
    
    @staticmethod
    def cast_teams(index, team_size):
        return [index[i:i + team_size] for i in range(0, len(index), team_size)]
    
    @staticmethod
    def replace_dict_keys_with_incremental_value(data):
            new = {}
            current = 0
            for values in data.values():
                new[current] = values
                current += 1
            return new
    
    @staticmethod
    def np_calculate_iteration_mean_and_stdev(iteration):
            # Needs to Calculate Stdev for each iteration, e.g.:
            # [[1108 1220 1231 1231]
            #  [1266 1273 1285 1349]
            #  [1358 1362 1519 1621]
            #  [1467 1543 1647 1851]]
            return np.std(np.apply_along_axis(np.sum, 1, iteration))
    
    
