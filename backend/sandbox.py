import pandas as pd
import numpy as np
"""from sklearn.preprocessing import StandardScaler
import tensorflow as tf

x_test = pd.read_excel("data/X_test_scaled.xlsx")
x_test_scaled = pd.DataFrame(StandardScaler().fit_transform(x_test), columns=x_test.columns)
print(x_test_scaled.head())
scores_model = tf.keras.models.load_model("machine_learning_models/tensorflow_karateScoring_regression_model_directory.keras")
print(scores_model.input_shape)

xs = [None]*10
print(xs)"
"""

import opt_kx13x
import time
from datetime import datetime
import sys
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import pandas as pd
import qwiic_i2c
import os
import RPi.GPIO as GPIO
import multiprocessing as mp

global x1
x1 = []

def read_accelero(num, GPIO_IT, myKx, accel, t):
    myKx.clear_buffer()
    
    GPIO.setmode(GPIO.BCM) # BOARD, BCM
    GPIO.setup(GPIO_IT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    run_time = 100
    t.append(datetime.now().strftime("%y.%m.%d-%H:%M:%S.%f"))
    
    t_end = time.time() + run_time
    while time.time() < t_end:
        while(GPIO.input(GPIO_IT) == 1):
            #print(len(accel))
            continue  
        for i in range(50):
            accel.append(myKx.get_raw_accel_data())
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    t.append(datetime.now().strftime("%y.%m.%d-%H:%M:%S.%f"))
    
    
def data_reader(accel):
    last_read = 0
    while True:
        if len(accel) > last_read:
            new_data = accel# [last_read:]
            print("!!!!!!!!!!!!!!!!!!!", len(new_data))
            last_read = len(accel)
            plt.plot(accel)
        time.sleep(1)


def convert_number_signed(num, bits):
        
        if (num & (1 << (bits - 1))) != 0:
            num = num - (1 << bits)
        return num


def update_plot(frame, accel, line, fig1, ax3):
    time.sleep(0.05)
    new_data = accel[len(x1):-1]
    #x1 = []
    #print(new_data)
    for acc in new_data:
        
        xData = (convert_number_signed(acc[1] << 8, 16)) | acc[0]
        
        conv_G = .000976523950926236762                     
        x1.append(round(xData * conv_G, 6))
    print(len(x1))
    line.set_ydata(x1)
    line.set_xdata(range(len(x1)))
    ax3.set_xlim(0, len(x1))
    return line,
        
        
def runExample():
    fig = plt.figure(1)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharey=ax1)

    fig1, ax3 = plt.subplots()
    ax3.set_ylim(-2, 2)
    ax3.set_xlim(0, 100)

    line, = ax3.plot([], [], lw=1)

    ####################################
     
    print("Please wait until system setup")
    """
    GPIO setup:
    """
    GPIO_IT1 = 17 # 17 a most hasznalt GND alatt 1el, 27--> GND alatt 2. és 22 -->GND alatt 3.
    GPIO_IT2 = 22
    GPIO.setmode(GPIO.BCM) # BOARD, BCM
    #GPIO.setup(GPIO_IT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_IT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    """
    setup acceleros
    """
    myKx = opt_kx13x.QwiicKX134(bus=1, address=0x1f) # bus=1
    myKx2 = opt_kx13x.QwiicKX134(bus=3, address=0x1e) # bus=3
    
    if myKx.is_connected() == False:
        print('No connection with accelerometer 1f on bus 1')
        return
    if myKx2.is_connected() == False: # bus=3
        print('No connection with accelerometer')
        return
    
    if myKx.begin():
        print('Sensor 1 Ready')
    else:
        print('make sure you are using the KX134')
    if myKx2.begin():
        print('Sensor 2 Ready')
    else:
        print('make sure you are using the KX134')
    
    odr = 9
    if myKx.set_output_data_rate(odr) == False:
        print("accelerometer1: output data rate could not be configured")
    else:
        hz1 = myKx.get_output_data_rate()
        print("accelerometer1 output data rate set to", hz1, "Hz")
    if myKx2.set_output_data_rate(odr) == False:
        print("accelerometer2: data rate could not be configured")
    else:
        hz2 = myKx2.get_output_data_rate()
        print("accelerometer2: output data rate set to", hz2, "Hz")
        
    myKx.initialize(myKx.BUFFER_INTERRUPT_SETTINGS)
    myKx2.initialize(myKx2.BUFFER_INTERRUPT_SETTINGS)
    
    range_G1 = myKx.get_range()
    range_G2 = myKx2.get_range()
    #print("Accelerometer range set to:", range_G1, "G and", range_G2, "G")
    
    """
    in case of BUFFER_INTERRUPT_SETTINGS 32G is configured, so lines below do not needed
    if myKx.set_range(2) == False:
        print("accelerometer1 could not be configured")
    else:
        print("accelerometer1 range set to 32G")
    if myKx2.set_range(2) == False:
        print("accelerometer2 could not be configured")
    else:
        print("accelerometer2 range set to 32G")"""

    ####################################
    
    manager = mp.Manager()
    accel = manager.list()
    accel2 = manager.list()
    t1 = manager.list() # save start and end time of accelerometer1 read
    t2 = manager.list() # same for accelerometer2
    
    
    print("Start recording...")
    p1 = mp.Process(target=read_accelero, args=(1, GPIO_IT1, myKx, accel, t1))
    p2 = mp.Process(target=read_accelero, args=(2, GPIO_IT2, myKx2, accel2, t2))
    #reader_process = mp.Process(target=data_reader, args=(accel,))
     
    p1.start()
    p2.start()
    #reader_process.start()

    #plt.style.use('seaborn-darkgrid')
    
    ani = animation.FuncAnimation(fig1, update_plot, fargs=(accel, line, fig1, ax3), interval=50)
    plt.show()

    p1.join()
    p2.join()
    #reader_process.terminate()
    print("Stop recording")
    GPIO.cleanup()
    
    """
    process data
    """
    x1 = []
    y1 = []
    z1 = []
    x2 = []
    y2 = []
    z2 = []
    
    for acc in accel:
        xData = (myKx.convert_number_signed(acc[1] << 8, 16)) | acc[0]
        yData = (myKx.convert_number_signed(acc[3] << 8, 16)) | acc[2]
        zData = (myKx.convert_number_signed(acc[5] << 8, 16)) | acc[4]
        
        conv_G = myKx.get_conv_G()                       
        x1.append(round(xData * conv_G, 6))
        y1.append(round(yData * conv_G, 6))
        z1.append(round(zData * conv_G, 6))
    print("size of x1 list", len(x1))
        
    for acc in accel2:
        xData2 = (myKx2.convert_number_signed(acc[1] << 8, 16)) | acc[0]
        yData2 = (myKx2.convert_number_signed(acc[3] << 8, 16)) | acc[2]
        zData2 = (myKx2.convert_number_signed(acc[5] << 8, 16)) | acc[4]
        
        conv_G2 = myKx2.get_conv_G()
        x2.append(round(xData2 * conv_G2, 6))
        y2.append(round(yData2 * conv_G2, 6))
        z2.append(round(zData2 * conv_G2, 6))
    print("size of x2 list", len(x2))
    
    if x1 or x2:
        """
            plot results: 1st accelero without address pin wired plotted on top and the other accelero plotted at the bottom subplot
        """
        ax1.set_ylim([-range_G1, range_G1])
        lw = 1
        ax1.plot(x1, label='x1', linewidth=lw)
        ax1.plot(y1, label='y1', linewidth=lw)
        ax1.plot(z1, label='z1', linewidth=lw)
        ax1.legend()
        
        lw = 1
        ax2.set_ylim([-range_G2, range_G2])
        ax2.plot(x2, label='x2', linewidth=lw)
        ax2.plot(y2, label='y2', linewidth=lw)
        ax2.plot(z2, label='z2', linewidth=lw)
        ax2.legend()
        fig1 = plt.gcf()
        plt.show()
        
        toSave = input("Would you like to save your results? (yes/no)")
        if toSave == "yes":
            """
                save results as user wants --> csv and svg
            """
            filename_ = input("Please write the file name to save (without extension)\n")
            
            filename = filename_ + ".csv"
            #df = pd.DataFrame({'time':t, 'x1':x1, 'y1':y1, 'z1':z1, 'x2':x2, 'y2':y2, 'z2':z2})
            #df = pd.DataFrame({'x1':x1, 'y1':y1, 'z1':z1})
            df2 = pd.DataFrame({'x2':x2, 'y2':y2, 'z2':z2})
            #df.to_csv(filename, header=True, index=True)
            df2.to_csv(filename_ + "2.csv", header=True, index=True)
            
            fig_filename = filename_ + ".svg"
            fig1.savefig(fig_filename, dpi=150)
            
            #raw1 = for acc in accel: ["\t" + str(reg_value) for reg_value in acc]
            #raw2 = for acc in accel2: ["\t" + str(reg_value) for reg_value in acc]
            
            info_text = [
                    #"Accelerometer 1",
                    #"\tOutput data rate: " + str(hz1) + "Hz",
                    #"\tAccelerometer range: " + str(range_G1) + "G",
                    "#\tConverted numbers to G with:" + str(conv_G),
                    #"\tTime of record: from " + t1[0] + " to " + t1[1],
                    "Accelerometer 2",
                    "\tOutput data rate: " + str(hz2) + "Hz",
                    "\tAccelerometer range: " + str(range_G2) + "G",
                    "\tConverted numbers to G with:" + str(conv_G2),
                    "\tTime of record: from " + t2[0] + " to " + t2[1],
                    "\n",
                    "Raw data from accelerometer 1\n"
                    ]
            info_filename = filename_ + ".txt"
            with open(info_filename, 'a') as f:
                f.writelines('\n'.join(info_text))
                """for acc in accel:
                    f.write('\t'.join(str(reg_value) for reg_value in acc))
                    f.write('\n')
                f.write('\n')"""
                f.write("Raw data from accelerometer 2")
                f.write('\n')
                for acc in accel2:
                    f.write('\t'.join(str(reg_value) for reg_value in acc))
                    f.write('\n')
                f.close()
            
            current_path = os.getcwd()
            saved = current_path + "/" 
            print("Your session is saved: 		                ", saved + filename)
            print("You can also find a picture of the plot: 	", saved + fig_filename)
            print("And an info file with raw data as well:   	", saved + info_filename) 
        elif(toSave == "no"):
            pass
        else:
            print("Couldn't process the answer ", toSave)
            pass
        
        
    else:
        print("+-----------------------------------------------------+")
        print("|                                                     |")
        print("|                No data was recorded                 |")
        print("|                                                     |")
        print("+-----------------------------------------------------+")


if __name__ == '__main__':
    try:
        runExample()
    except(KeyboardInterrupt, SystemExit) as exErr:
        sys.exit(0)
    print("VEGEEEE")

