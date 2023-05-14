import pandas
class Translator:
    """
    Class to be used as a translator, given a word to translate and a dictionary for reference  
    """
    def __init__(self, dict_table: pandas.DataFrame):
        self.index_dict_table = dict()
        self.dict_table: pandas.DataFrame = dict_table
        self.set_dict_table()
       
    def set_dict_table(self):
        languages = self.dict_table.columns
        for idx, row in self.dict_table.iterrows():
            for language in languages:
                word = row[language]
                if word not in self.index_dict_table:
                    self.index_dict_table[word] = []
                self.index_dict_table[word] = [idx, language]

    def translate(self, word, desired_language):
        translated_word = ""
        language = ""
        try:
            word_index, language = self.index_dict_table[word]
        except KeyError:
            return None
        
        translated_word = self.dict_table.at[word_index, desired_language]
        
        return translated_word

def translate_table(row, column, desired_language):
    return translator.translate(row[column], desired_language)
