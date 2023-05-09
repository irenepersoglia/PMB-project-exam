# PMB-PANDA-project

The aim of the project was the study of regulatory relationships between cell lines and their tissues of origin.\
In particular, the tool that is used to calculate the networs is PANDA (Passing Attributes between Networks for Data Assimilation), an open source tool which conveys multiple sources of information to predict regulatory relationships between genes. 

### Data used for this project
In particular, the study focuses on two cell lines (LCLs and primary fibroblast) and their two relative tissues of origin (blood and skin samples, respectively), and the goal is to compare the regulatory networks of the pairs. The data required to run the simulation is composed by three networks, two of them being common to all four kind of data, and one relative to each group. The first two networks are called the **motif prior** and the **protein-protein interaction networks**, while the latter is the **gene expression network**, which is clearly different for each one of the four samples. 

## The PANDA package
The package used in this study is called PANDA (https://github.com/netZoo/netZooPy) 
