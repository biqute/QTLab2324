import time
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import HP8753E as hp


class MplCanvasPhase(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvasPhase, self).__init__(fig)


class S21Phase_Widget(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(S21Phase_Widget, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvasPhase(self, width=10, height=8, dpi=100)
        data = self.get_data()
        sc.axes.scatter(data[0], data[1], marker='x', color='black', s=1)
        sc.axes.set_xlabel('Frequency [GHz]')
        sc.axes.set_ylabel('Power [dBm]')
        sc.axes.set_title('S21 Absolute Value plot')
        self.setCentralWidget(sc)

        self.show()

    def get_data(self):
        vna = hp.HP8753E()
        vna.autoscale()
        i, q, f = vna._I, vna._Q, vna._F
        phase = vna.phase_S21(i, q)
        return f, phase