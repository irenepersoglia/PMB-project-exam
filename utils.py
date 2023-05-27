
def remove_version(data, partition_symbol, column):
    """ 
    Function that removes the assembly version from the genes that are expressed according to the Ensembl nomenclature

    Args:
        data (any): Ensembl gene name, the row of the df
        partition_symbol (str): usually '.'
        column (str): name of the df column to be processed

    Returns:
        gene_id: the identification name of the gene without assembly version
    """
    # identify the two parts before and after a specified symbol
    gene_id, sep, version = data[column].partition(partition_symbol)
    
    return gene_id

def parse_columns(df_1, df_2):
    """
    Function that parse two DataFrames and returns them with only the common columns

    Args:
        df_1 (DataFrame): first DataFrame
        df_2 (DataFrame): second DataFrame

    Returns:
        df_1, df_2 : the two DataFrames with only the columns that appear in both
    """
    # identify the columns
    column_list_1 = df_1.columns
    column_list_2 = df_2.columns
    
    # create a list with only the columns in common between the two DFs
    cols_list =  [x for x in column_list_1 if x in column_list_2]
    print(cols_list)
    
    return df_1[cols_list], df_2[cols_list]