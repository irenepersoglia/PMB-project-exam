# PMB-PANDA-project

The aim of the project was the study of regulatory relationchips between cell lines and their tissues of origin. The tool that is used to calculate the networks is PANDA (Passing Attributes between Networks for Data Assimilation), an open source tool which conveys multiple sources of information to predict regulatory relationships between genes. \
Since the data required by PANDA should be in a particular format, this work is mainly focused on the cleaning and preprocessing of the newtorks, as requested by the PANDA package. 

### Data used for this project
In particular, this project focused on the comparison of regulatory netwoks between cell lines and their tissues of origin (LCLs vs blood samples and primary fibroblasts vs skin samples). The data required to run the simulation consist of a motif prior network, a protein-protein interaction network, and four gene expression networks, one for each kind of sample. In particular, the gene expression data is typically a gene-by-sample matrix containing expression data, while the protein-protein interaction network is a TFs-by-TFs (TFs: transcription factors) matrix, with valyes ranging from 0 to 1, where 1 indicates a physical interaction between genes and 0 otherwise.\
The data was retrieved by two databases that are widely used in the bioscientific field. The first is the String database, which gives access to all known and predicted protein-protein interaction data, not only for the Homo Sapiens (as it is in this case) but also for all the different kind of organisms.\
The second database used is GTEx, a data resource and tissue bank which studies the relationship between genetic variants and gene expression in multiple human tissues and across individuals.\
A smaller sample of the used data can be found in the [example folder](https://github.com/irenepersoglia/PMB-project-exam/tree/main/example).

## The project goal
The purpose of this project is to clean and prepare the protein-protein interaction network and the gene expression networks to be compatible with the data required to run the PANDA package. For a better understanding of how the package works, please refer to [their Github page](https://github.com/netZoo/netZooPy).\
Briefly, this script takes as inputs the networks that PANDA will analyze, and preprocess them in order to be used correctly. In particular in this case it works as a gene and protein "translator", changing the nomenclature of genes and proteins according to a given dictionary. In this way the networks can agree with one another, being expressed according to the same nomenclature.

## Installation
To install the application, please use the following code:
```
git clone https://github.com/irenepersoglia/PMB-project-exam.git
cd PMB-project-exam
pip install -r requirements.txt
```

## Usage
When installed, the user can run the program from the command line. There are actually two different ways in which the data can be processed, depending on the kind of data. While for the protein-protein interaction it is simply a substitution according to the uploaded dictionary, for the gene expression data the matter is slightly more complicated. In the present study, the networks for the gene expression must be cleaned in order to keep only the same set of subjects in both, otherwise a comparison as in this case would be useless. Hence, there are additional functions that are added in this second case.\
For more clarity, two different scripts have been created, depending on the desired data.\
For the protein-protein interaction analysis, the reference file is [this one](https://github.com/irenepersoglia/PMB-project-exam/blob/main/translate_proteins.py). To run the script type in the command line:
```
python translate_proteins.py --dictionary <dictionary>  --table <data to be preprocessed> --num_processes <the number of parallel processses in the multiprocessing> --save_table <optional>
```
where the last argument saves a copy of the new translated table in the same directory.\
For the gene expression analysis, the reference file is [this one](https://github.com/irenepersoglia/PMB-project-exam/blob/main/translate_proteins.py). As before, to run from the command line type:
```
python translate_genes.py --dictionary <dictionary>  --first_table <first set of data to be preprocessed> --second_table <second set of data to be preprocessed> --num_processes <the number of parallel processses in the multiprocessing> --save_table <optional>
```
As you can see it takes as arguments two different tables, since for the further analysis it will be important that the same subjects only are kept in the two dataframes. 

## Project structure
After setting as inputs the requested dataframes and the number of processes, it is possible to run the script. In particular, any data retrieved from the two cited databases is suitable for the analysis, while the dictionary dataframes please refer to the [Example section](#example).\

First, the program creates an object "translator" from the dictionary, also setting the languages for the translation. At this point, the table that has to be translated according to the nomenclature indicated in the dictionary is cleaned in order to keep only the data that will be used by PANDA.\
In the case of the protein-protein interaction table, the column that indicates the interaction score between genes is divided by a factor of 10^3, since this value must range between 0 and 1.\
For the gene expression data instead, the columns with the chromosome indications are removed, leaving us with only the gene names and their expression values relative to each subject in the dataframe.

After this, the translation begins. The Translator class identifies the word (protein or gene name) in the dictionary, finding the translation, and subsequently translates the corrispondent row in the original table. By doing this on the whole table with the apply function, the program returns the whole translated table.\

In the case of gene expression data, since the goal of this project was to prepare the data to be used in a PANDA analysis about a comparison between cell lines and tissue samples, the programm additionally cleans the translated tables in order to keep only the same tested subjects.

### Number of processes and asynchronous multiprocessing
To speed up the process in case of large data, the user can define as input the number of processes used by the program. The number of processes used must be chosen carefully, since a too many processes can use all the cpu available, bringing actually no benefit to the processing time. The number of processes is an optional argument, hence if the user does not provide any, a default value of 1 will be assigned.

Additionally, it has been chosen to additionally reduce the computational time, since this kind of data, especially protein-protein interaction data, can be extremely big. In order to parallelize the processing, the data to be analyzed are splitted into chunks that are translated separately, and eventually merged again in the right order at the end of the process.\

## Testing
A "test" folder has been added to the repository with all the data requited to run the tests.py file. This file contains the tests runned to assert the program integrity and precision.\
To run this from the command line, type:
```
pytest tests.py
```

## Example
In this section an example of the usage is presented. An "example" folder has been added to this repository, so that the user can try to run the scripts with this toy data.\
Inside the folder data two sub-folders are present, each containg the toy data for the protein-protein interaction analysis and the gene expression analysis. While the dataframes for the tables to translate are reduced to only a small subsection (since real data would have been too large), the files used as dictionaries are obviously the original ones. For the protein analysis, the samples taken are the ones for Homo Sapiens, while for the gene expression data, small subsets of samples relative to blood and lymphocytes are reported.\
To run the two distinct scripts from the command line:
```
python translate_proteins.py --dictionary example/proteins/human.name_2_string.tsv --table example/proteins/9606.protein.links.v11.5.txt --num_processes 4 --save_table
```
```
python translate_genes.py --dictionary example/genes/mart_export.txt --first_table example/genes/Whole_Blood_Analysis.v6p.normalized.expression.bed --second_table example/genes/Cells_EBV-transformed_lymphocytes_Analysis.v6p.normalized.expression.bed --num_processes 4 --save_table
```
This process takes up from less than a minute up to a few minutes to complete, depending on the power of the user's machine. 
##
Following this scripts, any data retrieved from the cited databases could be analyzed, but it is strongly recommended that the the dictionaries used in both cases are the ones provided by this example folder.
