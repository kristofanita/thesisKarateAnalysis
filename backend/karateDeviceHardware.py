from backend import opt_kx13x
import time
from datetime import datetime
import sys
import csv
import matplotlib.pyplot as plt
import math
import pandas as pd
import qwiic_i2c
import os
import RPi.GPIO as GPIO
import multiprocessing as mp
from backend import global_vars

class Makiwara(object):
    
    def __init__(self):
        self.myKx = opt_kx13x.QwiicKX134(bus=1, address=0x1f) # bus=1
        self.myKx2 = opt_kx13x.QwiicKX134(bus=3, address=0x1e) # bus=3
        self.GPIO_IT1 = 17 # 17 a most hasznalt GND alatt 1el, 27--> GND alatt 2. és 22 -->GND alatt 3.
        self.GPIO_IT2 = 22
        self.range_G1 = -1
        self.range_G2 = -1
        self.hz1 = -1
        self.hz2 = -1    
        self.manager = mp.Manager()
        self.accel = self.manager.list()
        self.accel2 = self.manager.list()
        self.t1 = self.manager.list() # save start and end time of accelerometer1 read
        self.t2 = self.manager.list() # same for accelerometer2
        self.p1 = None
        self.p2 = None
        self.setupSensors()
        self.p1 = mp.Process(target=self.read_accelero, args=(1, self.GPIO_IT1, self.myKx, self.accel, self.t1))
        self.p2 = mp.Process(target=self.read_accelero, args=(2, self.GPIO_IT2, self.myKx2, self.accel2, self.t2))
    

    def setupSensors(self):
        print("Please wait until system setup")
        """
            GPIO setup:
            """
        GPIO.setmode(GPIO.BCM) # BOARD, BCM
        GPIO.setup(self.GPIO_IT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_IT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
        """
            setup acceleros
        """
        if self.myKx.is_connected() == False:
            print('No connection with accelerometer 1f on bus 1')
            return
        if self.myKx2.is_connected() == False: # bus=3
            print('No connection with accelerometer')
            return
            
        if self.myKx.begin():
            print('Sensor 1 Ready')
        else:
            print('make sure you are using the KX134')
        
        if self.myKx2.begin():
            print('Sensor 2 Ready')
        else:
            print('make sure you are using the KX134')
            
        odr = 9
        if self.myKx.set_output_data_rate(odr) == False:
            print("accelerometer1: output data rate could not be configured")
        else:
            self.hz1 = self.myKx.get_output_data_rate()
            print("accelerometer1 output data rate set to", self.hz1, "Hz")
        
        if self.myKx2.set_output_data_rate(odr) == False:
            print("accelerometer2: data rate could not be configured")
        else:
            self.hz2 = self.myKx2.get_output_data_rate()
            print("accelerometer2: output data rate set to", self.hz2, "Hz")
                
        self.myKx.initialize(self.myKx.BUFFER_INTERRUPT_SETTINGS)
        self.myKx2.initialize(self.myKx2.BUFFER_INTERRUPT_SETTINGS)    
        
        if self.myKx.set_range(2) == False:
            print("accelerometer1 could not be configured")
        else:
            print("accelerometer1 range set to 32G")
        if self.myKx2.set_range(2) == False:
            print("accelerometer2 could not be configured")
        else:
            print("accelerometer2 range set to 32G")
        
        self.range_G1 = self.myKx.get_range()
        self.range_G2 = self.myKx2.get_range()
        print("Accelerometer range set to:", self.range_G1, "G and", self.range_G2, "G")
        

            ####################################
     

    def read_accelero(self, num, GPIO_IT, myKx, accel, t):
        myKx.clear_buffer()
        print("START")
        GPIO.setmode(GPIO.BCM) # BOARD, BCM
        GPIO.setup(GPIO_IT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        t.append(datetime.now()) # .strptime("%y.%m.%d-%H:%M:%S.%f")
        
        t_end = time.time() + global_vars.timeInput
        while time.time() < t_end:
            while(GPIO.input(GPIO_IT) == 1):
                continue  
            for i in range(50):
                accel.append(myKx.get_raw_accel_data())
        # t.append(datetime.now().strftime("%y.%m.%d-%H:%M:%S.%f"))

    """
    def runMakiwara(self, playButtonEnabled):
        if playButtonEnabled:
            print("Start recording...")
            #if not self.play.isEnabled():
            #  
            #self.p1.start()
            self.p2.start()
                
            #self.p1.join()
            self.p2.join()
            print("Stop recording")
            GPIO.cleanup()
        else:
            if self.p2.is_alive(): # and self.p1.is_alive()
                #self.p1..terminate()
                self.p2.terminate()
                #self.p1.join()
                self.p2.join()
    """

    def runMakiwara1(self):
            print("Start recording...")
            self.p1.start()
            self.p2.start()
            #self.p2.join()
            GPIO.cleanup()

    def generate_time_vector(self, start_datetime, end_datetime, num_points):
        #start_datetime = datetime.strptime(t_start)#  '%Y.%m.%d-%H:%M:%S.%f'
        #end_datetime = datetime.strptime(t_end, '%Y.%m.%d-%H:%M:%S.%f')

        time_difference = end_datetime - start_datetime
        time_step = time_difference / (num_points - 1)

        time_vector = [start_datetime + i * time_step for i in range(num_points)]
        return time_vector
    
    def convertData(self, t_end2):
        """
        process data
        """
        global rawDataFrame
        x1 = []
        y1 = []
        z1 = []
        x2 = []
        y2 = []
        z2 = []
        for acc in self.accel:
            xData = (self.myKx.convert_number_signed(acc[1] << 8, 16)) | acc[0]
            yData = (self.myKx.convert_number_signed(acc[3] << 8, 16)) | acc[2]
            zData = (self.myKx.convert_number_signed(acc[5] << 8, 16)) | acc[4]
            
            conv_G = self.myKx.get_conv_G()                       
            x1.append(round(xData * conv_G, 6))
            y1.append(round(yData * conv_G, 6))
            z1.append(round(zData * conv_G, 6))
        print("size of x1 list", len(x1))
            
        for acc in self.accel2:
            xData2 = (self.myKx2.convert_number_signed(acc[1] << 8, 16)) | acc[0]
            yData2 = (self.myKx2.convert_number_signed(acc[3] << 8, 16)) | acc[2]
            zData2 = (self.myKx2.convert_number_signed(acc[5] << 8, 16)) | acc[4]
            
            conv_G2 = self.myKx2.get_conv_G()
            x2.append(round(xData2 * conv_G2, 6))
            y2.append(round(yData2 * conv_G2, 6))
            z2.append(round(zData2 * conv_G2, 6))
        print("size of x2 list", len(x2))
        print(x2[0])
        if len(x1) < len(x2):
            for _ in range(len(x2) - len(x1)):
                x1.insert(len(x1), 0)
                y1.insert(len(y1), 0)
                z1.insert(len(z1), 0)
        elif len(x2) < len(x1):
            for _ in range(len(x1) - len(x2)):
                x2.insert(0, 0)
                y2.insert(0, 0)
                z2.insert(0, 0)
        # tmp = pd.DataFrame({'X1':x1, 'Y1':y1, 'Z1':z1, 'X2':x2, 'Y2':y2, 'Z2':z2})
        if not global_vars.rawDataFrame.empty:
            global_vars.rawDataFrame = pd.DataFrame()
        global_vars.rawDataFrame.insert(0, "X1", x1)
        global_vars.rawDataFrame.insert(1, "Y1", y1)
        global_vars.rawDataFrame.insert(2, "Z1", z1)
        global_vars.rawDataFrame.insert(3, "X2", x2)
        global_vars.rawDataFrame.insert(4, "Y2", y2)
        global_vars.rawDataFrame.insert(5, "Z2", z2)

        #mock data as I have no makiwara and only one sensor
        # df = pd.read_csv("/home/karate/karateProjectFullstack/data/GLaci.csv", index_col=False, usecols=['X1', 'Y1', 'Z1'])
        # df2 = pd.read_csv("/home/karate/karateProjectFullstack/data/GLaci2.csv", index_col=False, usecols=['X2', 'Y2', 'Z2'])
        # global_vars.rawDataFrame = pd.concat([df, df2], axis=1)
        
        print(global_vars.rawDataFrame.info())
        print(global_vars.rawDataFrame.head())
        num_points = len(x1)
        print("num points:", num_points)
        print("start_time:", self.t1[0])
        print("end_time:", t_end2)
        global_vars.time_vector = self.generate_time_vector(self.t1[0], t_end2, num_points)

    def plotSaveRawData(self):
        if rawDataFrame.X1 or rawDataFrame.X2:
            """
                plot results: 1st accelero without address pin wired plotted on top and the other accelero plotted at the bottom subplot
            """
            fig = plt.figure(1)
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212, sharey=ax1)
            ax1.set_ylim([-self.range_G1, self.range_G1])
            lw = 1
            ax1.plot(rawDataFrame.X1, label='x1', linewidth=lw)
            ax1.plot(rawDataFrame.Y1, label='y1', linewidth=lw)
            ax1.plot(rawDataFrame.Z1, label='z1', linewidth=lw)
            ax1.legend()

            ax2.set_ylim([-self.range_G2, self.range_G2])
            ax2.plot(rawDataFrame.X2, label='x2', linewidth=lw)
            ax2.plot(rawDataFrame.Y2, label='y2', linewidth=lw)
            ax2.plot(rawDataFrame.Z2, label='z2', linewidth=lw)
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
                #df2 = pd.DataFrame({'x2':x2, 'y2':y2, 'z2':z2})
                #df.to_csv(filename, header=True, index=True)
                #df2.to_csv(filename_ + "2.csv", header=True, index=True)
                rawDataFrame.to_csv(filename, header=True, index=True)
                fig_filename = filename_ + ".svg"
                fig1.savefig(fig_filename, dpi=150)
                
                #raw1 = for acc in accel: ["\t" + str(reg_value) for reg_value in acc]
                #raw2 = for acc in accel2: ["\t" + str(reg_value) for reg_value in acc]
                conv_G2 = self.myKx2.get_conv_G()
                info_text = [
                        #"Accelerometer 1",
                        #"\tOutput data rate: " + str(self.hz1) + "Hz",
                        #"\tAccelerometer range: " + str(self.range_G1) + "G",
                        #"\tConverted numbers to G with:" + str(conv_G),
                        #"\tTime of record: from " + self.t1[0] + " to " + self.t1[1],
                        "Accelerometer 2",
                        "\tOutput data rate: " + str(self.hz2) + "Hz",
                        "\tAccelerometer range: " + str(self.range_G2) + "G",
                        "\tConverted numbers to G with:" + str(conv_G2),
                        "\tTime of record: from " + self.t2[0] + " to " + self.t2[1],
                        "\n",
                        "Raw data from accelerometer 1\n"
                        ]
                info_filename = filename_ + ".txt"
                with open(info_filename, 'a') as f:
                    f.writelines('\n'.join(info_text))
                    for acc in self.accel:
                        f.write('\t'.join(str(reg_value) for reg_value in acc))
                        f.write('\n')
                    f.write('\n')
                    f.write("Raw data from accelerometer 2")
                    f.write('\n')
                    for acc in self.accel2:
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


"""if __name__ == '__main__':
    try:
        runExample()
    except(KeyboardInterrupt, SystemExit) as exErr:
        sys.exit(0)
    print("VEGEEEE")
    """
