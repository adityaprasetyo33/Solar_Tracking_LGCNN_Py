from trainingLgcnn import training
from testLgcnn import test
import numpy as np
import serial
import random
import time

#training.trainingLgcnn()
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    ser.write(str(1).encode('utf-8'))
    hasil = 1
    while True:
        line1 = ser.readline().decode('utf-8').rstrip()
        print(line1)
        if line1 != '':
            arr = [float(x) for x in line1.split(",")]
            hasil = test.testLgcnn(arr)
            print(hasil)
            ser.write(str(hasil).encode('utf-8'))
            time.sleep(5)
        else:
            ser.write(str(hasil).encode('utf-8'))
        time.sleep(1)
        #hasil = test.testLgcnn(arr)
        #print(hasil)
        
