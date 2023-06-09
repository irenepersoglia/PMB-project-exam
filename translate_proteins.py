import argparse
import pandas as pd
import numpy as np

from translator import Translator
import utils

if __name__ == "__main__":

    # Command line parser
    argparser = argparse.ArgumentParser(prog = 'PMB_project_exam', description = 'PMB_project_exam')
    argparser.add_argument('--dictionary', type = str, help = 'set the dictionary for the translation', default = "", required = True)
    argparser.add_argument('--table', type = str, help = 'set the table to translate', default = "", required = True)
    argparser.add_argument('--num_processes', type = int, help = 'set the number of processes', default = 1, required = False)
    argparser.add_argument('--save_table', help = '(optional) saves the translated file', default = False, required = False, action="store_true")


    # Parameters
    args = argparser.parse_args()
    dictionary_path = args.dictionary
    table_path = args.table
    n_processes = args.num_processes
    save_table = args.save_table
    
    # Take columns names (languages) from the dictionary
    with open(dictionary_path, "r") as file:
        header = file.readline()
        
    cols = [col.strip() for col in header.strip("#").split("/")]
    
    # Load dictionary dataframe
    dictionary_df = pd.read_csv(dictionary_path, sep = '\t', comment = "#", names = cols)
    languages = cols[1:]    # keep only the columns with the languages
    dictionary_df = dictionary_df[languages]
    
    # Define translator
    translator = Translator(dictionary_df, n_processes)
    
    # Load table to translate
    table_df = pd.read_csv(table_path, sep = " ")
    table_df["combined_score"] = np.dot(table_df["combined_score"], 0.001)
    
    # Translate table
    table_df = utils.translation_table(table_df, translator, "protein", "display name")

    # Save the new table in the same path
    if save_table:
        utils.save_table(table_df, table_path)