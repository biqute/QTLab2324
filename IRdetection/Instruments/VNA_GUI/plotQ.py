import time
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import HP8753E as hp


class MplCanvasQ(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvasQ, self).__init__(fig)


class Q_Widget(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Q_Widget, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvasQ(self, width=10, height=8, dpi=100)
        data = self.get_data()
        sc.axes.plot(data[0], data[1])
        sc.axes.set_xlabel('Frequency [GHz]')
        sc.axes.set_ylabel('Q')
        sc.axes.set_title('Q plot')
        self.setCentralWidget(sc)

        self.show()

    def get_data(self):
        vna = hp.HP8753E()
        i, q, f = vna._I, vna._Q, vna._F
        return f, q