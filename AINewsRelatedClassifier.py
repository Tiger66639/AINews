'''
AINewsRelatedClassifier is a SVM classifier to distinguish from AI-Related or
AI-NotRelated news after the news is crawled and saved into database.

It aims to filter news which contains whitelist terms but actually is not
discussing about AI such as news mention the movie 'Artificial Intelligence'.

The training SVM part locates in AINewsSVM.py which should be executed 
at the same time with the original rating based SVM classification training.

This is the prediction part which is used during the crawling phrase to predict
whether the save news is related or not.

'''
import math
import stat
from os import chdir,getcwd,path,chmod
from svmutil import *
from subprocess import *

from AINewsConfig import config, paths
from AINewsTools import loadcsv, savefile, loadfile
from AINewsDB import AINewsDB

class AINewsRelatedClassifier:
    def __init__(self):
        '''
        Initialize the parameters of AINewsRelatedClassifier
        '''
        filename = "IsRelated"
        svm_path = paths['svm.svm_data']
        self.mysvm = svm_load_model(svm_path + filename + ".model")
        self.range = {}
        self.__load_range(svm_path + filename + ".range")
        
       
        
    def __load_range(self, filename):
        """
        Read in the range file generated by svm-train tool which list the min
        and max value of each feature. Since the min value is always 0, only
        the max value is read and stored in a dictionary
        self.range[wordid] = max_value of the feature
        @param filename: the libSVM formatted input file
        @type filename: C{string}
        """
        lines = loadfile(filename)
        for line in lines[2:]:
            items = line[:-1].split(' ')
            self.range[int(items[0])] = float(items[2]) 
    
    def predict(self, data):
        '''
        Predict the story text to be AI-related or AI-NotRelated.
        @param data: the news story's term vector
        @type data: C{dict}
        '''
        scaled_data = {}
        for key in data:
            if key in self.range:
                scaled_data[key] = data[key] / self.range[key]
                
        isrelated = svm_predict([0], [scaled_data], self.mysvm)
        #print isrelated
        return isrelated
        
