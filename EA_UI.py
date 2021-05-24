import graphBandwidth

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets
import sys
import random
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
import serial
import time
import traceback
from datetime import datetime
from PyQt5 import uic
import numpy as np

from random import seed
from random import randint
from random import random
import matplotlib.pyplot as plt
import numpy as np
import math
import copy
import serial  # serial library
import numpy
import matplotlib
from drawnow import *
import time
import traceback
from datetime import datetime
import sys
import math
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('EA_UI.ui', self)
        self.resize(888, 600)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        # self.ui.grid_layout_graph.addWidget(self.canvas, 0, 0, 1, 1)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # widget_placholder would hold the layout together
        self.ui.space_for_graph.setLayout(layout)

        self.file_ = "f2_l-d_kp_20_878.txt"
        self.population_size_ = 0
        self.offspring_size_ = 0
        self.generations_ = 0
        self.mutation_rate_ = 0.0
        self.iterations_ = 0
        self.parent_ss_ = ""
        self.survivor_ss_ = ""
        self.arr_x_ = []
        self.arr_y_BSF_ = []
        self.arr_y_ASF_ = []
        self.best_fitness_ = 0
        self.avg_fitness_ = 0

        self.show()

        self.ui.create_button.pressed.connect(self.create_graph)
        self.ui.save_button.pressed.connect(self.save_graph)
        # self.ui.population_size.setMaximum(1000)
        # self.ui.offspring_size.setMaximum(1000)
        # self.ui.generations.setMaximum(5000)
        # self.ui.mutation_rate.setMaximum(1.0)

    def create_graph(self):
        self.population_size_ = self.ui.population_size.value()
        print(self.population_size_)
        self.offspring_size_ = self.ui.offspring_size.value()
        self.generations_ = self.ui.generations.value()
        self.iterations_ = self.ui.iterations.value()
        self.mutation_rate_ = float(self.ui.mutation_rate.value())
        self.parent_ss_ = self.ui.parent_ss.currentText()
        self.survivor_ss_ = self.ui.survivor_ss.currentText()
        self.EA_obj_ = graphBandwidth(
            self.file_, self.population_size_, self.offspring_size_, self.generations_, self.mutation_rate_, self.iterations_, self.parent_ss_, self.survivor_ss_)
        self.arr_x_, self.arr_y_BSF_, self.arr_y_ASF_ = self.EA_obj_.run_algo()
        self.best_fitness_ = self.EA_obj_.best_fitness
        self.avg_fitness_ = self.EA_obj_.avg_fitness
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.arr_x_, self.arr_y_BSF_,
                              'r', label="Best Fitness")
        self.canvas.axes.plot(self.arr_x_, self.arr_y_ASF_,
                              'b', label="Avg Fitness")
        self.canvas.axes.legend()
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
        # set the texts
        self.ui.best_fitness.setText(str(self.best_fitness_))
        self.ui.avg_fitness.setText(str(self.avg_fitness_))

    def save_graph(self):
        pass

    # def update_plot(self):
    #     self.canvas.axes.cla()  # Clear the canvas.
    #     self.canvas.axes.plot(self.xdata, self.ydata, 'r')
    #     # Trigger the canvas to update and redraw.
    #     self.canvas.draw()


if __name__ == "__main__":  # Multiple threads called under the main function
    def run():
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())

run()