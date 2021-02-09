'''
TP1 - Stroop Experiment
Universidad Torcuato Di Tella - MiM + Analytics
Alejandro Romanisio - aromanisio@gmail.com
Joaquin Gonzalez - joagonzalez@gmail.com
Fecha: 09/02/2021
'''

import sys
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pandas import read_excel

class DataAnalysis:

    DIR = '/home/jgonzalez/dev/ditella-neurociencia-toma-decisiones/src/tp1/data/'
    FILES = []
    TRIALS = 20
    consistent = []
    inconsistent = []
    response_time = []
    muCongruentes = 0
    muIncongruentes = 0
    stdCongruentes = 0
    stdIncongruentes = 0


    def __init__(self):
        self.read_list_files()

    def get_results(self):
        pass

    def read_file(self, filename, directory=None):
        '''
        Read file content
        '''
        try:
            if directory == None:
                directory = self.DIR
            f = open(directory + filename, 'r')
            data = f.read()
            print(data)
        except Exception as e:
            print(f'Error opening file {filename}!')
            print(f'Error: {str(e)}')

    def read_list_files(self, directory=None):
        '''
        Read list of files from data directory
        '''

        if directory == None:
            directory = self.DIR

        self.FILES = [f for f in listdir(directory) if isfile(join(directory, f))]

    def get_list_files(self):
        return self.FILES

    def get_difficulty(self):
        self.read_list_files()
        difficulty = []
        for file in self.FILES:
            tabla = open(self.DIR + file)
            i=0
            while i < self.TRIALS: 
                line=tabla.readline()
                parsed_line=line.split()
                self.response_time.append(float(parsed_line[8]))
                difficulty.append(int(parsed_line[3]))
                i+=1
            self.consistent = [i for i, x in enumerate(difficulty) if x == 1]
            self.inconsistent = [i for i, x in enumerate(difficulty) if x == 0]

            print(self.consistent)
            print(self.inconsistent)
            print(self.response_time)

    def analyze_data(self):
        response_time=np.array(self.response_time)
        print(response_time)
        
        self.muCongruentes=np.mean(response_time[self.consistent]);
        self.muIncongruentes=np.mean(response_time[self.inconsistent]);
        self.stdCongruentes=np.std(response_time[self.consistent]);
        self.stdIncongruentes=np.std(response_time[self.inconsistent]);

        print(self.muCongruentes)
        print(self.muIncongruentes)
        print(self.stdCongruentes)
        print(self.stdIncongruentes)

    def is_significant(self):
        response_time = np.array(self.response_time)
        test=stats.ttest_ind(response_time[self.consistent], 
                             response_time[self.inconsistent]);
        print(test)
        
        return(test)
    
    def plot_cons_incons(self):
        n_groups = 2

        test = self.is_significant()

        fig, ax = plt.subplots()

        rects1 = ax.bar(1, self.muCongruentes, 0.3,
                        alpha=0.4, color='b',
                        yerr=self.stdCongruentes/np.sqrt(len(self.consistent)),
                        label='Congruentes')

        rects2 = ax.bar(1 + 0.35, self.muIncongruentes, 0.3,
                        alpha=0.4, color='r',
                        yerr=self.stdIncongruentes/np.sqrt(len(self.inconsistent)),
                        label='Incongruentes')

        plt.ylim([600,1200])
        plt.xticks([1,1.35], ('1', '2'))
        ax.set_ylabel('RT')
        ax.set_title('P='+str(test[1]))
        ax.legend(loc='upper left')
        plt.show() 


if __name__ == "__main__":
    informe = DataAnalysis()
    print(informe.get_list_files())
    informe.read_file(informe.get_list_files()[0])
    informe.get_difficulty()
    informe.analyze_data()
    informe.is_significant()
    informe.plot_cons_incons()