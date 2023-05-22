import csv
import os
from datetime import datetime

class CSVWriter:
    
    def __init__(self):
        now = datetime.now()
        #self.COLUMNS = ['Index', 'OSC1', 'OSC2', 'Diff', 'Encoder Val']
        self.filename = './log/' + now.strftime("%Y_%m_%d_") + 'log'
        self.file = None
        self.csvwriter = None 
        self.create_file()

    def __init__(self, filetitle):
        now = datetime.now()
        #self.COLUMNS = ['Index', 'OSC1', 'OSC2', 'Diff', 'Encoder Val']
        self.filename = './log/' + now.strftime("%Y_%m_%d_") + filetitle
        self.file = None
        self.csvwriter = None 
        self.create_file()

    def create_file(self, text=None):
        if text is not None:
            self.filename = text
        self.file = open(self.first_file(), 'w')
        self.csvwriter = csv.writer(self.file)
        #self.csvwriter.writerow(self.COLUMNS)

    def first_file(self):
        counter = 0
        while True:
            output_file = "{}_{:05}.csv".format(self.filename, counter)
            counter += 1
            
            if not os.path.exists(os.getcwd()+'\log'):
                os.makedirs("log")        
            if os.path.exists(output_file):
                continue
            return output_file

    def close(self):
        self.file.close()

    def write(self, array):
        self.csvwriter.writerow(array)
        self.file.flush()
