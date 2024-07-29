from random import randint

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
sys.path.insert(1, 'C://Users//kid//SynologyDrive//Lab2023//KIDs//QTLab2324//IRdetection//Instruments//Gas_Handler22')
import handler

class Plot_P15(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Temperature vs time dynamic plot
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0))
        self.plot_graph.setTitle("Temperature vs Time", color="b", size="20pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "Temperature (°C)", **styles)
        self.plot_graph.setLabel("bottom", "Time (min)", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(20, 40)
        self.time = list(range(10))
        self.temperature = [randint(20, 40) for _ in range(10)]
        # Get a line reference
        self.line = self.plot_graph.plot(
            self.time,
            self.temperature,
            name="Temperature Sensor",
            pen=pen,
            symbol="+",
            symbolSize=15,
            symbolBrush="b",
        )
        # Add a timer to simulate new temperature measurements
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        fridge = handler.FridgeHandler()
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
        self.press = self.press[1:]
        self.press.append(float(fridge.get_sensor(15)))
        self.line.setData(self.time, self.temperature)

app = QtWidgets.QApplication([])
main = Plot_P15()
main.show()
app.exec()