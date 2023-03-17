# AGNI-Text
Text and Speech obscenity detection module for AGNI. 
This module employees SVM for detecting obscenity in texts. We are working on employing BERT as an improved model for 
classification, if it doesn't cause significant changes in the server costs. The ASR module is based on current SOTA model
for Speech to Text by Paddle Paddle. 

## Steps to use this repo locally: 
### Download miniconda (if you don't have):
Follow the steps mentioned [here](https://conda.io/projects/conda/en/stable/user-guide/install/linux.html) to download Miniconda 
in your device. 
## Steps:
1. Create a conda environment: `conda create -n kavach-text python=3.7.10`
2. Activate the environment: `conda activate kavach-text`
3. Install requirements: `pip install -r requirements.txt`
4. Run the server: `python app.py`

---
Feel free to raise issues if you face any issues while running there server. 
