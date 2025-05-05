import pandas as pd
from datetime import datetime
import multiprocessing as mp


def init():
    global makiwara
    makiwara = None

    global x1
    x1 = []

    global rawDataFrame
    rawDataFrame = pd.DataFrame()     #columns=['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2']

    global currentMeasurementStats
    currentMeasurementStats = pd.DataFrame()
    
    global time_vector
    time_vector = None

    global timeInput
    timeInput = 60

    global current_user
    current_user = None

    global punch_scores_plot
    punch_scores_plot = []
