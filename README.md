# HybridFC: A Hybrid Fact-Checking Approach over Knowledge Graphs

![Screenshot from 2022-07-25 22-22-05](https://user-images.githubusercontent.com/10128056/180878241-bae8b3f6-88da-49ca-97d1-aeb6c0357c83.png)

This open-source project contains the Python implementation of our approach [HybridFC](https://papers.dice-research.org/2022/ISWC_HybridFC/public.pdf). This project is designed to ease real-world applications of fact-checking over knowledge graphs and produce better results. With this aim, we rely on:

1. [PytorchLightning](https://www.pytorchlightning.ai/) to perform training via multi-CPUs, GPUs, TPUs, or  computing clusters, 
2. [Pre-trained-KG-embeddings](https://embeddings.cc/) to get pre-trained KG embeddings for knowledge graphs for knowledge graph-based component, 
3. [Elastic-search](https://www.elastic.co/blog/loading-wikipedia) to load text corpus (Wikipedia) on the elastic search for text-based component, and
4. [Path-based-approach](https://github.com/dice-group/COPAAL/tree/develop) to calculate the output score for the path-based component.


## Installation
First, clone the repository:

``` html
git clone https://github.com/factcheckerr/HybridFC.git

cd HybridFC
``` 

## Reproducing Results
There are two options to reproduce the results. 
1) using pre-generated data, and
2) Regenerate data from scratch.
Please choose any 1 of these 2 options.

### 1) Re-using pre-generated data
download and unzip data and embedding files in the root folder of the project.

``` html
pip install gdown

wget https://files.dice-research.org/datasets/ISWC2022_HybridFC/data.zip

unzip data.zip
``` 


Note: if it gives permission denied error you can try running the commands with "sudo"

### 2) Regenerate data from scratch (FactCheck and COPAAL output)
In case you don't want to use pre-generated data, follow this step:

run KGV to collect results from FactCheck and COPAAL.

run FactCheck on [FactBench](https://github.com/DeFacto/FactBench), [FaVel](https://github.com/ltphen/favel/tree/develop/Datasets/Favel_Dataset), and [BPDP](https://github.com/ltphen/favel/tree/develop/Datasets/BPDP/BPDP_Dataset) datasets using [Wikipedia](https://www.elastic.co/blog/loading-wikipedia) as a reference corpus. 

As an input user needs the output of [FactCheck](https://github.com/dice-group/FactCheck/tree/develop-for-FROCKG-branch) in JSON format.

JSON format is as follows:

``` html
-=-=-=-=-=-=-==-=-==-=-=-=-==-=-=-=-=-=-=-==-=-=-=-
10
/factbench/test/correct/death/death_00053.ttl
 defactoScore: 0.98 setProofSentences : [ComplexProofs{website='https://en.wikipedia.org/wiki/Reba White Williams', proofPhrase='In 1999 , White Williams ran unsuccessfully for the New York City City Council in District 4 .', trustworthinessScore='0.997908778988452'}, ComplexProofs{website='https://en.wikipedia.org/wiki/James Leo Herlihy', proofPhrase='Like Williams , Herlihy had lived in New York City .', trustworthinessScore='0.9975670565782072'}, ComplexProofs{website='https://en.wikipedia.org/wiki/Charles Williams (musician)', proofPhrase='Charles Isaac Williams -LRB- born July 18 , 1932 -RRB- is an alto saxophonist based in New York City .', trustworthinessScore='0.9991775993927828'}] subject : Tennessee Williams object : New York City predicate deathPlace
-=-=-=-=-=-=-==-=-==-=-=-=-==-=-=-=-=-=-=-==-=-=-=-

``` 

Put the result JSON file in the data folder.

Further details are in the readme file in [overall_process folder](https://github.com/factcheckerr/HybridFC/tree/master/overall_process)

## Running experiments
Install dependencies via conda:
``` html

#setting up the environment
#creating and activating the conda environment

conda env create -f environment.yml

conda activate hfc2

#If conda command not found: download miniconda from (https://docs.conda.io/en/latest/miniconda.html#linux-installers) and set the path: 
#export PATH=/path-to-conda/miniconda3/bin:$PATH

```
start generating results:
``` html

# Start the training process, with the required number of hyperparameters. Details about other hyperparameters are in the main.py file.
python main.py --emb_type CoNex --model full-Hybrid --num_workers 32 --min_num_epochs 100 --max_num_epochs 1000 --check_val_every_n_epochs 10 --eval_dataset FactBench 

# Computing evaluation files from the saved model in "dataset/Hybrid_Stroage" directory
python evaluate_checkpoint_model.py --emb_type TransE --model full-Hybrid --num_workers 32 --min_num_epochs 100 --max_num_epochs 1000 --check_val_every_n_epochs 10 --eval_dataset FactBench
``` 


##### comments:
1. To reproduce similar results you have to use the exact parameters as listed above.

2. For other datasets you need to change the parameter in front of --dataset

3. Use GPU for fast processing. The default parameter is set to 2 GPUs that we used to generate results.

4. For different embeddings type(emb_type) or model type(model), you just need to change the parameters. 

5. For differnt embeddings type(emb_type) or model type(model), you just need to change the parameters.

Available embeddings types:
[ConEx](https://arxiv.org/pdf/2008.03130.pdf), [TransE](https://everest.hds.utc.fr/lib/exe/fetch.php?media=en:cr_paper_nips13.pdf), 

The following can be added:
[ComplEx](https://arxiv.org/abs/2008.03130), [RDF2Vec](https://madoc.bib.uni-mannheim.de/41307/1/Ristoski_RDF2Vec.pdf) (only for BPDP dataset), [QMult](https://arxiv.org/pdf/2106.15230.pdf).

Available models:
hybridfc-full-Hybrid, KGE-only,text-only, text-KGE-Hybrid, path-only, text-path-Hybrid, KGE-path-Hybrid

Note: model names are case-sensitive. So please use exact names.

## ReGenerate AUROC results:
After computing evaluation results, the prediction files are saved in the "dataset/HYBRID_Storage" folder along with ground truth files.
These files can be uploaded to a live instance of [GERBIL](http://swc2017.aksw.org/gerbil/config) (by Roder et al.) framework to produce AUROC curve scores.  

## Future plan:
In future work, we will exploit the modularity of HybridFC by integrating rule-based approaches and path embedding. We also plan to explore other possibilities to select the best evidence sentences.

## Acknowledgement 
The work has been supported by the EU H2020 Marie Skłodowska-Curie project KnowGraphs (no. 860801)).

## Authors
 * [Umair Qudus](https://dice-research.org/UmairQudus) (DICE, Paderborn University) 
 * [ Michael Röder](https://dice-research.org/MichaelRoeder) (DICE,  Paderborn University) 
 * [Muhammad Saleem](https://dice-research.org/MuhammadSaleem) (DICE,  Paderborn University) 
 * [Axel-Cyrille Ngonga Ngomo](https://dice-research.org/AxelCyrilleNgongaNgomo) (DICE,  Paderborn University)
  






