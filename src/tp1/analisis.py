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

    DIR = './data/'
    FILES = []
    LANGUAGES = []
    RESULTS = {}
    SHOW_PLOT = False
    SAVE_PLOT_AS_FILE = True


    def __init__(self):
        self.read_list_files()


    def get_results(self):
        '''
        Getter for results
        '''
        return self.RESULTS


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


    def create_result_structure(self, filename, language):
        '''
        Adds generic result structure for a new language detected
        '''
        print(f'Creating data structure for {filename}-{language}')

        if filename not in self.RESULTS:
            self.RESULTS[filename] = {}

        if language not in self.RESULTS[filename]:
            self.RESULTS[filename][language] = {}

        if language == '0':
            self.RESULTS[filename][language]['language'] = 'ingles'
        else:
            self.RESULTS[filename][language]['language'] = 'español'
        self.RESULTS[filename][language]['consistent'] = []
        self.RESULTS[filename][language]['inconsistent'] = []
        self.RESULTS[filename][language]['difficulty'] = []
        self.RESULTS[filename][language]['response_time'] = []
        self.RESULTS[filename][language]['correct_answers'] = []
        self.RESULTS[filename][language]['muCongruentes'] = 0
        self.RESULTS[filename][language]['muIncongruentes'] = 0
        self.RESULTS[filename][language]['stdCongruentes'] = 0
        self.RESULTS[filename][language]['stdIncongruentes'] = 0


    def get_list_files(self):
        '''
        Getter for files list
        '''
        return self.FILES


    def get_difficulty(self, filename):
        '''
        Read a file and collects required data
        '''
        tabla = open(self.DIR + filename)
        i=0
        line = tabla.readline()
        while line: 
            parsed_line=line.split()
            language = parsed_line[4]
            line=tabla.readline()
            
            if language not in self.LANGUAGES:
                self.LANGUAGES.append(language)
            
            if filename not in self.RESULTS or language not in self.RESULTS[filename]:
                self.create_result_structure(filename, language)
            
            if parsed_line[7] == '1': # me quedo solo con los que conteste bien
                self.RESULTS[filename][language]['response_time'].append(float(parsed_line[8]))
                self.RESULTS[filename][language]['correct_answers'].append(parsed_line[7])
                self.RESULTS[filename][language]['difficulty'].append(int(parsed_line[3]))
            
            i+=1
        
        # print(self.RESULTS[filename])

        # me quedo solo con los que conteste bien
        for language, values in self.RESULTS[filename].items():
            self.RESULTS[filename][language]['consistent'] = [i for i, x in enumerate(self.RESULTS[filename][language]['difficulty']) if x == 1 and self.RESULTS[filename][language]['correct_answers'][i] == '1']
            self.RESULTS[filename][language]['inconsistent'] = [i for i, x in enumerate(self.RESULTS[filename][language]['difficulty']) if x == 0 and self.RESULTS[filename][language]['correct_answers'][i] == '1']

        # print('english results')
        # print(self.RESULTS[filename]['0'])
        # print('spanish results')
        # print(self.RESULTS[filename]['1'])


    def analyze_data(self, filename, language):
        print(f'Analyzing data for {self.RESULTS[filename][language]["language"]}')
        response_time=np.array(self.RESULTS[filename][language]['response_time'])
        # print(response_time)
        
        self.RESULTS[filename][language]['muCongruentes'] = np.mean(response_time[self.RESULTS[filename][language]['consistent']]);
        self.RESULTS[filename][language]['muIncongruentes'] = np.mean(response_time[self.RESULTS[filename][language]['inconsistent']]);
        self.RESULTS[filename][language]['stdCongruentes'] = np.std(response_time[self.RESULTS[filename][language]['consistent']]);
        self.RESULTS[filename][language]['stdIncongruentes'] = np.std(response_time[self.RESULTS[filename][language]['inconsistent']]);

        stroopEffect = self.RESULTS[filename][language]["muIncongruentes"] - self.RESULTS[filename][language]["muCongruentes"]
        
        print(f'Mean consistent {self.RESULTS[filename][language]["muCongruentes"]}')
        print(f'Std consistent {self.RESULTS[filename][language]["stdCongruentes"]}')
        print(f'Mean inconsistent {self.RESULTS[filename][language]["muIncongruentes"]}')
        print(f'Std inconsistent {self.RESULTS[filename][language]["stdIncongruentes"]}')
        print(f'Stroop effect {stroopEffect}')


    def is_significant(self, filename, language):
        response_time = np.array(self.RESULTS[filename][language]['response_time'])
        test=stats.ttest_ind(response_time[self.RESULTS[filename][language]['consistent']], 
                             response_time[self.RESULTS[filename][language]['inconsistent']]);

        print(f'Is significant for language {language}: {test}')
        
        return(test)


    def plot_cons_incons(self, filename, language):
        n_groups = 2
        language_name = self.RESULTS[filename][language]["language"]
        test = self.is_significant(filename, language)

        fig, ax = plt.subplots()

        rects1 = ax.bar(1, self.RESULTS[filename][language]["muCongruentes"], 0.3,
                        alpha=0.4, color='b',
                        yerr=self.RESULTS[filename][language]['stdCongruentes']/np.sqrt(len(self.RESULTS[filename][language]['consistent'])),
                        label=f'Congruentes [{language_name}]')

        rects2 = ax.bar(1 + 0.35, self.RESULTS[filename][language]["muIncongruentes"], 0.3,
                        alpha=0.4, color='r',
                        yerr=self.RESULTS[filename][language]['stdIncongruentes']/np.sqrt(len(self.RESULTS[filename][language]['inconsistent'])),
                        label=f'Incongruentes [{language_name}]')

        plt.ylim([100,1600])
        plt.xticks([1,1.35], ('1', '2'))
        ax.set_ylabel('Response Time')
        ax.set_title(f'P={str(test[1])} \nFilename: {filename}')
        ax.legend(loc='upper left')

        if self.SHOW_PLOT:
            plt.show() 
        
        if self.SAVE_PLOT_AS_FILE:
            aux = filename.split('.')
            image_name = 'results/' + aux[0] + '_' + aux[1] + '_' + aux[3] + language_name + '.png'
            plt.savefig(image_name)

if __name__ == "__main__":
    informe = DataAnalysis()
    print(informe.get_list_files())
    for filename in informe.get_list_files():
        print(f'Solving analysis for file: {filename}')
        informe.read_file(filename)
        informe.get_difficulty(filename)
        for language in informe.RESULTS[filename]:
            informe.analyze_data(filename, language)
            informe.is_significant(filename, language)
            informe.plot_cons_incons(filename, language)
    # Para debug
    # print(informe.get_results())