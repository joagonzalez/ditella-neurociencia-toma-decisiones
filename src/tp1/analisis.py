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
# from pandas import read_excel

class DataAnalysis:

    DIR = '/home/jgonzalez/dev/ditella-neurociencia-toma-decisiones/src/tp1/data/'
    FILES = []
    TRIALS = 20
    LANGUAGES = []
    RESULTS = {}


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

    def create_result_structure(self, language):
        '''
        Adds generic result structure for a new language detected
        '''
        self.RESULTS[language] = {}
        if language == '0':
            self.RESULTS[language]['language'] = 'ingles'
        else:
            self.RESULTS[language]['language'] = 'español'
        self.RESULTS[language]['consistent'] = []
        self.RESULTS[language]['inconsistent'] = []
        self.RESULTS[language]['difficulty'] = []
        self.RESULTS[language]['response_time'] = []
        self.RESULTS[language]['correct_answers'] = []
        self.RESULTS[language]['muCongruentes'] = 0
        self.RESULTS[language]['muIncongruentes'] = 0
        self.RESULTS[language]['stdCongruentes'] = 0
        self.RESULTS[language]['stdIncongruentes'] = 0

    def get_list_files(self):
        return self.FILES

    def get_difficulty(self):
        self.read_list_files()

        for file in self.FILES:
            tabla = open(self.DIR + file)
            i=0
            while i < self.TRIALS: 
                line=tabla.readline()
                parsed_line=line.split()
                language = parsed_line[4]
                if language not in self.LANGUAGES:
                    self.LANGUAGES.append(language)
                    self.create_result_structure(language)

                    self.RESULTS[language]['response_time'].append(float(parsed_line[8]))
                    self.RESULTS[language]['correct_answers'].append(parsed_line[7])
                    self.RESULTS[language]['difficulty'].append(int(parsed_line[3]))
                else:
                    self.RESULTS[language]['response_time'].append(float(parsed_line[8]))
                    self.RESULTS[language]['correct_answers'].append(parsed_line[7])
                    self.RESULTS[language]['difficulty'].append(int(parsed_line[3]))

                i+=1
            print(self.RESULTS)
            for language, values in self.RESULTS.items():
                self.RESULTS[language]['consistent'] = [i for i, x in enumerate(self.RESULTS[language]['difficulty']) if x == 1]
                self.RESULTS[language]['inconsistent'] = [i for i, x in enumerate(self.RESULTS[language]['difficulty']) if x == 0]

            print('english results')
            print(self.RESULTS['0'])
            print('spanish results')
            print(self.RESULTS['1'])

    def analyze_data(self, language):
        print(f'Analyzing data for {self.RESULTS[language]["language"]}')
        response_time=np.array(self.RESULTS[language]['response_time'])
        print(response_time)
        
        self.RESULTS[language]['muCongruentes'] = np.mean(response_time[self.RESULTS[language]['consistent']]);
        self.RESULTS[language]['muIncongruentes'] = np.mean(response_time[self.RESULTS[language]['inconsistent']]);
        self.RESULTS[language]['stdCongruentes'] = np.std(response_time[self.RESULTS[language]['consistent']]);
        self.RESULTS[language]['stdIncongruentes'] = np.std(response_time[self.RESULTS[language]['inconsistent']]);

        print(f'Mean consistent {self.RESULTS[language]["muCongruentes"]}')
        print(f'Std consistent {self.RESULTS[language]["stdCongruentes"]}')
        print(f'Mean inconsistent {self.RESULTS[language]["muIncongruentes"]}')
        print(f'Std inconsistent{self.RESULTS[language]["stdIncongruentes"]}')

    def is_significant(self, language):
        response_time = np.array(self.RESULTS[language]['response_time'])
        test=stats.ttest_ind(response_time[self.RESULTS[language]['consistent']], 
                             response_time[self.RESULTS[language]['inconsistent']]);

        print(f'Is significant for language {language}: {test}')
        
        return(test)
    
    def plot_cons_incons(self, language):
        n_groups = 2

        test = self.is_significant(language)

        fig, ax = plt.subplots()

        rects1 = ax.bar(1, self.RESULTS[language]["muCongruentes"], 0.3,
                        alpha=0.4, color='b',
                        yerr=self.RESULTS[language]['stdCongruentes']/np.sqrt(len(self.RESULTS[language]['consistent'])),
                        label=f'Congruentes [{self.RESULTS[language]["language"]}]')

        rects2 = ax.bar(1 + 0.35, self.RESULTS[language]["muIncongruentes"], 0.3,
                        alpha=0.4, color='r',
                        yerr=self.RESULTS[language]['stdIncongruentes']/np.sqrt(len(self.RESULTS[language]['inconsistent'])),
                        label=f'Incongruentes [{self.RESULTS[language]["language"]}]')

        plt.ylim([600,1600])
        plt.xticks([1,1.35], ('1', '2'))
        ax.set_ylabel('Response Time')
        ax.set_title('P='+str(test[1]))
        ax.legend(loc='upper left')
        plt.show() 



if __name__ == "__main__":
    informe = DataAnalysis()
    for filename in informe.get_list_files():
        print(f'Solving analysis for file: {filename}')
        informe.read_file(filename)
        informe.get_difficulty()
        for language in informe.LANGUAGES:
            informe.analyze_data(str(language))
            informe.is_significant(str(language))
            informe.plot_cons_incons(str(language))