# What is this repository?

This repository contains the source code for the paper: `Detecting Potential Fraudulent Trading Patterns in Decentraland: A Data-Driven Analysis of the Ethereum Network and OpenSea Marketplace`, as part of the research project for the course CS 846: Software Engineering for Big Data and Artificial Intelligence, Fall 2024.


## Resesarch Contributors
- Hesam Sarkhosh (hsarkhos@uwaterloo.ca)

## Content Review

There are three main folders in the root directory: (you can also find the [presentation.pptx](./presentation.pptx) and [proposal.pdf](./proposal.pdf) in the root directory.)

### [/analysis](/analysis/)
This folder contains all the source code for parsing, filtering, analyzing and visualizing on the analysis (reseatch questions) section.

### [/dataset](/dataset/)
This folder contains all the datasets used in this research, including the kaggle datasets for labeling of the first approach (failed). The `IITP_VDLand` dataset is shared separatly in the email and excluded (.gitignore) from the puplic repository. 
- [/2404.07533v1.pdf](./dataset/2404.07533v1.pdf) -> The IITP_VDLand paper

### [/model](/model/)
This directory contains the codes for training the proposed model on the dataset:
- [/electronics-12-03180-v2.pdf](./model/electronics-12-03180-v2.pdf) -> The paper which Graph Embedding Algoeithm is based on
- [/main.ipynb](./model/main.ipynb) -> The notebook which incldues all the codes of the implementation section inlcuding preprocessing, embedding algorithm and model training.
- [/main.pdf](./model/main.pdf)` -> For ease of access, the pdf version of the notebook is porvided.
- [/random_forest_model.joblib](./model/random_forest_model.joblib) -> an export of the random forest classifier model in the second approach. (see the notebook for more information.)


## How to Run [main.ipynb](./model/main.ipynb)?

You can decide whether to install packages globally or on a `.venv`. Despite that, the gerenal steps are as below:
```
# Step 1: Installing Packages:
pip install -r /path/to/requirements.txt

# Step 2: Connect your venv to jupyter or VScode or any other environment you use and run the note book section by section.
```


## Acknowledgement 
The IITP_VDLand dataset used in this research was retrieved from the paper: [IITP-VDLand: A Comprehensive Dataset on Decentraland Parcels](https://arxiv.org/abs/2404.07533). We extend our gratitude to the authors for providing access to this dataset, which significantly contributed to the advancement of our study on virtual land analysis.

As the dataset has not been formally and publicly released, it is not included in this repository. For access to the dataset, please contact [Hesam Sarkhosh](mailto:hsarkhos@uwaterloo.ca) or the IITP_VDLand contributors.

The Embeddings used in this paper are from the paper: [Graph Embedding-Based Money Laundering Detection
for Ethereum](https://www.mdpi.com/2079-9292/12/14/3180). 

I would also like to express my sincere appreciation to Jun Lim ([jun.lim@uwaterloo.ca](mailto:jun.lim@uwaterloo.ca)) and Ayinde Yakubu ([ayakubu@uwaterloo.ca](mailto:ayakubu@uwaterloo.ca)) for their valuable contributions to certain aspects of the data analysis, conducted as part of an informal collaborative research initiative.
