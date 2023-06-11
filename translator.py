import pandas
import multiprocessing as mp 
import warnings
import numpy as np
from tqdm import tqdm

import utils

class Translator:
    """
    Class to be used as a translator, given a word or table to translate, and a dictionary for reference.
    """
    
    def __init__(self, dict_table: pandas.DataFrame, num_processes: int):
        """
        This function initializes the object attributes.

        Args:
            dict_table (pandas.DataFrame): the data to be passed to the class as dictionary for the translation
            num_processes (int): the number of parallel processes applied
        """
        
        self.num_processes: int = num_processes
        self.index_dict_table = dict()
        self.dict_table: pandas.DataFrame = dict_table
        self.set_dict_table()
       
    def set_dict_table(self):
        """
        Function that sets the dictionary, identifying the languages for the translation and the words' indexes.
        """
        
        languages = self.dict_table.columns
        for idx, row in self.dict_table.iterrows():
            for language in languages:
                word = row[language]
                if word not in self.index_dict_table:
                    self.index_dict_table[word] = []
                self.index_dict_table[word] = [idx, language]

    def translate(self, word, desired_language):
        """
        This function finds the translated word.

        Args:
            word: the word to be translated
            desired_language: the desired translation language

        Returns:
            the translated word in the dictionary table
        """
        
        translated_word = ""
        try:
            word_index, _ = self.index_dict_table[word]
        except KeyError:
            return None
        
        translated_word = self.dict_table.at[word_index, desired_language]
        
        return translated_word

    def translate_row(self, row, column, desired_language):
        """
        Given a table, this function returns the translated word in that table,
        identified by its row and column.
        
        Args:
            row: the row of the word to be translated
            column: the column of the word to be translated
            desired_language: the desired translation language

        Returns:
            translated word: the translated word
        
        """
        
        return self.translate(row[column], desired_language)
    
    def translate_worker(self, args):
        """
        This function translates a whole table, returning another table
        with all the words translated according to the dictionary.
        It is called by the several processes and the process_id 
        identifies the process.

        Args:
            process_id: identifies the process, given by the input variable 'num_processes'
            table: the table to be translated
            column: the table's column to be translated
            desired_language: the desired language for the translation

        Returns:
            table: the translated table
        """
        
        process_id = args[0]
        column = args[1]
        table = args[2]
        desired_language = args[3]
        
        # Create a progress bar for each process
        tqdm.pandas(desc='worker #{}'.format(process_id), position=process_id)
        
        # Use the 'apply' function to extend the translation to the entire column
        table[column] = table.progress_apply(lambda row: self.translate_row(row, column, desired_language), axis=1)
        
        return table    
    
    def translate_table(self, table, column, desired_language):
        """
        This function implements the translation with a multiprocess procedure. 
        It splits the dataframe according to the number of processes and 
        proceeds to apply the translation in each separately. 
        Finally it merges the different parts returning the whole translated table.  

        Args:
            table: the table to be translated
            column: the table's column to be translated
            desired_language: the desired language for the translation

        Returns:
            table: the translated table
        """
        
        if self.num_processes == 1:
            table = self.translate_worker(args=([self.num_processes, column, table, desired_language]))
        else:
            if self.num_processes == 0: 
                warnings.warn("No number of processes specified, the program will use all available cpu. This may slow down your pc.")
                self.num_processes = mp.cpu_count()
            # Divide the dataframe according to the number of processes    
            splitted_df = np.array_split(table, self.num_processes)

            # Start processes in asyncronous way
            with mp.Pool(processes = self.num_processes) as pool:
                for i in range(self.num_processes):
                    results = pool.apply_async(self.translate_worker, args=([i, column, splitted_df[i], desired_language],))

                # Get the results and merge them in a table
                table = results.get()
                # Close the process pool
                pool.close() 
                # Wait for all tasks to complete
                pool.join() 
            
        return table
