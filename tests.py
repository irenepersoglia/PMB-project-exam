from translator import Translator
from utils import remove_version, parse_columns

import pandas as pd
import numpy as np 


def test_translate():
    """
    Test for the 'translate' method in the Translator class.
    """
    
    # Create test dataframe
    data = {"Italian": ["rosso", "blu", "giallo", "verde"], "English": ["red", "blue", "yellow", "green"]}
    dictionary = pd.DataFrame(data)    
    dictionary = Translator(dictionary, 1)
    
    translated_word = dictionary.translate("yellow", "Italian")
    
    assert translated_word == "giallo"
    
def test_translate_row():
    """
    Test for the 'translate_row' method in the Translator class.
    """

    # Create test dataframes
    data1 = {"Italian": ["rosso", "blu", "giallo", "verde"], "English": ["red", "blue", "yellow", "green"]}
    dictionary = pd.DataFrame(data1)    
    dictionary = Translator(dictionary, 1)

    data2 = {"Words": ["blue", "yellow"]}
    translator_data_test = pd.DataFrame(data2)

    translated_row = dictionary.translate_row(translator_data_test.iloc[0], "Words", "Italian")
    
    assert translated_row == "blu"
    
def test_translate_table():
    """
    Test for the 'translate_table' method in the Translator class.
    """

    # Create test dataframes
    data1 = {"Italian": ["rosso", "blu", "giallo", "verde"], "English": ["red", "blue", "yellow", "green"]}
    dictionary = pd.DataFrame(data1)    
    dictionary = Translator(dictionary, 1)

    data2 = {"Words": ["blue", "yellow"]}
    translator_data_test = pd.DataFrame(data2)

    translated_table = dictionary.translate_table(translator_data_test, "Words", "Italian")

    assert translated_table.iloc[0,0] == "blu"
    assert translated_table.iloc[1,0] == "giallo"


def test_remove_version():
    """
    Tests if, given a known dataframe, the new gene names are the
    expected ones.
    """
    
    df_rm_ver = pd.read_csv("test/gene_data_test.bed", sep = "\t")
    column = "gene_id"
    df_rm_ver[column] = df_rm_ver.apply(lambda row : remove_version(row, ".", column), axis = 1)

    assert df_rm_ver[column][0] == "ENSG00000223972"
    assert df_rm_ver[column][1] == "ENSG00000227232"
    assert df_rm_ver[column][2] == "ENSG00000238009"
    assert df_rm_ver[column][3] == "ENSG00000233750"


def test_parse_columns():
    """
    Tests if given two known dataframes:
        - the columns of the new ones are of the same length
        - the columns are the expected ones
    """

    d1 = {"A":[1,2,3], "B":[2,4,1], "D":[3,1,2], "E":[2,3,4]}
    d2 = {"B":[6,9,7], "C":[9,5,8], "E":[8,9,5], "F":[6,8,7], "I":[5,6,7]}
    df1 = pd.DataFrame(d1)
    df2 = pd.DataFrame(d2)
    
    df1_new, df2_new = parse_columns(df_1=df1, df_2=df2)
    
    assert len(df1_new.columns) == len(df2_new.columns)
    assert df1_new.columns.all() == "B" or "E"
    assert df2_new.columns.all() == "B" or "E"