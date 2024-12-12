import pandas as pd
from datetime import datetime

def init():
    global rawDataFrame
    rawDataFrame = pd.DataFrame()     #columns=['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2']

    global currentMeasurementStats
    currentMeasurementStats = pd.DataFrame()
    
    global time_vector, start_time, end_time
    start_time = '2024.04.30-01:33:43.800573'
    end_time = '2024.04.30-01:34:13.805039'
    time_vector = []

    global timeInput
    timeInput = 60

