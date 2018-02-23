# DeepReinforcementLearning
A replica of the AlphaZero methodology in Python

See this article for a summary of the algorithm and run instructions.

https://applied-data.science/blog/how-to-build-your-own-alphazero-ai-using-python-and-keras/


## GETTING STARTED
To start the learning process, run the top two panels in the run.ipynb Jupyter notebook. 
Only when it has built up enough game positions to fill its memory will the neural network will begin training.

Therefore, you will need to leave it running until the memory size, which is listed in the output in the Jupyter notebook 
reaches the MEMORY_SIZE specified in the config.py file. (defaults to "30000")

<strong>This initial training can take many hours</strong> and if you stop it before 
the MEMORY_SIZE parameter is reached, you will not get a model in run/models and 
the next cells in run.ipynb will not work. so... have some patience during training!
