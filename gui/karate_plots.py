import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer

from backend import global_vars


class PlotTraining(FigureCanvas):
    def __init__(self, parent=None):     
        self.fig, self.ax = plt.subplots(2, 1, figsize=(10, 5), dpi=200,
                                         sharex=True, sharey=True)
        #self.fig = Figure(dpi = 150)
        super().__init__(self.fig)
        self.xlim = None 
        self.ylim = None
        #self.grafica_datos()
        self.line, = self.ax[0].plot([], [])
        self.ax[0].set_ylim(-64, 64)
        self.ax[0].set_xlim(0, 100)

        self.converted_list_size = 0
        self.converted_z1 = []

        self.timer = QTimer()
        #self.timer.setInterval(0.5)
        #self.timer.timeout.connect(global_vars.makiwara.update_plot)
        self.timer.timeout.connect(self.real_time_plot)
        
        self.timer.start(50) # 100ms frissites

    def real_time_plot(self):
        tmp = global_vars.makiwara.accel[self.converted_list_size:]
        if tmp:
            for acc in tmp:
                zData = (global_vars.makiwara.myKx.convert_number_signed(acc[5] << 8, 16)) | acc[4]
                
                conv_G = global_vars.makiwara.myKx.get_conv_G()
                self.converted_z1.append(round(zData * conv_G, 6))
            
            
            self.converted_list_size = len(self.converted_z1)
            print(self.converted_list_size)
        
        self.line.set_ydata(self.converted_z1)
        self.line.set_xdata(range(self.converted_list_size))
        self.ax[0].set_xlim(0, self.converted_list_size)
        self.draw()

    def grafica_datos(self):
        if not isinstance(self.ax, np.ndarray):
            self.ax = [self.ax]

        #if hasattr(self, 'ax_limits'):
        try:
            self.xlim = [ax.get_xlim() for ax in self.ax]
            self.ylim = [ax.get_ylim() for ax in self.ax]
            
        except AttributeError:
            self.xlim = [None] * len(self.ax)
            self.ylim = [None] * len(self.ax)

        matplotlib.rc('xtick', labelsize=3)
        matplotlib.rc('ytick', labelsize=3)
        self.ax[0].clear()
        self.ax[0].plot(global_vars.time_vector, global_vars.rawDataFrame.X1, linewidth=1, antialiased=True, label='X1')
        self.ax[0].plot(global_vars.time_vector, global_vars.rawDataFrame.Y1, linewidth=1, antialiased=True, label='Y1')
        self.ax[0].plot(global_vars.time_vector, global_vars.rawDataFrame.Z1, linewidth=1, antialiased=True, label='Z1')
        plt.xticks(rotation=45)
        self.ax[0].set_title("Accelerometer signals - no punch was detected on the makiwara", fontsize=6)
        #self.ax[0].set_xlabel("Time: H:M:S", fontsize=4)
        self.ax[0].set_ylabel("Acceleration [G]", fontsize=4)

        self.ax[1].clear()
        self.ax[1].plot(global_vars.time_vector, global_vars.rawDataFrame.X2, linewidth=1, antialiased=True, label='X2')
        self.ax[1].plot(global_vars.time_vector, global_vars.rawDataFrame.Y2, linewidth=1, antialiased=True, label='Y2')
        self.ax[1].plot(global_vars.time_vector, global_vars.rawDataFrame.Z2, linewidth=1, antialiased=True, label='Z2')
        self.ax[1].set_xlabel("Time: H:M:S", fontsize=4)
        self.ax[1].set_ylabel("Acceleration [G]", fontsize=4)
        
        if self.xlim[0] is not None:
            #self.ax[0].set_xlim(self.xlim[0])
            #self.ax[0].set_ylim(self.ylim[0])
            self.ax[0].set_xlim(auto=True)
            self.ax[0].set_ylim(auto=True)

        if self.xlim[1] is not None:
            self.ax[1].set_xlim(auto=True)
            self.ax[1].set_ylim(auto=True)
        

        """self.ax_limits = {
            'xlim': [ax.get_xlim() for ax in self.ax],
            'ylim': [ax.get_ylim() for ax in self.ax]
        }"""
        self.ax[0].legend(loc='upper left', fontsize=4)
        self.ax[1].legend(loc='upper left', fontsize=4)
        self.fig.tight_layout()
        #QtCore.QTimer.singleShot(10, self.grafica_datos)
        self.draw()


class PlotFeedback(FigureCanvas):
    def __init__(self, parent=None):     
        self.fig, self.ax = plt.subplots(2, 1, figsize=(10, 5), dpi=200,
                                         sharex=True, sharey=True)
        #self.fig = Figure(dpi = 150)
        super().__init__(self.fig)
        self.xlim = None 
        self.ylim = None
        self.grafica_datos()

    def grafica_datos(self):
        if not isinstance(self.ax, np.ndarray):
            self.ax = [self.ax]

        #if hasattr(self, 'ax_limits'):
        try:
            self.xlim = [ax.get_xlim() for ax in self.ax]
            self.ylim = [ax.get_ylim() for ax in self.ax]
            
        except AttributeError:
            self.xlim = [None] * len(self.ax)
            self.ylim = [None] * len(self.ax)

        matplotlib.rc('xtick', labelsize=3)
        matplotlib.rc('ytick', labelsize=3)
        self.ax[0].clear()
        self.ax[0].plot(global_vars.time_vector, global_vars.rawDataFrame.X1, linewidth=1, antialiased=True, label='X1')
        self.ax[0].plot(global_vars.time_vector, global_vars.rawDataFrame.Y1, linewidth=1, antialiased=True, label='Y1')
        self.ax[0].plot(global_vars.time_vector, global_vars.rawDataFrame.Z1, linewidth=1, antialiased=True, label='Z1')
        for punch in global_vars.currentMeasurementStats.max_acc:
            p_idx = global_vars.rawDataFrame.Z1.loc[global_vars.rawDataFrame.Z1 == punch].index[0]
            self.ax[0].plot(global_vars.time_vector[p_idx], punch, "*")
        plt.xticks(rotation=45)
        self.ax[0].set_title("Accelerometer signals", fontsize=6)
        #self.ax[0].set_xlabel("Time: H:M:S", fontsize=4)
        self.ax[0].set_ylabel("Acceleration [G]", fontsize=4)

        self.ax[1].clear()
        self.ax[1].plot(global_vars.time_vector, global_vars.rawDataFrame.X2, linewidth=1, antialiased=True, label='X2')
        self.ax[1].plot(global_vars.time_vector, global_vars.rawDataFrame.Y2, linewidth=1, antialiased=True, label='Y2')
        self.ax[1].plot(global_vars.time_vector, global_vars.rawDataFrame.Z2, linewidth=1, antialiased=True, label='Z2')
        self.ax[1].set_xlabel("Time: H:M:S", fontsize=4)
        self.ax[1].set_ylabel("Acceleration [G]", fontsize=4)
        
        if self.xlim[0] is not None:
            #self.ax[0].set_xlim(self.xlim[0])
            #self.ax[0].set_ylim(self.ylim[0])
            self.ax[0].set_xlim(auto=True)
            self.ax[0].set_ylim(auto=True)

        if self.xlim[1] is not None:
            self.ax[1].set_xlim(auto=True)
            self.ax[1].set_ylim(auto=True)
        

        """self.ax_limits = {
            'xlim': [ax.get_xlim() for ax in self.ax],
            'ylim': [ax.get_ylim() for ax in self.ax]
        }"""
        self.ax[0].legend(loc='upper left', fontsize=4)
        self.ax[1].legend(loc='upper left', fontsize=4)
        self.fig.tight_layout()
        #QtCore.QTimer.singleShot(10, self.grafica_datos)
        self.draw()
