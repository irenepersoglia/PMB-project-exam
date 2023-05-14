# PMB-PANDA-project

The aim of the project was the study of regulatory relationships between cell lines and their tissues of origin.\
In particular, the tool that is used to calculate the networs is PANDA (Passing Attributes between Networks for Data Assimilation), an open source tool which conveys multiple sources of information to predict regulatory relationships between genes. 

### Data used for this project
In particular, the study focuses on two cell lines (LCLs and primary fibroblast) and their two relative tissues of origin (blood and skin samples, respectively), and the goal is to compare the regulatory networks of the pairs. The data required to run the simulation is composed by three networks, two of them being common to all four kind of data, and one relative to each group. The first two networks are called the **motif prior** and the **protein-protein interaction networks**, while the latter is the **gene expression network**, which is clearly different for each one of the four samples. 

### The PANDA package
The package used in this study is called PANDA (check [their Github](https://github.com/netZoo/netZooPy) for a detailed descritpion). In particular, PANDA considers initial networks as composed by effector and affected nodes, where the information can flow between tep effectors or affectors or, more importantly, between an effector node and its affected target, along the so-called "routes of affection". Then, by using a message-passing procedure, it assimilates the various initial information inot one coherent model, passing attributes between the effectors and their affected targets along the various routes of affection and updating each until all three are in agreement with one another.

## Installation
To install the application, please use the following code:
```
git clone https://github.com/irenepersoglia/PMB-project-exam.git
cd PMB-project-exam
pip install -r requirements.txt
```
## Usage
When installed, the user can run the program from the command line. According to the path where you data is stored, type:
```
python netZooPy/panda/run_panda.py -e netZooPy/tests/ToyData/ToyExpressionData.txt -m netZooPy/tests/ToyData/ToyMotifData.txt -p netZooPy/tests/ToyData/ToyPPIData.txt -f True -o test_panda.txt
```
where:
* the **motif prior** is typically a TF-by-gene matrix, with values ranging from 0 to 1, where 1 indicates the presence of sequence (motif) of a TF in the gene regualtory region, and 0 otherwise
* the **gene expression data** is typically a gene-by-sample matrix containing expression data
* the **PPI network** (protein-protein interaction network) is a TF-by-TF matrix, with values ranging from 0 to 1, where 1 indicates a physical interaction between two TFs and 0 otherwise
\
An example of dataset that can be used in this analysis can be found [here]().

## Project structure and organization
After setting in input the required data, the greatest part of the project is the cleaning and preparing of the data themselves. In particular, it is important for the genes present in the three networks to be expressed according to the same nomenclature (ENSEMBL, HGNC, etc.). In this script, this "translating" procedure is repeated for both the PPI prior and the gene expression data, to make them compatible with the motif prior. Of course, in order to do so, an additional matrix to be used as dictionary is needed. \
Then, the expression data is reduced to only samples present in both of the networks used at the end to compare the regulatory networks.\
Finally, PANDA is run on the prepared data. Additionally, is also available a function which calculates the difference in the out-degree (defined as the sum of all outgoing edges for each TFs) between the cell line and the tissue of origin to be compared. In this way it is possible to rank the most targeting TFs, as positive values for this ou-degree difference indicate higher targeting in cell lines, while negative values indicate higher targeting in tissues. 
