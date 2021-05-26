from graphBandwidth import graphBandwidth
from evol_algo import EA_imp
from generate_graphs import *

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

        # self.file_ = "f2_l-d_kp_20_878.txt"
        self.graphs = generate_graphs(files)
        self.testing_graph = self.graphs[0]
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
        self.num_vertice = ''

        self.show()

        self.ui.create_button.pressed.connect(self.create_graph)
        self.ui.save_button.pressed.connect(self.save_graph)

    def select_graph(self):
        if self.ui.type_of_graph.currentText() == '11 vertices':
            self.testing_graph = self.graphs[0]
            self.num_vertice = '11'
        elif self.ui.type_of_graph.currentText() == '23 vertices':
            self.testing_graph = self.graphs[1]
            self.num_vertice = '23'
        elif self.ui.type_of_graph.currentText() == '100 vertices':
            self.testing_graph = self.graphs[2]
            self.num_vertice = '100'
        else:
            self.testing_graph = self.graphs[3]
            self.num_vertice = '300'
    
    def create_graph(self):
        self.select_graph()
        self.population_size_ = self.ui.population_size.value()
        print(self.population_size_)
        self.offspring_size_ = self.ui.offspring_size.value()
        self.generations_ = self.ui.generations.value()
        self.iterations_ = self.ui.iterations.value()
        self.mutation_rate_ = float(self.ui.mutation_rate.value())
        self.parent_ss_ = self.ui.parent_ss.currentText()
        self.survivor_ss_ = self.ui.survivor_ss.currentText()
        self.EA_obj_ = graphBandwidth(
            self.testing_graph, self.population_size_, self.offspring_size_, self.generations_, self.mutation_rate_, self.iterations_, self.parent_ss_, self.survivor_ss_)
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
        # self.EA_obj_.plot_graph(self.arr_x_, self.arr_y_BSF_, self.arr_y_ASF_)
        x = np.array(self.arr_x_)
        y = np.array(self.arr_y_BSF_)
        y2 = np.array(self.arr_y_ASF_)
        plt.clf()
        plt.plot(x, y, label='Best Fitness so far')
        plt.plot(x, y2, label='Average Fitness so far')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('EA graph analysis \n Best fitness = ' + str(self.best_fitness_) + ', Average Fitness = ' + str(self.avg_fitness_))
        plt.legend()
        # txt = 'Number of Vertices = ' + self.num_vertice + ', Parent Selection Scheme = ' + str(self.parent_ss_) + ', Survivor Selection Scheme = ' + str(self.survivor_ss_) + ', Population size = ' + str(self.population_size_) + ', Offspring size = ' + str(self.offspring_size_) + ', No. of Generations = ' + str(self.generations_)
        # fig = plt.figure()
        # fig.text(.5, .05, txt, ha='center')
        text = self.num_vertice + '_' + str(self.parent_ss_) + '_' + str(self.survivor_ss_) + '_' + str(
            self.population_size_) + '_' + str(self.offspring_size_) + '_' + str(self.generations_)
        plt.savefig('Results\_' + text + '.png',
                    facecolor='white', transparent=False)
        plt.clf()


if __name__ == "__main__":  # Multiple threads called under the main function
    def run():
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())

run()