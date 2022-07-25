# HybridFC: A Hybrid Fact-Checking Approach for Knowledge Graphs

![Screenshot from 2022-07-25 22-22-05](https://user-images.githubusercontent.com/10128056/180878241-bae8b3f6-88da-49ca-97d1-aeb6c0357c83.png)

This open-source project contains the Python implementation of our approach HybridFC. This project is designed to ease real-world applications of fact-checking over knowledge graphs and produce better results. With this aim, we rely on:

1. [PytorchLightning](https://www.pytorchlightning.ai/) to perform training via multi-CPUs, GPUs, TPUs or  computing cluster, 
2. [Pre-trained-KG-embeddings](https://embeddings.cc/) to get pre-trained KG embeddings for knowledge graphs for knowledge graph-based component, 
3. [Elastic-search](https://www.elastic.co/blog/loading-wikipedia) to load text corpus (wikipedia) on elastic search for text-based component, and
4. [Path-based-approach](https://github.com/dice-group/COPAAL/tree/develop) to calculate output score for the path-based component.


## Installation
First clone the repository:
``` html
git clone https://github.com/factcheckerr/HybridFC.git

cd HybridFC
``` 

## Reproducing Results
There are two options to repreoduce the results. (1) using pre-generated data, and (2) Regenerate data from scratch.
Please chose any 1 of the these 2 options.

### 1) Re-Using pre-generated data
download and unzip data and embeddings files in the root folder of the project.

``` html
pip install gdown

wget https://zenodo.org/record/6523389/files/dataset.zip

wget https://zenodo.org/record/6523438/files/Embeddings.zip


unzip dataset.zip

unzip Embeddings.zip
``` 


Note: if it gives permission denied error you can try running the commands with "sudo"

### 2) Regenerate data from scratch (FactCheck output)
In case you don't want to use pre-generated data, follow this step:

run FactCheck on [FactBench dataset](https://github.com/DeFacto/FactBench) using [Wikipedia](https://www.elastic.co/blog/loading-wikipedia) as a reference corpus. 

As an input user needs output of [FactCheck](https://github.com/dice-group/FactCheck/tree/develop-for-FROCKG-branch) in json format.

Put the result json file in dataset folder.

Further details are in readme file in [overall_process folder](https://github.com/factcheckerr/HybridFC/tree/master/overall_process)

## Running experiments
Install dependencies via conda:
``` html

#setting up environment
#creating and activating conda environment

conda env create -f environment.yml

conda activate hfc2
```
start generating results:
``` html

# Start training process, with required number of hyperparemeters. Details about other hyperparameters is in main.py file.
python main.py --emb_type TransE --model full-Hybrid --num_workers 32 --min_num_epochs 100 --max_num_epochs 1000 --check_val_every_n_epochs 10 --eval_dataset FactBench 

# computing evaluation files from saved model in "dataset/Hybrid_Stroage" directory
python evaluate_checkpoint_model.py --emb_type TransE --model full-Hybrid --num_workers 32 --min_num_epochs 100 --max_num_epochs 1000 --check_val_every_n_epochs 10 --eval_dataset FactBench
``` 

##### comments:
for differnt embeddings type(emb_type) or model type(model), you just need to change the parameters.

Available embeddings types:
[ConEx](https://arxiv.org/pdf/2008.03130.pdf), [TransE](https://everest.hds.utc.fr/lib/exe/fetch.php?media=en:cr_paper_nips13.pdf), [ComplEx](https://arxiv.org/abs/2008.03130), [RDF2Vec](https://madoc.bib.uni-mannheim.de/41307/1/Ristoski_RDF2Vec.pdf) (only for BPDP dataset), [QMult](https://arxiv.org/pdf/2106.15230.pdf).

Available models:
full-Hybrid, KGE-only, text-KGE-Hybrid, path-only, text-path-Hybrid, KGE-path-Hybrid

Note: model names are case sensitive. So please use exact names.

## ReGenerate AUROC results:
After computing evaluation results, the prediction files are saved in the "dataset/HYBRID_Storage" folder along with ground truth files.
These files can be uploaded to a live instance of [GERBIL](http://swc2017.aksw.org/gerbil/config) (by Roder et al.) framework to produce AUROC curve scores.  

## Future plan:
TODO
## Acknowledgement 
The work has been supported by the EU H2020 Marie Skłodowska-Curie project KnowGraphs (no. 860801)).
## Authors
TODO







