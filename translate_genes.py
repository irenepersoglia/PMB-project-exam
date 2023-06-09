import argparse
import pandas as pd
import numpy as np

from translator import Translator
import utils

if __name__ == "__main__":

    # Command line parser
    argparser = argparse.ArgumentParser(prog = 'PMB_project_exam', description = 'PMB_project_exam')
    argparser.add_argument('--dictionary', type = str, help = 'set the dictionary for the translation', default = "", required = True)
    argparser.add_argument('--first_table', type = str, help = 'set the first table to translate', default = "", required = True)
    argparser.add_argument('--second_table', type = str, help = 'set the second table to translate', default = "", required = True)
    argparser.add_argument('--num_processes', type = int, help = 'set the number of processes', default = 1, required = False)
    argparser.add_argument('--save_table', help = '(optional) saves the translated files', default = False, required = False, action="store_true")


    # Parameters
    args = argparser.parse_args()
    dictionary_path = args.dictionary
    first_table_path = args.first_table
    second_table_path = args.second_table
    n_processes = args.num_processes
    save_table = args.save_table

    # Load dictionary dataframe and set the languages
    dictionary_df = pd.read_csv(dictionary_path, sep = ',')
    dictionary_df = dictionary_df.dropna()
    languages = dictionary_df.columns
    dictionary_df = dictionary_df[languages]
    
    # Define translator
    translator = Translator(dictionary_df, n_processes)
    
    # Load the two tables to translate with a pre-processing (remove version and unwanted columns)
    first_table_df = utils.import_genes_table(first_table_path)    
    second_table_df = utils.import_genes_table(second_table_path)
 
    # Translate first table
    columns_to_translate = [col for col in first_table_df.columns if "gene" in col]
    
    for column in columns_to_translate:
        first_table_df = translator.translate_table(first_table_df, column, "Gene name")
    
    first_table_df = first_table_df.replace(to_replace='None', value=np.nan).dropna()
        
    # Translate second table
    columns_to_translate = [col for col in second_table_df.columns if "gene" in col]
    
    for column in columns_to_translate:
        second_table_df = translator.translate_table(second_table_df, column, "Gene name")
        
    second_table_df = second_table_df.replace(to_replace='None', value=np.nan).dropna()
    
    # Parse the two tables to keep only the same subjects for subsequent analysis
    first_table_df, second_table_df = utils.parse_columns(df_1=first_table_df, df_2=second_table_df)
    
    # Save the new tables in the same path
    if save_table:
        translated_first_table_file_name = "translated_" + first_table_path.split("/")[-1]
        translated_first_table_path = "/".join(first_table_path.split("/")[:-1])
        translated_first_table_path += "/"
        translated_first_table_path += translated_first_table_file_name
        first_table_df.to_csv(translated_first_table_path, index = False)
    
        translated_second_table_file_name = "translated_" + second_table_path.split("/")[-1]
        translated_second_table_path = "/".join(second_table_path.split("/")[:-1])
        translated_second_table_path += "/"
        translated_second_table_path += translated_second_table_file_name
        second_table_df.to_csv(translated_second_table_path, index = False)