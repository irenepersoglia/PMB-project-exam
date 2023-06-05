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
python translate_proteins.py --dictionary <dictionary>  --table <data to be preprocessed> --num_processes <the number of parallel processses in the multiprocessing> --save_table <yes or no>
```
where the last argument saves a copy of the new translated table in the same directory.\
For the gene expression analysis, the reference file is [this one](https://github.com/irenepersoglia/PMB-project-exam/blob/main/translate_proteins.py). As before, to run from the command line type:
```
python translate_genes.py --dictionary <dictionary>  --first_table <first set of data to be preprocessed> --second_table <second set of data to be preprocessed> --num_processes <the number of parallel processses in the multiprocessing> --save_table <True or False>
```
As you can see it takes as arguments two different tables, since for the further analysis it will be important that the same subjects only are kept in the two dataframes. 
